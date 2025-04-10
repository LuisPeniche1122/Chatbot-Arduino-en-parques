import streamlit as st

#if "password_entered" not in st.session_state:
#    st.session_state.password_entered = False

#if not st.session_state.password_entered:
#    password_input = st.text_input("Ingrese la contraseña", type="password")
#    stored_password = st.secrets["ADMIN_PAGE"]["password"]

#    if stored_password is None:
#        st.error("Error: La contraseña no está configurada en secrets.toml")
#    elif password_input == stored_password:
#        st.session_state.password_entered = True
#        st.success("Acceso concedido")
#    elif password_input:
#        st.error("Contraseña incorrecta")

# Si el usuario ingresó la contraseña, permitir personalización
#if st.session_state.password_entered:

# Definir las páginas disponibles
pg = st.navigation([st.Page("pruebas_archivos.py", title="Pruebas y subida de archivos", icon="📁"),
st.Page("personalizacion.py", title="Personalización", icon="🎨"),
st.Page("historial_chats.py", title="Historial de chats", icon="🗃"),
])

# Ejecutar la página seleccionada
pg.run()
