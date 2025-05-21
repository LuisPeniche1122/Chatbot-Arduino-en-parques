#historial_chats.py

import streamlit as st
import json
from pathlib import Path
from utils import HISTORY_MEMORY

#Limpia cualquier historial anterior de la memoria
HISTORY_MEMORY.chat_memory.clear()

#Crea la barra lateral donde se mostrarán los archivos de historial
sidebar = st.sidebar
with sidebar:
    carpeta = Path('historiales')  #Carpeta donde se guardan los historiales en formato JSON
    history_container = st.container(height=720)  #Contenedor para mostrar la lista de chats
    nombre_archivo = "Seleccione un chat para mostrar el historial"  #Texto por defecto

    with history_container:
        #Recorre los archivos dentro de la carpeta de historiales
        for archivo in carpeta.iterdir():
            if archivo.is_file():
                #Muestra un botón por cada archivo de historial encontrado
                if st.button(f"{archivo.name}", key=f"show_{archivo}"):
                    HISTORY_MEMORY.chat_memory.clear()  #Limpia la memoria antes de cargar el nuevo historial
                    nombre_archivo = archivo.name  #Guarda el nombre del archivo seleccionado

                    #Abre el archivo y carga el historial del chat
                    with open(archivo, 'r', encoding='utf-8') as f:
                        conversaciones = json.load(f)

                        #Agrega cada mensaje al historial de la memoria
                        for conversacion in conversaciones:
                            entrada_usuario = conversacion["usuario"]
                            respuesta_bot = conversacion["bot"]

                            HISTORY_MEMORY.chat_memory.add_user_message(entrada_usuario)
                            HISTORY_MEMORY.chat_memory.add_ai_message(respuesta_bot)
                        f.close()

#Título de la página
st.title("Sección de historial de chats del chat-bot")

#Muestra el nombre del archivo cargado, o el mensaje por defecto
if nombre_archivo == "seleccione un chat para mostrar el historial":
    st.subheader(nombre_archivo)
else:
    st.subheader(f"Mostrando el chat: {nombre_archivo}")

#Contenedor donde se muestran los mensajes del historial
chat_container = st.container(height=450)

#Define qué avatar usar para cada tipo de mensaje
avatars = {
    "human": "user",
    "ai": "assistant",
    "system": "assistant"
}

#Muestra cada mensaje guardado en la memoria, con su avatar correspondiente
with chat_container:
    for msg in HISTORY_MEMORY.chat_memory.messages:
        if msg.type in avatars and msg.content.strip():
            st.chat_message(avatars[msg.type]).write(msg.content)
