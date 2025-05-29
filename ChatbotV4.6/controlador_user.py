#controlador.py

from manejador_archivos import ManejadorArchivos
from logica_chat import LogicaChat
from manejador_bd import ManejadorBD

#Clase que actúa como intermediario entre la interfaz y la lógica del programa
class Controlador_User:
    def __init__(self):
        #Inicializa los manejadores de archivos, lógica del chat y base de datos
        self.manejador_archivos = ManejadorArchivos()
        self.logica_chat = LogicaChat()
        self.manejador_bd = ManejadorBD()

    def generar_respuesta(self, entrada_usuario, memoria):
        self.logica_chat.generar_respuesta_user(entrada_usuario, memoria)
