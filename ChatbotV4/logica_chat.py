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

#Función que guarda automáticamente el historial del chat cada ciertos segundos (60)
def auto_guardado(session_id, memory, intervalo=60):
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
    with open(f"{carpeta}/{session_id}.json", "w", encoding="utf-8") as f:
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
            "ChatGPT 3.5 Turbo": ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)
        }
    
    def __init__(self):
        
        #Inicializa el modelo por defecto (Gemini de Google)
        self.modelo_chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        self.modelo_embeddings = "models/embedding-001"
        self.manejador_bd = ManejadorBD()

        #Prompt del chatbot, personalidad y forma de actuar del chat
        self.prompt_inicial = """
            Eres un asistente de IA. Responde de manera clara y concisa.
            Si no sabes algo, indícalo amablemente y no inventes respuestas.
        """

    #Función principal para generar respuestas a partir de la entrada del usuario
    def generar_respuesta(self, entrada_usuario, modelo_elegido, memory):
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

        self.modelo_chat = self.MODELOS_DISPONIBLES.get(modelo_elegido, ChatGoogleGenerativeAI(model="gemini-1.5-flash"))
        
        #Invoca el modelo con el prompt y obtiene la respuesta
        respuesta = self.modelo_chat.invoke(prompt_final)

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
