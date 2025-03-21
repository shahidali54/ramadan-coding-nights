import os  # For accessing environment variables
import chainlit as cl  # Web UI framework for chat applications
from dotenv import load_dotenv  # For loading environment variables
from typing import Optional, Dict  # Type hints for better code clarity
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.tool import function_tool
import requests

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize OpenAI provider with Gemini API settings
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# Configure the language model
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider)


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

    cl.user_session.set("history", [])  # Initialize empty chat history

    await cl.Message(
        content="Hello! How can I help you today?"
    ).send()  # Send welcome message


# Handler for incoming chat messages
@cl.on_message
async def handle_message(message: cl.Message):

    history = cl.user_session.get("history")  # Get chat history from session

    history.append(
        {"role": "user", "content": message.content}
    )  # Add user message to history

    result = await cl.make_async(Runner.run_sync)(agent, input=history)

    response_text = result.final_output
    await cl.Message(content=response_text).send()

    history.append({"role": "assistant", "content": response_text})
    cl.user_session.set("history", history)
