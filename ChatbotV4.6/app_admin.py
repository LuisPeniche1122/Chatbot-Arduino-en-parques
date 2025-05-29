import streamlit as st
from config import set_environment
from utils import HISTORY_MEMORY

set_environment()

# Verifica si existe la clave en el estado
if "password_entered" not in st.session_state:
    st.session_state.password_entered = False

# Si ya se ingresó la contraseña correctamente, se cargan las páginas del admin
if st.session_state.password_entered:
    pg = st.navigation([
        st.Page("pruebas_archivos.py", title="Pruebas y subida de archivos", icon="📁"),
        st.Page("personalizacion.py", title="Personalización", icon="🎨"),
        st.Page("historial_chats.py", title="Historial de chats", icon="🕘"),
    ])
    pg.run()

else:
    # Solo mostramos el input si aún no se ha ingresado
    password_input = st.text_input("Ingrese la contraseña", type="password")
    stored_password = st.secrets["ADMIN_PAGE"]["password"]

    if not stored_password:
        st.error("Error: La contraseña no está configurada en secrets.toml")
    elif password_input == stored_password:
        st.session_state.password_entered = True
        st.success("Acceso concedido")
        st.rerun()
    elif password_input:
        st.error("Contraseña incorrecta")
