#utils.py

import uuid
from langchain.memory import ConversationBufferMemory

#Inicializa una memoria de conversación
def init_test_memory():
    return ConversationBufferMemory(
        memory_key="test_memory",        #Clave para identificar esta memoria
        return_messages=True             #Retorna los mensajes completos, no solo el texto
    )

#Inicializa una memoria general para guardar historial
def init_history_memory():
    return ConversationBufferMemory(
        memory_key="history_memory",
        return_messages=True
    )

#Crea una nueva memoria única con un ID generado automáticamente
def create_memory_with_id():
    memory_id = str(uuid.uuid4())       #ID único para identificar la conversación
    memory = ConversationBufferMemory(
        memory_key=f"user_memory_{memory_id}",
        return_messages=True
    )
    return memory_id, memory            #Retorna el ID y la memoria correspondiente


#Constantes globales para memoria de uso inmediato
TEST_MEMORY = init_test_memory()
HISTORY_MEMORY = init_history_memory()