import streamlit as st
import json
from utils import MEMORY
from langchain_core.messages import AIMessage
from config import set_environment
from controlador import Controlador

set_environment()
controlador = Controlador()

#Archivo de configuración
CONFIG_FILE = "config.json"

#Cargar la configuración de colores del JSON
def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "background_color": "#2e302e",
            "text_color": "#FFFFFF",
            "sidebar_bg_color": "#057195",
            "sidebar_text_color": "#000000",
            "model_choice": "Google",
        }

#Cargar configuración de colores
config = load_config()

#Configuración de la página
st.set_page_config(page_title="Soporte: Arduino en parques", page_icon="\U0001F4DF")
st.title(config["user_page_title"])

#Aplica los colores
custom_style = f"""
    <style>
        .stApp {{
            background-color: {config["background_color"]};
            color: {config["text_color"]};
        }}
        .stSidebar {{
            background-color: {config["sidebar_bg_color"]};
            color: {config["sidebar_text_color"]};
        }}
    </style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

model_choice = {config["model_choice"]}

avatars = {
    "human": "user",    
    "ai": "assistant",  
    "system": "assistant" 
}

chat_container = st.container(height = 450)

input = st.chat_input(placeholder = config["input_placeholder"])

if input:
    controlador.generar_respuesta(input, model_choice)

with chat_container:
    if len(MEMORY.chat_memory.messages) == 0:
        mensaje_inicial = AIMessage(content = config["initial_message"])
        MEMORY.chat_memory.add_message(mensaje_inicial)

    for msg in MEMORY.chat_memory.messages:
        if msg.type in avatars and msg.content.strip():
            st.chat_message(avatars[msg.type]).write(msg.content)
