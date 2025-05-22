#manejador_archivos.py

import os
import pathlib
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from chromadb.utils import embedding_functions
from manejador_bd import ManejadorBD
import tempfile

#Clase que maneja la carga, fragmentación y preparación de archivos
class ManejadorArchivos:
    #Diccionario que define qué cargador usar según la extensión del archivo
    EXTENSIONES_PERMITIDAS = {
        ".pdf": PyPDFLoader,
        ".txt": TextLoader,
        ".docx": Docx2txtLoader
    }

    def __init__(self):
        #Divide textos en fragmentos de 1000 caracteres con 200 de solapamiento
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        #Modelo de embeddings de Google para generar representaciones vectoriales
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        #Instancia para subir datos a la base de datos
        self.manejador_bd = ManejadorBD()

    #Función para cargar el archivo temporalmente y leer su contenido
    def cargar_documento(self, archivo):
        print("entra cargar documentos")

        #Se guarda el archivo en una ubicación temporal
        temp_dir = tempfile.TemporaryDirectory()
        temp_filepath = os.path.join(temp_dir.name, archivo.name)

        with open(temp_filepath, "wb") as f:
            f.write(archivo.getvalue())

        ext = pathlib.Path(temp_filepath).suffix  #Obtiene la extensión del archivo
        print(ext)

        loader = self.EXTENSIONES_PERMITIDAS.get(ext)  #Selecciona el cargador correspondiente
        print(loader)

        if not loader:
            print("extension no soportada")

        loaded = loader(temp_filepath)  #Crea la instancia del cargador
        docs = loaded.load()  #Carga el contenido del archivo

        if not docs:
           print("No se han cargado documentos válidos.")

        print("se cargaron los documentos")
        print()
        return docs

    #Divide el documento en fragmentos manejables
    def dividir_documento(self, documento):
        fragmentos = self.splitter.split_documents(documento)
        print("Fragmentos generados")
        print()
        return fragmentos

    #Genera un vector (embedding) por cada fragmento de texto
    def generar_embeddings(self, fragmentos):
        embeddings = []
        for fragmento in fragmentos:
            embedding = self.embedding_model.embed_query(fragmento.page_content)
            embeddings.append(embedding)
        
        print("se han generado los emebbedings")
        print()
        return embeddings
    
    #Prepara los datos en el formato correcto para subirlos a la base de datos
    def preparar_archivo(self, nombre_archivo, fragmentos, embeddings):
        resultados = []
        cant_fragmentos = 0

        for fragmento, embedding in zip(fragmentos, embeddings):
            cant_fragmentos += 1
            id_unico = f"{nombre_archivo}_{cant_fragmentos}"  #ID única por fragmento
            resultados.append({
                "id": id_unico,  #ID del fragmento
                "texto": fragmento.page_content,  #Contenido del texto
                "metadatos": {
                    **fragmento.metadata,
                    "source": nombre_archivo  #Fuente: nombre del archivo original
                },
                "embedding": embedding  #Vector generado para este fragmento
            })

        print("se ha preparado el archivo para subir")
        print()
        return resultados

    #Ejecuta todo el flujo: cargar archivo, dividir, generar embeddings y subir a la BD
    def subir_archivo(self, archivo):
        print(archivo.name)

        #Paso 1: Cargar el archivo
        documento = self.cargar_documento(archivo)

        #Paso 2: Dividir en fragmentos
        fragmentos = self.dividir_documento(documento)

        #Paso 3: Generar embeddings
        embeddings = self.generar_embeddings(fragmentos)

        #Paso 4: Preparar datos para la base
        resultados = self.preparar_archivo(archivo.name, fragmentos, embeddings)

        #Paso 5: Subir a la base de datos
        self.manejador_bd.subir_documento(resultados)
