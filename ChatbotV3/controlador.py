#controlador.py

from manejador_archivos import ManejadorArchivos
from logica_chat import LogicaChat
from manejador_bd import ManejadorBD

#Clase que actúa como intermediario entre la interfaz y la lógica del programa
class Controlador:
    def __init__(self):
        #Inicializa los manejadores de archivos, lógica del chat y base de datos
        self.manejador_archivos = ManejadorArchivos()
        self.logica_chat = LogicaChat()
        self.manejador_bd = ManejadorBD()

    def cargar_documento(self, archivo):
        self.manejador_archivos.subir_archivo(archivo)

    def eliminar_documento(self, nombre):
        self.manejador_bd.eliminar_documento_por_nombre(nombre)

    def generar_respuesta(self, entrada_usuario, modelo_elegido, memoria):
        self.logica_chat.generar_respuesta(entrada_usuario, modelo_elegido, memoria)

    def obtener_extensiones_permitidas(self):
        return self.manejador_archivos.EXTENSIONES_PERMITIDAS.keys()


