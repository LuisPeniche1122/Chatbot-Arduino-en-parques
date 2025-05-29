#config.py

import os
import streamlit as st

#Obtiene las API Keys del documento secrets.toml
def set_environment():
        os.environ["GOOGLE_API_KEY"] = st.secrets["API_KEY"]["GOOGLE_API_KEY"]
        os.environ["OPENAI_API_KEY"] = st.secrets["API_KEY"]["OPENAI_API_KEY"]
        
#Obtiene el directorio actual del archivo config.py
directorio_actual = os.path.dirname(__file__)

#Crea la ruta a la base de datos
RUTA_BD = os.path.join(directorio_actual, "bd")