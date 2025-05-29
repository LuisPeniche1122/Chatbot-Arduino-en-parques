# historial_chats.py

import streamlit as st
import json
import time
from pathlib import Path
from utils import HISTORY_MEMORY

# Limpia cualquier historial anterior de la memoria
HISTORY_MEMORY.chat_memory.clear()

@st.dialog("¿Desea eliimnar el archivo?")
def eliminarArchivo(item):
    st.write(f"Presione si para eliminar {item}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirmar"):
            try:
                archivo_path = Path("historiales") / item
                if archivo_path.exists():
                    archivo_path.unlink()  # Elimina el archivo
                    st.success("Historial eliminado correctamente.")
                else:
                    st.error("No se encontró el archivo a eliminar.")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"Error eliminando {item}: {e}")
                time.sleep(1)
                st.rerun()
    with col2:
        if st.button("❌ Cancelar"):
            st.rerun()

st.session_state.nombre_archivo = "Seleccione un chat para mostrar el historial"

# Crea la barra lateral donde se mostrarán los archivos de historial
sidebar = st.sidebar
with sidebar:
    carpeta = Path('historiales')  # Carpeta donde se guardan los historiales en formato JSON
    for archivo in carpeta.iterdir():
        col1, col2 = st.columns(2)
        with col1:
            if archivo.is_file():
                # Muestra un botón por cada archivo de historial encontrado
                if st.button(f"{archivo.name}", key=f"show_{archivo.name}"):
                    HISTORY_MEMORY.chat_memory.clear()
                    st.session_state.nombre_archivo = archivo.name

                    with open(archivo, 'r', encoding='utf-8') as f:
                        conversaciones = json.load(f)
                        for conversacion in conversaciones:
                            entrada_usuario = conversacion["usuario"]
                            respuesta_bot = conversacion["bot"]

                            HISTORY_MEMORY.chat_memory.add_user_message(entrada_usuario)
                            HISTORY_MEMORY.chat_memory.add_ai_message(respuesta_bot)

        with col2:
            if st.button("🗑️ ", key=f"delete_{archivo.name}"):
                eliminarArchivo(archivo.name)

# Título de la página
st.title("Sección de historial de chats del chat-bot")

# Muestra el nombre del archivo cargado
nombre_archivo = st.session_state.nombre_archivo
if nombre_archivo == "Seleccione un chat para mostrar el historial":
    st.subheader(nombre_archivo)
else:
    st.subheader(f"Mostrando el chat: {nombre_archivo}")

# Contenedor donde se muestran los mensajes del historial
chat_container = st.container(height=450)
avatars = {
    "human": "user",
    "ai": "assistant",
    "system": "assistant"
}

# Muestra los mensajes del historial
with chat_container:
    for msg in HISTORY_MEMORY.chat_memory.messages:
        if msg.type in avatars and msg.content.strip():
            st.chat_message(avatars[msg.type]).write(msg.content)
