import streamlit as st  # Import Streamlit for creating the web-based UI
import random  # Import random for generating random choices
import string  # Import string to use predefined character sets


# Function to generate a random password
def generate_password(length, use_digits, use_special):
    characters = string.ascii_letters  # Includes uppercase and lowercase letters

    if use_digits:
        characters += string.digits  # Adds numbers (0-9) if selected

    if use_special:
        characters += (
            string.punctuation
        )  # Adds special characters (!@#$%^&* etc.) if selected

    # Generate a password by randomly selecting characters based on the length provided
    return "".join(random.choice(characters) for _ in range(length))


# Streamlit UI setup
st.title("Simple Password Generator")  # Display the app title on the web page

# User input: password length (slider to select length between 6 and 32 characters)
length = st.slider("Select password length:", min_value=6, max_value=32, value=12)

# Checkbox options for including numbers and special characters in the password
use_digits = st.checkbox("Include numbers")  # Checkbox for numbers (0-9)
use_special = st.checkbox(
    "Include special characters"
)  # Checkbox for special characters (!@#$%^&*)

# Button to generate password
if st.button("Generate Password"):
    password = generate_password(
        length, use_digits, use_special
    )  # Call the password generation function
    st.write(f"Generated Password: `{password}`")  # Display the generated password
