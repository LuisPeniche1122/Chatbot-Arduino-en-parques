#app_admin.py

import streamlit as st
from utils import HISTORY_MEMORY
from config import set_environment

set_environment()

#Verifica si existe una contraseña
if "password_entered" not in st.session_state:
    st.session_state.password_entered = False  #Si no existe, se inicializa como False

#Si no se ha ingresado la contraseña aún
if not st.session_state.password_entered:
    #Muestra un campo de entrada para la contraseña
    password_input = st.text_input("Ingrese la contraseña", type="password")
    stored_password = st.secrets["ADMIN_PAGE"]["password"]  #Obtiene la contraseña desde el archivo de configuración 'secrets.toml'

    if stored_password is None:
        st.error("Error: La contraseña no está configurada en secrets.toml")  #Muestra un error si no hay contraseña configurada
    elif password_input == stored_password:
        st.session_state.password_entered = True  #Si la contraseña es correcta, se actualiza el estado
        st.success("Acceso concedido")
    elif password_input:
        st.error("Contraseña incorrecta")

#Si la contraseña fue ingresada correctamente, se permite el acceso a las páginas del administrador
if st.session_state.password_entered:

    #Páginas disponibles para navegación
    pg = st.navigation([
        st.Page("pruebas_archivos.py", title="Pruebas y subida de archivos", icon="📁"),
        st.Page("personalizacion.py", title="Personalización", icon="🎨"),
        st.Page("historial_chats.py", title="Historial de chats", icon="🗃"),
    ])

    #Ejecuta la página seleccionada
    pg.run()

