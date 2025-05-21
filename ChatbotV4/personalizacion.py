#personalizacion.py

import streamlit as st
import json
import time

#Título principal de la sección
st.title("Sección de personalización de la página principal")

#Ubicación del archivo donde se guarda la configuración personalizada
CONFIG_FILE = "config.json"

#Cargar configuración desde el archivo JSON
def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        #Si no existe el archivo, se retorna una configuración por defecto
        return {
            "background_color": "#FFFFFF",
            "text_color": "#000000",
            "sidebar_bg_color": "#F0F0F0",
            "sidebar_text_color": "#333333",
        }

#Guardar configuración al archivo JSON
def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

#Alternar selección de menú en la sesión
def seleccionar_menu(menu):
    if st.session_state.menu == menu:
        st.session_state.menu = None
    else:
        st.session_state.menu = menu

#Contenido de la barra lateral
sidebar = st.sidebar
with sidebar:
    config = load_config()

    st.subheader("🎨 Personalización de colores")

    #Selectores de color para personalización
    background_color = st.color_picker("Color de fondo", config["background_color"])
    text_color = st.color_picker("Color del texto", config["text_color"])
    

    #Botón para guardar la configuración de colores
    if st.button("Guardar cambios"):
        config["background_color"] = background_color
        config["text_color"] = text_color

        save_config(config)
        exito = st.success("Cambios guardados correctamente, estos se reflejarán en la página principal.")
        time.sleep(3)
        exito.empty()

#Crear pestañas: una para vista previa y otra para ajustes generales
preview_tab, ajustes_tab = st.tabs(["Vista previa", "Ajustes generales"])

# Pestaña de vista previa: simulación de la página principal
with preview_tab:
    st.subheader("Vista previa simulada")

    with st.container():
        st.markdown(
            f"""
            <div style="
                background-color: {background_color};
                color: {text_color};
                padding: 40px;
                border-radius: 10px;
                border: 1px solid #ccc;
            ">
                <h2 style="margin-top: 0;">{config.get("user_page_title", "Título de la página")}</h2>
                <p>{config.get("initial_message", "Mensaje inicial de bienvenida...")}</p>
                <input 
                    type="text" 
                    placeholder="{config.get("input_placeholder", "Escribe aquí...")}" 
                    style="
                        padding: 10px;
                        font-size: 16px;
                        width: 100%;
                        margin-top: 20px;
                        border-radius: 5px;
                        border: 1px solid #aaa;
                    "
                />
            </div>
            """,
            unsafe_allow_html=True
        )

#Pestaña de ajustes generales
with ajustes_tab:
    #Inputs para modificar valores textuales visibles en la página principal
    input_placeholder = st.text_input("Placeholder del input de usuario", config["input_placeholder"])
    user_page_title = st.text_input("Título de la página", config["user_page_title"])
    initial_message = st.text_area("Texto del mensaje inicial", config["initial_message"])

    #Botón para guardar los ajustes generales
    if st.button("Guardar"):
        config["input_placeholder"] = input_placeholder
        config["user_page_title"] = user_page_title
        config["initial_message"] = initial_message

        save_config(config)
        mensaje_exito = st.success("Configuración guardada correctamente.")
        time.sleep(3)
        mensaje_exito.empty()
