# Import necessary tools/libraries
import streamlit as st  # Imports Streamlit for making web apps
import random  # Imports random number generator
import time  # Imports time-related functions
import requests  # Imports tool for making web requests

# Set the title of our web app
st.title("Money Making Machine")


# Function to create random amount of money
def generate_money():
    return random.randint(1, 1000)  # Gives random number between 1 and 1000


# Create a section for generating money
st.subheader("Instant Cash Generator")
if st.button("Generate Money"):  # When user clicks the button
    st.write("Counting your money...")  # Show loading message
    time.sleep(5)  # Wait for 5 seconds
    amount = generate_money()  # Get random amount
    st.success(f"You made ${amount}!")  # Show success message with amount


# Function to get side hustle ideas from a server
def fetch_side_hustle():
    try:
        # Try to get data from local server
        response = requests.get("http://127.0.0.1:8000/side_hustles")
        if response.status_code == 200:  # If request successful
            hustles = response.json()  # Convert response to JSON
            return hustles["side_hustle"]  # Return the hustle idea
        else:
            return "Freelancing"  # Default response if server fails

    except:
        return "Something went wrong!"  # Error message if request fails


# Create a section for side hustle ideas
st.subheader("Side Hustle Ideas")
if st.button("Generate Hustle"):  # When user clicks button
    idea = fetch_side_hustle()  # Get a hustle idea
    st.success(idea)  # Show the idea


# Function to get money-related quotes from server
def fetch_money_quote():
    try:
        # Try to get quote from local server
        response = requests.get("http://127.0.0.1:8000/money_quotes")
        if response.status_code == 200:  # If request successful
            quotes = response.json()  # Convert response to JSON
            return quotes["money_quote"]  # Return the quote
        else:
            return "Money is the root of all evil!"  # Default quote if server fails
    except:
        return "Something went wrong!"  # Error message if request fails


# Create a section for motivation quotes
st.subheader("Money-Making Motivation")
if st.button("Get Inspired"):  # When user clicks button
    quote = fetch_money_quote()  # Get a quote
    st.info(quote)  # Show the quote
