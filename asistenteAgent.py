from os import getenv
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.tools.tavily_search import TavilySearchResults
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar el modelo de lenguaje GPT-4o con OpenRouter
llm = ChatOpenAI(
    openai_api_key=getenv("OPENROUTER_API_KEY"),
    openai_api_base=getenv("OPENROUTER_BASE_URL"),
    model_name="openai/gpt-4o",
    model_kwargs={
        "extra_headers": {
            "Helicone-Auth": f"Bearer " + getenv("HELICONE_API_KEY")
        }
    },
)

# Inicializar herramienta de búsqueda en internet
search_tool = TavilySearchResults(max_results=3)

# Cargar documentos de referencia (Ejemplo: RGPD y normativas fiscales)
urls = [
    "https://eur-lex.europa.eu/legal-content/ES/TXT/HTML/?uri=CELEX:32016R0679",  # RGPD
    "https://www.boe.es/buscar/act.php?id=BOE-A-2007-20555",  # Ley de Consumidores y Usuarios
    "https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2023.html"  # Normativa fiscal
]

loader = WebBaseLoader(web_paths=urls)
docs = loader.load()

# Dividir los documentos en fragmentos
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(docs)

# Crear embeddings con Hugging Face
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Crear base de datos vectorial con Chroma
vectorstore = Chroma(embedding_function=embeddings)
vectorstore.add_documents(splits)

# Función principal del chatbot (RAG + Búsqueda en internet)
def chatbot(message, history):
    relevant_docs = vectorstore.similarity_search(message)
    if relevant_docs:
        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])
        final_prompt = (
            "Eres un asistente experto en asesoría legal y financiera. "
            "Utiliza el siguiente contexto para responder de forma breve y precisa. "
            "Si no encuentras la información en la base de datos, responde solo 'No tengo información suficiente'.\n\n"
            "Si la pregunta no es sobre temas legales o financieros, responde 'La pregunta no entra en mi campo de conocimiento'.\n\n"
            f"Contexto:\n{context_text}\n\n"
            f"Pregunta: {message}\n"
            "Respuesta:"
        )
        response = llm.invoke(final_prompt)
        response_text = response.content if response and hasattr(response, 'content') else ""
        
        if "No tengo información suficiente" in response_text or not response_text.strip():
            search_results = search_tool.run(message)
            structured_response = "No encontré información en la base de datos. Aquí tienes información relevante de la web:\n\n"
            for result in search_results:
                structured_response += f"🔹 **Fuente:** [{result['url']}]({result['url']})\n📌 **Resumen:** {result['content']}\n\n"
            return structured_response
        
        return response_text
    
    # Si no hay información en RAG, buscar en internet
    search_results = search_tool.run(message)
    structured_response = "No encontré información en la base de datos. Aquí tienes información relevante de la web:\n\n"
    for result in search_results:
        structured_response += f"🔹 **Fuente:** [{result['url']}]({result['url']})\n📌 **Resumen:** {result['content']}\n\n"
    return structured_response

# Interfaz de Gradio
demo = gr.ChatInterface(
    chatbot,
    chatbot=gr.Chatbot(height=400, type="messages"),
    textbox=gr.Textbox(placeholder="Escribe tu consulta legal o financiera aquí...", container=False, scale=7),
    title="Asesor Legal y Financiero AI",
    description="Chatbot basado en RAG para responder preguntas sobre normativas legales y fiscales. Si no encuentra la información, buscará en internet.",
    theme="ocean",
    examples=[
        "¿Cuáles son las obligaciones fiscales de una empresa en España?",
        "Explícame los derechos del consumidor en un contrato de servicio.",
        "¿Cuáles son las obligaciones de un delegado de protección de datos?"
    ],
    type="messages",
    editable=True,
    save_history=True,
)

if __name__ == "__main__":
    demo.queue().launch()
