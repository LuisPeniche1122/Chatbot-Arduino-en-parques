# 🤖 ChatbotV4.5
ChatbotV3 es una aplicación desarrollada en Python que permite la interacción entre usuarios y un asistente conversacional inteligente, con interfaces diferenciadas para usuarios y administradores. Utiliza Streamlit para crear interfaces web simples y rápidas, y Langchain para gestionar flujos conversacionales complejos e integrar modelos de lenguaje avanzados.

### ⚙️ Instalación

Sigue estos pasos para instalar las dependencias necesarias y ejecutar el proyecto:

1. **Clona este repositorio**:

```bash
git clone https://github.com/tu_usuario/ChatbotV3.git
cd ChatbotV3
```
2. **Crea un entorno virtual (opcional pero recomendado):**

```bash
python -m venv venv
source venv/bin/activate  # En Linux/macOS
venv\Scripts\activate     # En Windows
```
3. **Instala las dependencias necesarias:**

```bash
pip install -r requirements.txt
```

### 🔐 Configuración de claves

Para que la aplicación funcione correctamente, es necesario crear una carpeta de configuración y un archivo con tus credenciales.

#### 1. Crea una carpeta llamada `.streamlit` en la raíz del proyecto:

```bash
mkdir .streamlit
```

#### 2. Dentro de esa carpeta, crea un archivo llamado secrets.toml:
```bash
secrets.toml
```

#### 3. Abre el archivo secrets.toml y pega el siguiente contenido, reemplazando con tus datos personales:
```bash
[ADMIN_PAGE]
user = "Tu Usuario"
password = "Tu Contraseña"

[API_KEY]
GOOGLE_API_KEY = "Tu API KEY de Google"
OPENAI_API_KEY = "Tu API KEY de GPT"
```
> 💡 **¡Importante!**  
> Este archivo es utilizado por Streamlit para manejar configuraciones sensibles como usuarios administradores y claves de API. Asegúrate de **no compartirlo públicamente**.
