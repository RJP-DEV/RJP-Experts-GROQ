import os

import gradio as gr
from groq import Groq

# Get Groq API key
groq_api_key = "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"

client = Groq(api_key=groq_api_key)

def autocomplete(text):  
    if text != "":
        response = client.chat.completions.create(
            model='gemma-7b-it',
            messages=[
                {
                    "role": "user", 
                    "content": text
                }],
            stream=True
            )
            
        partial_message = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                partial_message = partial_message + chunk.choices[0].delta.content
                yield partial_message
              
css = """
.generating {
    display: none
}
"""
# Create the Gradio interface with live updates
iface = gr.Interface(
    fn=autocomplete,
    inputs=gr.Textbox(lines=2,
                      placeholder="Hello 👋",
                      label="Input Sentence"),
    outputs=gr.Markdown(),
    title="Catch me if you can 🐰",
    description="Powered by Groq & Gemma",
    live=True,  # Set live to True for real-time feedback
    allow_flagging="never",  # Disable flagging
    css=css
)
iface.dependencies[0]['show_progress'] = "hidden"
iface.dependencies[2]['show_progress'] = "hidden"

# Launch the app
iface.launch()