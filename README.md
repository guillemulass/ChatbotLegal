# Asistente Legal y Financiero - Chatbot con LangChain

## Descripción
Este proyecto implementa un chatbot basado en técnicas de **Procesamiento del Lenguaje Natural (PLN)** para responder consultas en el ámbito legal y financiero. Utiliza **RAG (Retrieval-Augmented Generation)** para mejorar la precisión de sus respuestas y puede realizar búsquedas en internet cuando la información no está en su base de datos.

## Tecnologías Utilizadas
- **Lenguaje**: Python
- **Modelo de Lenguaje**: `GPT-4o` (vía OpenRouter)
- **Framework de IA**: LangChain
- **Embeddings**: `sentence-transformers/all-mpnet-base-v2` (Hugging Face)
- **Base de Datos Vectorial**: Chroma
- **Carga de Documentos**: WebBaseLoader
- **Búsqueda Web**: TavilySearchResults
- **Interfaz**: Gradio

## Características del Chatbot
✅ Procesa preguntas en lenguaje natural.
✅ Utiliza documentos legales y fiscales como referencia.
✅ Realiza consultas en internet si la información no está disponible.
✅ Filtra consultas fuera del ámbito legal y financiero.
✅ Responde de manera precisa y estructurada.

## Instalación y Uso
### 1. Clonar el repositorio
```sh
git clone https://github.com/tu-usuario/asistente-legal-financiero.git
cd asistente-legal-financiero
```

### 2. Instalar dependencias
Se recomienda usar un entorno virtual:
```sh
pip install -r requirements.txt
```

### 3. Configurar las credenciales
Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
```env
OPENROUTER_API_KEY=tu_api_key
OPENROUTER_BASE_URL=https://openrouter.helicone.ai/api/v1
HELICONE_API_KEY=tu_api_key
TAVILY_API_KEY=tu_api_key
```

### 4. Ejecutar el chatbot
```sh
python asistenteAgent.py
```

## Estructura del Proyecto
```
├── asistenteAgent.py    # Código principal del chatbot
├── requirements.txt     # Dependencias del proyecto
├── README.md            # Documentación del repositorio
├── .env.example         # Ejemplo de configuración de variables de entorno
```

## Ejemplos de Uso
Algunas preguntas que puedes hacerle al chatbot:
- *¿Cuáles son las obligaciones fiscales de una empresa en España?*
- *Explícame los derechos del consumidor en un contrato de servicio.*
- *¿Cuáles son las obligaciones de un delegado de protección de datos?*

## Monitorización y Despliegue
- **Monitorización**: Soporte para Helicone, Langfuse o LangSmith.
- **Despliegue**: Compatible con Gradio, Streamlit y otras interfaces web.

## Contribuciones
Si deseas contribuir, por favor abre un **pull request** o crea un **issue** en el repositorio.

## Licencia
Este proyecto está licenciado bajo la **MIT License**.

