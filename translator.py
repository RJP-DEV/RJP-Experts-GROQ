import os

from groq import Groq
import streamlit as st

from logger import logger
from languages import supported_languages
from text_to_speech import convert_text_to_mp3


# Get Groq API key
groq_api_key = st.secrets["key"]

    # Initialize Groq client
client = Groq(       
        api_key=groq_api_key
    )

def detect_source_language(text: str) -> str:
    """Detect the language of source text

    :type text: str
    :param text: Source text to detect language
    :rtype: str
    :returns: Detected language of source text
    """

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "You are a multi-language translator."},
            {
                "role": "user",
                "content": f"Which language is '{text}' written in? Explain in 1 word without punctuation.",
            },
        ],
        temperature=0,
    )

    source_language = response.choices[0].message.content.strip()

    if source_language.capitalize() not in list(supported_languages.keys())[1:]:
        st.error(f"Detected source language '{source_language}' is not supported!")
        st.stop()

    logger.debug(f"Detected source language: {source_language}")

    return source_language


def translate() -> None:
    """Translate text and write result to translation session state variable"""

    text = st.session_state.source_text
    source_language = st.session_state.source_lang
    target_language = st.session_state.target_lang

    logger.debug(f"Source text: {text}")
    logger.debug(f"Source language: {source_language}")
    logger.debug(f"Target language: {target_language}")

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "system",
                "content": "You are a multi-language translator.",
            },
            {
                "role": "user",
                "content": f"Translate the following {source_language} text to {target_language} without quotes: '{text}'",
            },
        ],
        temperature=0,
    )

    st.session_state.translation = (
        response.choices[0].message.content.strip().replace("'", "").replace('"', "")
    )

    logger.debug(f"Translation: {st.session_state.translation}")

    convert_text_to_mp3(st.session_state.translation, supported_languages[target_language])