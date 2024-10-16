import os, json
from openai import AzureOpenAI 
import streamlit as st

# Load environment variables for Azure OpenAI
client = AzureOpenAI(
api_key="130839dcd720474387d55136b6dd6f45",
api_version="2024-08-01-preview",
azure_endpoint="https://reelhackathon.openai.azure.com"
)


# Function to generate event suggestions using Azure OpenAI's chat model
def get_event_suggestions(prompt):
    """Generates event suggestions based on user input."""
    # Define the system prompt to set the context for the assistant
    system_prompt = "You are an event planning assistant. Your role is to help users plan their events by providing suggestions for venues, activities, budgets, and logistics based on their preferences."

    # Create the chat completion request with the system and user prompts
    response = (client.chat.completions.create(
model="gpt-4o", # model = &quot;deployment_name&quot;.
messages=[
{"role": "system", "content": system_prompt},
{"role": "user", "content": prompt}
]
)
    # Use your deployment name
      
    )
    
    # Return the assistant's response
    print(response)
    if response.choices and len(response.choices) > 0:
            assistant_message = response.choices[0].message.content
    else:
            assistant_message = "No choices found in the response."
    return assistant_message



# Streamlit Layout for Event Planning Assistant
st.title("Event Planning Assistant")

# Sidebar for event details
with st.sidebar:
    st.header("Event Details")
    event_type = st.selectbox("Select Event Type", ['Corporate', 'Wedding', 'Birthday', 'Other'])
    event_goal = st.text_input("Event Goal", "e.g., Team Building, Celebration")
    budget = st.number_input("Budget ($)", min_value=0, value=1000)
    event_date = st.date_input("Event Date")
    
    # Generate suggestions when clicked
    if st.button("Get Event Suggestions"):
        prompt = f"Plan a {event_type} event with a budget of ${budget}. The goal is {event_goal}. The event date is {event_date}."
        event_suggestions = get_event_suggestions(prompt)
        st.write(event_suggestions)

# Chat-like interface for interacting with the event assistant
st.header("Event Planner Chat")
user_input = st.text_input("Enter your question or request")

if user_input:
    st.write(f"**You:** {user_input}")
    response = get_event_suggestions(user_input)
    st.write(f"**Assistant:** {response}")
