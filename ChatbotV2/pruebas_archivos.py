import streamlit as st
from utils import MEMORY
from langchain_core.messages import AIMessage
from config import set_environment
from controlador import Controlador
#configuración inicial
set_environment()

controlador = Controlador()

documentos_actuales = controlador.manejador_bd.obtener_nombres_documentos()
print(documentos_actuales)

#st.set_page_config(page_title="Ajustes de administrador", page_icon="🦜")
st.title("Seccion de pruebas del chat-bot")

#sidebar
sidebar = st.sidebar
with sidebar:
    #limpiar la memoria
    if st.sidebar.button("Clear message history"):
        MEMORY.chat_memory.clear()
        st.rerun()
    
    #elegir el modelo a utilizar
    model_choice = sidebar.radio(
    "Elige un modelo",
    options=["Google", "ChatGPT"],
    index = 0
    )

    # Subir archivos a la base de datos
    uploaded_files = sidebar.file_uploader(
        label="Upload files",
        type=list(controlador.obtener_extensiones_permitidas()),
        accept_multiple_files=True,
    )

    if uploaded_files:
        print("Se intenta subir un archivo")
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in documentos_actuales:
                try:
                    controlador.cargar_documento(uploaded_file)
                    st.sidebar.success(f"'{uploaded_file.name}' subido exitosamente!")
                except Exception as e:
                    st.sidebar.error(f"Error al subir '{uploaded_file.name}': {e}")
            else:
                st.sidebar.warning(f"'{uploaded_file.name}' ya existe en la base de datos.")

    # Mostrar documentos subidos
    if documentos_actuales:
        st.sidebar.markdown("### Documentos actuales")
        for doc_name in documentos_actuales:
            if st.sidebar.button(f"❌ {doc_name}", key=f"delete_{doc_name}"):
                try:
                    controlador.eliminar_documento(doc_name)
                    st.sidebar.success(f"'{doc_name}' eliminado correctamente!")
                    st.rerun()
                except Exception as e:
                    st.sidebar.error(f"Error eliminando '{doc_name}': {e}")

#Pagina principal
if not documentos_actuales:
    st.info("Please upload documents to continue.")
    st.stop()

avatars = {
    "human": "user",    
    "ai": "assistant",  
    "system": "assistant" 
}

#contenedor del chat
chat_container = st.container(height = 450)

#entgrada de texto
input = st.chat_input(placeholder="Give me 3 keywords for what you have right now")

if input:
    controlador.generar_respuesta(input, model_choice)

with chat_container:
    if len(MEMORY.chat_memory.messages) == 0:
        mensaje_inicial = AIMessage(content="Ask me anything!")
        MEMORY.chat_memory.add_message(mensaje_inicial)
    for msg in MEMORY.chat_memory.messages:
        if msg.type in avatars and msg.content.strip():
            st.chat_message(avatars[msg.type]).write(msg.content)