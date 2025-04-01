# logica_chat.py

from manejador_bd import ManejadorBD
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from utils import MEMORY

class LogicaChat:
    def __init__(self):
        self.modelo_chat = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
        self.modelo_embeddings = "models/embedding-001"
        self.manejador_bd = ManejadorBD()
        self.prompt_inicial = """
            Eres un asistente de IA. Responde de manera clara y concisa.
            Si no sabes algo, indícalo amablemente y no inventes respuestas.
        """

    def limpiar_memoria(self):
        MEMORY.clear()

    def generar_respuesta(self, entrada_usuario, modelo_elegido):
        print("entra generar respuesta")
        print(entrada_usuario)
        print()

        documentos = self.manejador_bd.obtener_documentos_relevantes(entrada_usuario)
        
        # Prompt con roles explícitos
        prompt = ChatPromptTemplate.from_messages([
            AIMessage(content=self.prompt_inicial),
            HumanMessage(content=f"Entrada: {entrada_usuario}\nDocumentos: {documentos}")
        ])

        prompt_final = prompt.format_messages()

        # **Imprimir mensajes en la memoria antes de invocar el modelo**
        print("Mensajes en memoria antes de la respuesta:")
        for msg in MEMORY.chat_memory.messages:
            print(f"{msg.type.upper()}: {msg.content}")
        print()

        if(modelo_elegido == "Google"):
            self.modelo_chat = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

        if(modelo_elegido == "ChatGPT"):
            self.modelo_chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)
        
        respuesta = self.modelo_chat.invoke(prompt_final)

        print("respuesta:-----------------------------------")
        print(respuesta)
        print("\n")
        MEMORY.chat_memory.add_user_message(entrada_usuario)
        print("se añadió el input del usuario")
        MEMORY.chat_memory.add_ai_message(respuesta.content)
        print("se añadió la respuesta de la IA")

