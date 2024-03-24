import streamlit as st
import os
from groq import Groq
import random

# ... (other imports and functions)

def main():
    # ... (code before user_question)

    if user_question:
        # Initialize Groq Langchain chat object and conversation
        groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {
            "role": "system",
            "content": prompt
            },
            # Set a user message for the assistant to respond to.
            {
            "role": "user",
            "content": user_question,
            }],
            model_name=model
        )

        conversation = ConversationChain(
            llm=groq_chat,
            memory=memory
        )

        try:
            response = conversation(user_question)
            st.write("Chatbot:", response)
        except Exception as e:
            st.write("An error occurred while processing your request:", str(e))

if __name__ == "__main__":
    main()