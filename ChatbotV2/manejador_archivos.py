# manejador_archivos.py

import os
import pathlib

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from chromadb.utils import embedding_functions
from manejador_bd import ManejadorBD
import tempfile


class ManejadorArchivos:
    EXTENSIONES_PERMITIDAS = {
        ".pdf": PyPDFLoader,
        ".txt": TextLoader,
        ".docx": UnstructuredWordDocumentLoader
        }

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.manejador_bd = ManejadorBD()

    def cargar_documento(self, archivo):
        print("entra cargar documentos")

        temp_dir = tempfile.TemporaryDirectory()
        temp_filepath = os.path.join(temp_dir.name, archivo.name)

        with open(temp_filepath, "wb") as f:
            f.write(archivo.getvalue())

        ext = pathlib.Path(temp_filepath).suffix

        print(ext)

        loader = self.EXTENSIONES_PERMITIDAS.get(ext)

        print(loader)

        if not loader:
            print("extension no soportada")

        loaded = loader(temp_filepath)

        docs = loaded.load()

        if not docs:
           print("No se han cargado documentos válidos.")

        print("se cargaron los documentos")
        print()
        return docs

    def dividir_documento(self, documento):
        fragmentos = self.splitter.split_documents(documento)
        print("Fragmentos generados")
        print()
        return fragmentos

    def generar_embeddings(self, fragmentos):
        embeddings = []
        for fragmento in fragmentos:
            embedding = self.embedding_model.embed_query(fragmento.page_content)
            embeddings.append(embedding)
            
        print("se han generado los emebbedings")
        print()
        return embeddings
    
    def preparar_archivo(self, nombre_archivo, fragmentos, embeddings):
        resultados = []

        cant_fragmentos = 0

        for fragmento, embedding in zip(fragmentos, embeddings):
            cant_fragmentos += 1
            id_unico = f"{nombre_archivo}_{cant_fragmentos}"
            resultados.append({
            "id": id_unico,  # La ID va fuera de los metadatos
            "texto": fragmento.page_content,  # Contenido del fragmento
            "metadatos": {
                **fragmento.metadata,  # Agregar metadatos existentes del fragmento
                "source": nombre_archivo  # Agregar el nombre del archivo como fuente
                },
            "embedding": embedding  # Incluir el embedding
            })
        
        print("se ha preparado el archivo para subir")
        print()

        return resultados


    def subir_archivo(self, archivo):
        print(archivo.name)
        # Paso 1: Cargar el archivo
        documento = self.cargar_documento(archivo)

        # Paso 2: Dividir el documento en fragmentos
        fragmentos = self.dividir_documento(documento)

        # Paso 3: Generar embeddings para cada fragmento
        embeddings = self.generar_embeddings(fragmentos)

        # paso 4: preparar los fragmentos con sus embeddings e ids para subbir a la bd
        resultados = self.preparar_archivo(archivo.name, fragmentos, embeddings)

        self.manejador_bd.subir_documento(resultados)

        
