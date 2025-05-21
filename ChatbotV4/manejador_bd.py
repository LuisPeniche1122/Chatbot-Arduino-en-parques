#manejador_bd.py

import chromadb
from config import RUTA_BD
from langchain_google_genai import GoogleGenerativeAIEmbeddings

#Clase que maneja la base de datos de embeddings y documentos
class ManejadorBD:
    def __init__(self):
        #Cliente persistente que guarda la BD en disco
        self.cliente_chroma = chromadb.PersistentClient(path=RUTA_BD)
        #Colección donde se almacenan los documentos
        self.base_datos = self.cliente_chroma.get_or_create_collection("documentos")
        #Modelo de embeddings para convertir texto a vectores
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    #Subir documentos a la base de datos
    def subir_documento(self, documentos):
        print(len(documentos))
        for doc in documentos:
            print("se ha subido correctamente el documento")
            self.base_datos.add(
                ids=[doc["id"]],             #ID única por fragmento
                embeddings=[doc["embedding"]],  #Vector del contenido
                documents=[doc["texto"]],       #Texto del fragmento
                metadatas=[doc["metadatos"]]    #Metadatos (incluye nombre del archivo original)
            )

    #Eliminar todos los fragmentos relacionados con un archivo por su nombre
    def eliminar_documento_por_nombre(self, nombre_documento):
        resultados = self.base_datos.get()
        ids_a_eliminar = []
        for metadatos, doc_id in zip(resultados.get("metadatas", []), resultados.get("ids", [])):
            if metadatos and metadatos.get("source") == nombre_documento:
                ids_a_eliminar.append(doc_id)
        
        if ids_a_eliminar:
            self.base_datos.delete(ids=ids_a_eliminar)

    #Buscar fragmentos relevantes en la base de datos a partir de una consulta (query)
    def obtener_documentos_relevantes(self, query, n_resultados=5):
        #Convertir la consulta en un vector de embedding
        query_embedding = self.embedding_model.embed_query(query)

        #Buscar los fragmentos más cercanos (similares) al vector de la consulta
        resultados = self.base_datos.query(
            query_embeddings=[query_embedding],
            n_results=n_resultados
        )

        #Formatear los resultados encontrados
        documentos_relevantes = []
        for documento, metadata in zip(resultados["documents"], resultados["metadatas"]):
            documentos_relevantes.append({"documento": documento, "metadatos": metadata})
        
        print("se han obtenido los documentos relevantes")
        print()
        return documentos_relevantes

    #Obtener la lista de nombres de archivos que han sido subidos a la BD
    def obtener_nombres_documentos(self):
        resultados = self.base_datos.get()
        nombres_documentos = set()
        for metadatos in resultados.get("metadatas", []):
            if metadatos and "source" in metadatos:
                nombres_documentos.add(metadatos["source"])
        return list(nombres_documentos)
