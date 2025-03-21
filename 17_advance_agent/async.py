import os

import requests
import chainlit as cl
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
from agents.tool import function_tool
from typing import Optional, Dict

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Step 1: Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# Step 2: Model
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider)

# Step 3: Config
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)


@function_tool("get_asharib_data")
def get_asharib_data() -> str:
    """
    Fetches profile data about Asharib Ali from his personal API endpoint.

    This function makes a request to Asharib's profile API and returns information
    about his background, skills, projects, education, work experience, and achievements.

    Returns:
        str: JSON string containing Asharib Ali's profile information
    """

    try:
        response = requests.get("https://www.asharib.xyz/api/profile")
        if response.status_code == 200:
            return response.text
        else:
            return f"Error fetching data: Status code {response.status_code}"
    except Exception as e:
        return f"Error fetching data: {str(e)}"


agent = Agent(
    name="Greeting Agent",
    instructions="""You are a Greeting Agent designed to provide friendly interactions and information about Asharib Ali.

Your responsibilities:
1. Greet users warmly when they say hello (respond with 'Salam from Asharib Ali')
2. Say goodbye appropriately when users leave (respond with 'Allah Hafiz from Asharib Ali')
3. When users request information about Asharib Ali, use the get_asharib_data tool to retrieve and share his profile information
4. For any questions not related to greetings or Asharib Ali, politely explain: 'I'm only able to provide greetings and information about Asharib Ali. I can't answer other questions at this time.'

Always maintain a friendly, professional tone and ensure responses are helpful within your defined scope.""",
    model=model,
    tools=[get_asharib_data],
)


# Decorator to handle OAuth callback from GitHub
@cl.oauth_callback
def oauth_callback(
    provider_id: str,  # ID of the OAuth provider (GitHub)
    token: str,  # OAuth access token
    raw_user_data: Dict[str, str],  # User data from GitHub
    default_user: cl.User,  # Default user object from Chainlit
) -> Optional[cl.User]:  # Return User object or None
    """
    Handle the OAuth callback from GitHub
    Return the user object if authentication is successful, None otherwise
    """
    print(f"Provider: {provider_id}")  # Print provider ID for debugging
    print(f"User data: {raw_user_data}")  # Print user data for debugging

    return default_user  # Return the default user object


# Handler for when a new chat session starts
@cl.on_chat_start
async def handle_chat_start():
    # Initialize empty message history in the session
    cl.user_session.set("history", [])

    await cl.Message(
        content="Hello, how can I help you today?"
    ).send()  # Send welcome message


# Handler for incoming chat messages
@cl.on_message
async def handle_message(message: cl.Message):
    # Get message history from session
    history = cl.user_session.get("history", [])

    # Add user message to history
    history.append({"role": "user", "content": message.content})

    # Create a message for streaming the response
    msg = cl.Message(content="")
    await msg.send()

    # Run the agent with streaming
    result = Runner.run_streamed(
        agent,
        input=history,
        run_config=config,
    )

    # Stream the tokens as they come
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            await msg.stream_token(event.data.delta)

    # Add assistant response to history
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
