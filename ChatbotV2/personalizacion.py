import streamlit as st
import json

#st.set_page_config(page_title="Ajustes de administrador", page_icon="🦜")
st.title("Seccion de personalización de la página principal")

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "background_color": "#FFFFFF",
            "text_color": "#000000",
            "sidebar_bg_color": "#F0F0F0",
            "sidebar_text_color": "#333333",
        }

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

def seleccionar_menu(menu):
        if st.session_state.menu == menu:
            st.session_state.menu = None
        else:
            st.session_state.menu = menu

sidebar = st.sidebar
with sidebar:

    config = load_config()
    
    st.sidebar.subheader("🎨 Personalización de colores")
    
    background_color = st.sidebar.color_picker("Color de fondo", config["background_color"])
    text_color = st.sidebar.color_picker("Color del texto", config["text_color"])
    sidebar_bg_color = st.sidebar.color_picker("Color de fondo del Sidebar", config["sidebar_bg_color"])
    sidebar_text_color = st.sidebar.color_picker("Color del texto del Sidebar", config["sidebar_text_color"])
    
    if st.sidebar.button("Guardar cambios"):
        new_config = {
            "background_color": background_color,
            "text_color": text_color,
            "sidebar_bg_color": sidebar_bg_color,
            "sidebar_text_color": sidebar_text_color,
            "model_choice": "Google",
        }
        save_config(new_config)
        st.sidebar.success("Colores guardados. Los cambios se reflejarán en la página principal.")

       

preview_tab, carga_imagenes_tab = st.tabs(["Vista previa", "Carga de imagenes"])

with preview_tab:

    mensajes_prueba = [
    {"type": "user", "content": "What is the weather like today?"},
    {"type": "ai", "content": "The weather is sunny with a slight chance of rain."},
    {"type": "user", "content": "Thanks! That helps a lot."}
    ]
    page_container = st.container(height = 700)

    with page_container:
        # Crear el contenedor para los mensajes
        st.container(height = 120, border = False)
        st.title("\U0001F4DFSoporte: Arduino en parques")
        chat_container = st.container(height=450)

        # Crear un campo de entrada de chat
        input = st.chat_input(placeholder="Give me 3 keywords for what you have right now")

        # Mostrar los 3 mensajes de prueba dentro del contenedor
        with chat_container:
            for msg in mensajes_prueba:
                if msg["content"].strip():
                    st.chat_message(msg["type"]).write(msg["content"])

    

with carga_imagenes_tab:
    st.header("A dog")

