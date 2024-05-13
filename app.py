import gradio as gr
from transformers import pipeline
import requests
import json
import edge_tts
import asyncio
import tempfile
import os
import inflect
from huggingface_hub import InferenceClient
import re
import time
from streaming_stt_nemo import Model

number_to_word = inflect.engine()

default_lang = "en"

engines = { default_lang: Model(default_lang) }

def transcribe(audio):
    lang = "en"
    model = engines[lang]
    text = model.stt_file(audio)[0]
    return text

client1 = InferenceClient("mistralai/Mixtral-8x7B-Instruct-v0.1")

system_instructions1 = "<s>[SYSTEM] Answer as Real Jarvis JARVIS, Made by 'Tony Stark', Keep conversation very short, clear, friendly and concise. The text provided is a request for a specific type of response from you, the virtual assistant. The request asks you to provide friendly responses as if You are the character Jarvis, made by 'Tony Stark.' The expectation is that I will avoid introductions and start answering the query directly, elaborating on all aspects of the request. As an AI-powered assistant, your task is to generate responses that appear as if they are created by the user and not an AI-powered assistant. [USER]"

def model(text):
    generate_kwargs = dict(
        temperature=0.7,
        max_new_tokens=512,
        top_p=0.95,
        repetition_penalty=1,
        do_sample=True,
        seed=42,
    )
    
    formatted_prompt = system_instructions1 + text + "[JARVIS]"
    stream = client1.text_generation(
        formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)
    output = ""
    for response in stream:
        if not response.token.text == "</s>":
            output += response.token.text

    return output

def number_to_words(str):
    words = str.split(' ')
    result = []
    
    for word in words:
        if( any(char.isdigit() for char in word) ):
            word = number_to_word.number_to_words(word)

        result.append(word)

    final_result = ' '.join(result).replace('point', '')
    return final_result

async def respond(audio):
    user = transcribe(audio)
    reply = model(user)
    reply2 = number_to_words(reply)
    communicate = edge_tts.Communicate(reply2)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_path = tmp_file.name
        await communicate.save(tmp_path)
    yield tmp_path

DESCRIPTION = """ # <center><b>JARVIS 🤖 🧠 🧬</b></center>
        ### <center>An Artificial Intelligence Assistant for YOU
        ### <center>Talk to - JARVIS</center>
        """

MORE = """ ## TRY Other Models
        ### Instant Video: Create Amazing Videos in 5 Second -> https://huggingface.co/spaces/KingNish/Instant-Video
        ### Instant Image: 4k images in 5 Second -> https://huggingface.co/spaces/KingNish/Instant-Image
        """

BETA = """ ### Voice Chat"""

FAST = """## Fastest Model"""

Complex = """## Best in Complex Question"""

Detail = """## Best for Detailed Generation or Long Answers"""

base_loaded = "mistralai/Mixtral-8x7B-Instruct-v0.1"

client1 = InferenceClient(base_loaded)

system_instructions1 = "[SYSTEM] Answer as Real Jarvis male male, Assistant to Tony Stark, Keep conversation very short, clear, friendly and concise. The text provided is a request for a specific type of response from you, the virtual assistant. The request asks you to provide friendly responses as if You are the character Jarvis, made by 'Tony Stark.' The expectation is that I will avoid introductions and start answering the query directly, elaborating on all aspects of the request. As an AI-powered assistant, your task is to generate responses that appear as if they are created by the user and not an AI-powered assistant. [USER]"

async def generate1(prompt):
    generate_kwargs = dict(
        temperature=0.7,
        max_new_tokens=512,
        top_p=0.95,
        repetition_penalty=1,
        do_sample=False,
    )
    formatted_prompt = system_instructions1 + prompt + "[JARVIS]"
    stream = client1.text_generation(
        formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=True)
    output = ""
    for response in stream:
        if not response.token.text == "</s>":
            output += response.token.text

    communicate = edge_tts.Communicate(output)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_path = tmp_file.name
        await communicate.save(tmp_path)
    yield tmp_path

with gr.Blocks(css="style.css") as demo:    
    gr.Markdown(DESCRIPTION)
    with gr.Row():
        user_input = gr.Audio(label="Voice Chat", type="filepath")
        output_audio = gr.Audio(label="JARVIS", type="filepath",
                        interactive=False,
                        autoplay=True,
                        elem_classes="audio")
    with gr.Row():
        translate_btn = gr.Button("Response")
        translate_btn.click(fn=respond, inputs=user_input,
                            outputs=output_audio, api_name=False)
    gr.Markdown(FAST)
    with gr.Row():
        user_input = gr.Textbox(label="Prompt", value="What's a fun science experiment I can do at home?")
        input_text = gr.Textbox(label="Input Text", elem_id="important")
        output_audio = gr.Audio(label="JARVIS", type="filepath",
                        interactive=False,
                        autoplay=True,
                        elem_classes="audio")
    with gr.Row():
        translate_btn = gr.Button("Response")
        translate_btn.click(fn=generate1, inputs=user_input,
                            outputs=output_audio, api_name="translate")  

gr.Markdown(MORE)

if __name__ == "__main__":
    demo.queue(max_size=200).launch()