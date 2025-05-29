#app_user.py
from config import set_environment

#Configura el entorno necesario
set_environment()

import streamlit as st
import json
from utils import create_memory_with_id
from langchain_core.messages import AIMessage
from controlador_user import Controlador_User
from logica_chat import auto_guardado

#Si no hay sesión iniciada, se crea una nueva memoria de conversación
if "session_id" not in st.session_state:
    MEMORY_ID, MEMORY = create_memory_with_id()
    st.session_state.session_id = MEMORY_ID
    st.session_state.memory = MEMORY
else:
    #Si ya existe una sesión, se recupera la memoria existente
    MEMORY = st.session_state.memory
    MEMORY_ID = st.session_state.session_id

#Guarda automáticamente la conversación actual
auto_guardado(MEMORY_ID, MEMORY)

#Se crea una instancia del controlador de chat
controlador = Controlador_User()

# Determina el archivo de configuración
CONFIG_FILE = "config.json"

#Función para cargar la configuración desde un archivo JSON
def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        #Si no se encuentra el archivo, se usan valores por defecto
        return {
            "background_color": "#2e302e",
            "text_color": "#FFFFFF",
            "sidebar_bg_color": "#057195",
            "sidebar_text_color": "#000000",
            "model_choice": "Google",
        }

#Cargar la configuración visual
config = load_config()

#Configuración del la pestaña de la página
st.set_page_config(page_title="Soporte: Arduino en parques", page_icon="\U0001F4DF")
st.title(config["user_page_title"])

#Aplicar colores personalizados a la app
custom_style = f"""
    <style>
        .stApp {{
            background-color: {config["background_color"]};
            color: {config["text_color"]};
        }}
    </style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

#Modelo de lenguaje seleccionado en la configuración
model_choice = config["model_choice"]

#Diccionario que define los avatares para cada tipo de mensaje
avatars = {
    "human": "user",
    "ai": "assistant",
    "system": "assistant"
}

#Contenedor donde se mostrará el chat
chat_container = st.container(height=450)

#Entrada de texto del usuario
input = st.chat_input(placeholder=config["input_placeholder"])

#Si el usuario envía algo, se genera una respuesta
if input:
    controlador.generar_respuesta(input, MEMORY)

#Mostrar mensajes dentro del contenedor de chat
with chat_container:
    #Si es la primera vez, se agrega un mensaje inicial del asistente
    if len(MEMORY.chat_memory.messages) == 0:
        mensaje_inicial = AIMessage(content=config["initial_message"])
        MEMORY.chat_memory.add_message(mensaje_inicial)

    #Mostrar todos los mensajes del historial
    for msg in MEMORY.chat_memory.messages:
        if msg.type in avatars and msg.content.strip():
            st.chat_message(avatars[msg.type]).write(msg.content)
