# personalizacion.py

import streamlit as st
import json
import time
from controlador_admin import Controlador_Admin

controlador = Controlador_Admin()

# Título principal de la sección
st.title("Sección de personalización de la página principal")

# Ubicación del archivo donde se guarda la configuración personalizada
CONFIG_FILE = "config.json"

# Cargar configuración desde el archivo JSON
def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Si no existe el archivo, se retorna una configuración por defecto
        return {
            "background_color": "#FFFFFF",
            "text_color": "#000000",
            "sidebar_bg_color": "#F0F0F0",
            "sidebar_text_color": "#333333",
            "model_choice": "Gemini 1.5 Flash"
        }

# Guardar configuración al archivo JSON
@st.dialog("¿Desea guardar esta configuración?")
def save_config(config):
    st.write(f"Presione si para confirmar")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirmar"):
            try:
                with open(CONFIG_FILE, "w") as file:
                    json.dump(config, file, indent=4)
                st.success(f"configuración guardada correctamente!")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"hubo un error al guardar la configuración: {e}")
                time.sleep(2)
                st.rerun()
    with col2:
        if st.button("❌ Cancelar"):
            st.rerun()

# Alternar selección de menú en la sesión
def seleccionar_menu(menu):
    if st.session_state.menu == menu:
        st.session_state.menu = None
    else:
        st.session_state.menu = menu

# Contenido de la barra lateral
sidebar = st.sidebar
with sidebar:
    config = load_config()

    st.subheader("🎨 Personalización de colores")

    # Selectores de color para personalización
    background_color = st.color_picker("Color de fondo", config["background_color"])
    text_color = st.color_picker("Color del texto", config["text_color"])

    # Botón para guardar la configuración de colores
    if st.button("Guardar cambios"):
        config["background_color"] = background_color
        config["text_color"] = text_color

        save_config(config)

# Crear pestañas
preview_tab, ajustes_tab, ajustes_modelo_tab = st.tabs(["Vista previa", "Ajustes generales", "Ajustes del Modelo"])

# Vista previa
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

# Ajustes generales
with ajustes_tab:
    input_placeholder = st.text_input("Placeholder del input de usuario", config["input_placeholder"])
    user_page_title = st.text_input("Título de la página", config["user_page_title"])
    initial_message = st.text_area("Texto del mensaje inicial", config["initial_message"])

    if st.button("Guardar", key="guardar_ajustes_generales"):
        config["input_placeholder"] = input_placeholder
        config["user_page_title"] = user_page_title
        config["initial_message"] = initial_message

        save_config(config)

# Ajustes del modelo
with ajustes_modelo_tab:
    prompt_inicial = st.text_area("Prompt que utiliza el modelo", config["prompt"])

    st.subheader("Selección del modelo de lenguaje que usa el chat bot")

    modelo_actual = config.get("model_choice", "gemini-1.5-flash")
    modelo_seleccionado = st.selectbox("Selecciona el modelo que usará la página del chat bot del usuario:", 
                                       controlador.obtener_modelos_disponibles(), index=0)

    if st.button("Guardar", key="guardar_modelo"):
        config["model_choice"] = modelo_seleccionado
        config["prompt"] = prompt_inicial
        save_config(config)
