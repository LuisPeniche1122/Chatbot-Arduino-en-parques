# manejador_bd.py

import chromadb
from config import RUTA_BD
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class ManejadorBD:
    def __init__(self):
        self.cliente_chroma = chromadb.PersistentClient(path=RUTA_BD)
        self.base_datos = self.cliente_chroma.get_or_create_collection("documentos")
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    def subir_documento(self, documentos):
        print(len(documentos))
        for doc in documentos:
            print("se ha subido correctamente el documento")
            self.base_datos.add(
            ids=[doc["id"]],
            embeddings=[doc["embedding"]],
            documents=[doc["texto"]],
            metadatas=[doc["metadatos"]]
            )

    def eliminar_documento_por_nombre(self, nombre_documento):
        resultados = self.base_datos.get()
        ids_a_eliminar = []
        for metadatos, doc_id in zip(resultados.get("metadatas", []), resultados.get("ids", [])):
            if metadatos and metadatos.get("source") == nombre_documento:
                ids_a_eliminar.append(doc_id)
        
        if ids_a_eliminar:
            self.base_datos.delete(ids=ids_a_eliminar)

    def obtener_documentos_relevantes(self, query, n_resultados=5):
        query_embedding = self.embedding_model.embed_query(query)  # Convertir query a embedding
        resultados = self.base_datos.query(
            query_embeddings=[query_embedding],  # Usar embedding en la consulta
            n_results=n_resultados
        )
        documentos_relevantes = []
        for documento, metadata in zip(resultados["documents"], resultados["metadatas"]):
            documentos_relevantes.append({"documento": documento, "metadatos": metadata})
        
        print("se han obtenido los documentos relevantes")
        print()
        return documentos_relevantes
    
    def obtener_nombres_documentos(self):
        resultados = self.base_datos.get()
        nombres_documentos = set()
        for metadatos in resultados.get("metadatas", []):
            if metadatos and "source" in metadatos:
                nombres_documentos.add(metadatos["source"])
        return list(nombres_documentos)