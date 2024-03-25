import streamlit as st
import os
from groq import Groq
import random

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import SystemMessagePromptTemplate, PromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate 

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

         
 

client = Groq(
    api_key= "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" )




class PersonalityChatBot(ChatBot):
    def __init__(self, personality):
        super().__init__(personality)
        self.set_trainer(ChatterBotCorpusTrainer)

        if personality == 'Friendly':
            self.train("chatterbot.corpus.english.greetings",
                       "chatterbot.corpus.english.conversations.greetings_and_farewells")
        elif personality == 'Professional':
            self.train("chatterbot.corpus.english.conversations.work")
        else:
            raise ValueError("Invalid personality type")

def reset_chat(chatbot):
    chatbot.storage.drop()

if __name__ == "__main__":
    personality = input("Enter the personality of the chatbot (Friendly or Professional): ")
    chatbot = PersonalityChatBot(personality)

    print("Hi, I'm your chatbot with the personality: " + personality)

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'reset':
            reset_chat(chatbot)
            print("Chatbot has been reset.")
            continue
        response = chatbot.get_response(user_input)
        print("Chatbot: " + str(response))