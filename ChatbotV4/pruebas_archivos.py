#pruebas_archivos.py

import streamlit as st
from utils import TEST_MEMORY
from langchain_core.messages import AIMessage
from controlador import Controlador
import uuid
import time

#Instancia del controlador general de la app
controlador = Controlador()

#Obtener los nombres de documentos actualmente en la base de datos
documentos_actuales = controlador.manejador_bd.obtener_nombres_documentos()
print(documentos_actuales)

#Título de la página
st.title("Sección de pruebas del chat-bot")

@st.dialog(" ")
def imprimirMensaje(item):
    st.write(item)
    if st.button("Ok"):
        st.rerun()

@st.dialog("¿Desea eliimnar el archivo?")
def eliminarArchivo(item):
    st.write(f"Presione si para eliminar {item}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirmar"):
            try:
                controlador.eliminar_documento(item)
                st.success(f"{item} eliminado correctamente!")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Error eliminando {item}: {e}")
                time.sleep(2)
                st.rerun()
    with col2:
        if st.button("❌ Cancelar"):
            st.rerun()

#Configuración del sidebar
sidebar = st.sidebar
with sidebar:
    #Botón para limpiar la memoria del chat
    if st.sidebar.button("Borrar historial de mensajes"):
        TEST_MEMORY.chat_memory.clear()
        st.rerun()

    #Elegir el modelo con el que se quiere conversar
    model_choice = sidebar.radio(
        "Elige un modelo",
        options = controlador.obtener_modelos_disponibles(),
        index=0
    )

    #Generar una clave única para manejar el estado del uploader
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = str(uuid.uuid4())

    #Carga de archivos
    uploaded_files = sidebar.file_uploader(
        label="Subir archivos",
        type=list(controlador.obtener_extensiones_permitidas()),
        accept_multiple_files=True,
        key=st.session_state.uploader_key,
    )

    #Procesar archivos subidos
    if uploaded_files:
        print("Se intenta subir un archivo")
        for uploaded_file in uploaded_files:
            try:
                if uploaded_file.name not in documentos_actuales:
                    controlador.cargar_documento(uploaded_file)
                    
                    # Se genera una nueva clave para limpiar el uploader
                    st.session_state.uploader_key = str(uuid.uuid4())
                    imprimirMensaje(f"{uploaded_file.name} subido exitosamente!")
                else:
                    st.session_state.uploader_key = str(uuid.uuid4())
                    imprimirMensaje(f"{uploaded_file.name} ya existe en la base de datos.")
            except Exception as e:
                st.session_state.uploader_key = str(uuid.uuid4())
                imprimirMensaje(f"Error al subir {uploaded_file.name}: {e}")
                

        # Eliminar documentos existentes con confirmación
    if documentos_actuales:
        st.markdown("### Documentos actuales")
        for doc_name in documentos_actuales:
            if st.button(f"❌ {doc_name}"):
                eliminarArchivo(doc_name)


#Detener la app si no hay documentos
if not documentos_actuales:
    st.info("Por favor, cargue documentos para continuar.")
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
input = st.chat_input(placeholder="Hazme una pregunta para probar los archivos")

#Procesar entrada del usuario
if input:
    try:
        controlador.generar_respuesta(input, model_choice, TEST_MEMORY)
    except Exception as e:
        imprimirMensaje(str(e))

#Mostrar mensajes en el contenedor de chat
with chat_container:
    #Mostrar mensaje inicial si la conversación está vacía
    if len(TEST_MEMORY.chat_memory.messages) == 0:
        mensaje_inicial = AIMessage(content="Pregúntame algo para probar los archivos!")
        TEST_MEMORY.chat_memory.add_message(mensaje_inicial)

    #Mostrar todos los mensajes con su respectivo avatar
    for msg in TEST_MEMORY.chat_memory.messages:
        if msg.type in avatars and msg.content.strip():
            st.chat_message(avatars[msg.type]).write(msg.content)
