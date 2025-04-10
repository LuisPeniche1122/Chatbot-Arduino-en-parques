import streamlit as st
import json
import time

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
        json.dump(config, file, indent = 4)

def seleccionar_menu(menu):
        if st.session_state.menu == menu:
            st.session_state.menu = None
        else:
            st.session_state.menu = menu

sidebar = st.sidebar
with sidebar:

    config = load_config()
    
    st.subheader("🎨 Personalización de colores")
    
    background_color = st.color_picker("Color de fondo", config["background_color"])
    text_color = st.color_picker("Color del texto", config["text_color"])
    sidebar_bg_color = st.color_picker("Color de fondo del Sidebar", config["sidebar_bg_color"])
    sidebar_text_color = st.color_picker("Color del texto del Sidebar", config["sidebar_text_color"])
    
    if st.button("Guardar cambios"):
        config["background_color"] = background_color
        config["text_color"] = text_color
        config["sidebar_bg_color"] = sidebar_bg_color
        config["sidebar_text_color"] = sidebar_text_color

        save_config(config)
        exito = st.success("CAmbios guardados correctamente, estos se reflejarán en la página principal.")
        time.sleep(3)
        exito.empty()


preview_tab, ajustes_tab = st.tabs(["Vista previa", "Ajustes generales"])

with preview_tab:
    url = "http://156.67.221.86:8502"  # Cambia esto por la URL que quieras mostrar
    st.components.v1.iframe(url, width=900, height=600)


    

with ajustes_tab:
    input_placeholder = st.text_input("Placeholder del input de usuario", config["input_placeholder"])
    user_page_title = st.text_input("Título de la página", config["user_page_title"])
    initial_message = st.text_area("Texto del mensaje inicial", config["initial_message"])

    # Botón para guardar cambios
    if st.button("Guardar"):
        config["input_placeholder"] = input_placeholder
        config["user_page_title"] = user_page_title
        config["initial_message"] = initial_message

        save_config(config)
        mensaje_exito = st.success("Configuración guardada correctamente.")
        time.sleep(3)
        mensaje_exito.empty()


