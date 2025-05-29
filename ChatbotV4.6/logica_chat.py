#logica_chat.py

from manejador_bd import ManejadorBD
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import time
import threading
import os
import json
from datetime import datetime

def load_config():
    CONFIG_FILE = "config.json"
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
            "model_choice": "Gemini 1.5 Flash",
            "prompt": "Eres un asistente de IA. Responde de manera clara y concisa.Si no sabes algo, indícalo amablemente y no inventes respuestas."
        }

#Función que guarda automáticamente el historial del chat cada ciertos segundos (60)
def auto_guardado(session_id, memory, intervalo=10):
    def guardar():
        while True:
            time.sleep(intervalo)
            if len(memory.chat_memory.messages) > 1:
                guardar_historial(session_id, memory)
    threading.Thread(target=guardar, daemon=True).start()

#Guarda el historial actual de la sesión en un archivo JSON
def guardar_historial(session_id, memoria):
    carpeta = "historiales"
    conversacion = convertir_memory_a_json(memoria)
    os.makedirs(carpeta, exist_ok=True)

    # Obtener la fecha actual en formato aaaa-mm-dd
    fecha_actual = datetime.now().strftime("%d-%m-%Y")

    # Construir el nombre del archivo
    nombre_archivo = f"{session_id}_{fecha_actual}.json"

    # Guardar el archivo
    with open(os.path.join(carpeta, nombre_archivo), "w", encoding="utf-8") as f:
        json.dump(conversacion, f, indent=4, ensure_ascii=False)

#Convierte la memoria del chat en una lista de diccionarios para guardar como JSON
def convertir_memory_a_json(memory):
    mensajes = memory.chat_memory.messages
    historial = []
    par = {}

    for msg in mensajes:
        if msg.type == "human":
            #Guarda el mensaje del usuario
            par = {
                "timestamp": msg.additional_kwargs["timestamp"],
                "usuario": msg.content,
                "bot": ""  
            }
        elif msg.type == "ai" and par:
            #Guarda la respuesta del bot asociada al mensaje del usuario
            par["bot"] = msg.content
            historial.append(par)
            par = {}  #Reinicia el par para la siguiente entrada

    return historial


#Clase que contiene la lógica para interactuar con el chatbot
class LogicaChat:
    MODELOS_DISPONIBLES = {
            "Gemini 1.5 Flash": ChatGoogleGenerativeAI(model="gemini-1.5-flash"),
            "Gemini 1.5 Pro": ChatGoogleGenerativeAI(model="gemini-1.5-pro"),
            "ChatGPT 3.5 Turbo": ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)
        }
    
    def __init__(self):
        config = load_config()
        nombre_modelo = config["model_choice"]
        self.modelo_chat_user = self.MODELOS_DISPONIBLES.get(nombre_modelo)
        self.modelo_chat_admin = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

        self.modelo_embeddings = "models/embedding-001"

        self.manejador_bd = ManejadorBD()

        #Prompt del chatbot, personalidad y forma de actuar del chat
        self.prompt_inicial = config["prompt"]

    def obtener_modelo(self, nombre_modelo):
        return self.MODELOS_DISPONIBLES.get(nombre_modelo)

    #Función principal para generar respuestas a partir de la entrada del usuario
    def generar_respuesta_admin(self, entrada_usuario, prompt_inicial, modelo_elegido, memory):
        print("entra generar respuesta")
        print(entrada_usuario)
        print()

        #Busca documentos relacionados con la entrada del usuario
        documentos = self.manejador_bd.obtener_documentos_relevantes(entrada_usuario)
        
        #Crea un prompt con el prompt del chatbot + entrada del usuario + documentos
        prompt = ChatPromptTemplate.from_messages([
            AIMessage(content=prompt_inicial),
            HumanMessage(content=f"Entrada: {entrada_usuario}\nDocumentos: {documentos}")
        ])
        prompt_final = prompt.format_messages()

        #Muestra en consola los mensajes actuales de la memoria (Uso en debug)
        print("Mensajes en memoria antes de la respuesta:")
        for msg in memory.chat_memory.messages:
            print(f"{msg.type.upper()}: {msg.content}")
        print()

        self.modelo_chat_admin = self.MODELOS_DISPONIBLES.get(modelo_elegido)
        
        #Invoca el modelo con el prompt y obtiene la respuesta
        respuesta = self.modelo_chat_admin.invoke(prompt_final)

        print("respuesta:-----------------------------------")
        print(respuesta)
        print("\n")

        #Guarda el mensaje del usuario en la memoria
        mensaje_usuario = HumanMessage(content=entrada_usuario, additional_kwargs={"timestamp": time.time()})
        memory.chat_memory.add_message(mensaje_usuario)
        print("se añadió el input del usuario")

        #Guarda la respuesta del bot en la memoria
        mensaje_bot = AIMessage(content=respuesta.content, additional_kwargs={"timestamp": time.time()})
        memory.chat_memory.add_message(mensaje_bot)
        print("se añadió la respuesta de la IA")

    def generar_respuesta_user(self, entrada_usuario, memory):
        print("entra generar respuesta")
        print(entrada_usuario)
        print()

        #Busca documentos relacionados con la entrada del usuario
        documentos = self.manejador_bd.obtener_documentos_relevantes(entrada_usuario)
        
        #Crea un prompt con el prompt del chatbot + entrada del usuario + documentos
        prompt = ChatPromptTemplate.from_messages([
            AIMessage(content=self.prompt_inicial),
            HumanMessage(content=f"Entrada: {entrada_usuario}\nDocumentos: {documentos}")
        ])
        prompt_final = prompt.format_messages()

        #Muestra en consola los mensajes actuales de la memoria (Uso en debug)
        print("Mensajes en memoria antes de la respuesta:")
        for msg in memory.chat_memory.messages:
            print(f"{msg.type.upper()}: {msg.content}")
        print()
        
        #Invoca el modelo con el prompt y obtiene la respuesta
        respuesta = self.modelo_chat_user.invoke(prompt_final)

        print("respuesta:-----------------------------------")
        print(respuesta)
        print("\n")

        #Guarda el mensaje del usuario en la memoria
        mensaje_usuario = HumanMessage(content=entrada_usuario, additional_kwargs={"timestamp": time.time()})
        memory.chat_memory.add_message(mensaje_usuario)
        print("se añadió el input del usuario")

        #Guarda la respuesta del bot en la memoria
        mensaje_bot = AIMessage(content=respuesta.content, additional_kwargs={"timestamp": time.time()})
        memory.chat_memory.add_message(mensaje_bot)
        print("se añadió la respuesta de la IA")
        
