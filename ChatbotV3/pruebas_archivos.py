#pruebas_archivos.py

import streamlit as st
from utils import TEST_MEMORY
from langchain_core.messages import AIMessage
from config import set_environment
from controlador import Controlador
import uuid
import time

#Configuración del entorno
set_environment()

#Instancia del controlador general de la app
controlador = Controlador()

#Obtener los nombres de documentos actualmente en la base de datos
documentos_actuales = controlador.manejador_bd.obtener_nombres_documentos()
print(documentos_actuales)

#Título de la página
st.title("Sección de pruebas del chat-bot")

#Configuración del sidebar
sidebar = st.sidebar
with sidebar:
    #Botón para limpiar la memoria del chat
    if st.sidebar.button("Clear message history"):
        TEST_MEMORY.chat_memory.clear()
        st.rerun()

    #Elegir el modelo con el que se quiere conversar
    model_choice = sidebar.radio(
        "Elige un modelo",
        options=["Google", "ChatGPT"],
        index=0
    )

    #Generar una clave única para manejar el estado del uploader
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = str(uuid.uuid4())

    #Carga de archivos
    uploaded_files = sidebar.file_uploader(
        label="Upload files",
        type=list(controlador.obtener_extensiones_permitidas()),
        accept_multiple_files=True,
        key=st.session_state.uploader_key,
    )

    #Procesar archivos subidos
    if uploaded_files:
        print("Se intenta subir un archivo")
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in documentos_actuales:
                try:
                    controlador.cargar_documento(uploaded_file)
                    st.sidebar.success(f"'{uploaded_file.name}' subido exitosamente!")
                    # Se genera una nueva clave para limpiar el uploader
                    st.session_state.uploader_key = str(uuid.uuid4())
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.sidebar.error(f"Error al subir '{uploaded_file.name}': {e}")
            else:
                st.sidebar.warning(f"'{uploaded_file.name}' ya existe en la base de datos.")

    #Eliminar documentos existentes
    if documentos_actuales:
        st.markdown("### Documentos actuales")
        for doc_name in documentos_actuales:
            if st.button(f"❌ {doc_name}", key=f"delete_{doc_name}"):
                try:
                    controlador.eliminar_documento(doc_name)
                    st.success(f"'{doc_name}' eliminado correctamente!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error eliminando '{doc_name}': {e}")

#Detener la app si no hay documentos
if not documentos_actuales:
    st.info("Please upload documents to continue.")
    st.stop()

#Avatares personalizados para los mensajes del chat
avatars = {
    "human": "user",
    "ai": "assistant",
    "system": "assistant"
}

#Contenedor para mostrar el historial de chat
chat_container = st.container(height=450)

#Entrada del usuario para el chatbot
input = st.chat_input(placeholder="Give me 3 keywords for what you have right now")

#Procesar entrada del usuario
if input:
    controlador.generar_respuesta(input, model_choice, TEST_MEMORY)

#Mostrar mensajes en el contenedor de chat
with chat_container:
    #Mostrar mensaje inicial si la conversación está vacía
    if len(TEST_MEMORY.chat_memory.messages) == 0:
        mensaje_inicial = AIMessage(content="Ask me anything!")
        TEST_MEMORY.chat_memory.add_message(mensaje_inicial)

    #Mostrar todos los mensajes con su respectivo avatar
    for msg in TEST_MEMORY.chat_memory.messages:
        if msg.type in avatars and msg.content.strip():
            st.chat_message(avatars[msg.type]).write(msg.content)
