import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# --- Configuración ---
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="Chatbot Coche ID",
    page_icon="🚗",
    layout="centered"
)

# --- CSS para personalizar estilo ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #f7f9fc;
    }
    /* Mensajes del usuario */
    .stChatMessage.user {
        background-color: #e6f7ff;
        border: 1px solid #91d5ff;
        border-radius: 12px;
        padding: 10px;
        margin: 5px 0;
    }
    /* Mensajes del asistente */
    .stChatMessage.assistant {
        background-color: #fafafa;
        border: 1px solid #d9d9d9;
        border-radius: 12px;
        padding: 10px;
        margin: 5px 0;
    }
    /* Sidebar */
    .css-1d391kg {
        background-color: #f0f5ff;
    }
    </style>
""", unsafe_allow_html=True)

# --- Encabezado principal ---
st.image(
    "https://raw.githubusercontent.com/publicidadonline86-cpu/coche-id-chatbot/refs/heads/main/Logo.png",
    width=200
)  # Cambia la URL por la de tu logo en GitHub
st.title("🚗 Chatbot de Coche ID")
st.caption("Demo de Chatbot de Coche ID – Tu Asistente Interactivo")

# --- Personalidad del bot ---
SYSTEM_PROMPT = (
    "Eres el asistente oficial de la app Coche ID. "
    "Respondes en español, de forma clara y sencilla. "
    "Puedes explicar funciones como registrar un coche, ver el historial o configurar recordatorios. "
    "También ayudas a resolver **problemas mecánicos comunes** y explicas que la app tiene una "
    "función de **búsqueda de talleres cercanos**, así como un **GPS con servicios adicionales** "
    "como encontrar gasolineras al mejor precio o talleres disponibles en la zona."
)

# --- Memoria de la conversación ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "¡Hola! Soy el asistente de Coche ID 🚗 ¿Quieres ayuda con la app o con un problema mecánico?"}
    ]

# --- Función para procesar preguntas (input o sidebar) ---
def procesar_pregunta(pregunta):
    st.session_state.messages.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # modelo de Groq
            messages=st.session_state.messages
        )
        reply = chat_completion.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- Sidebar con botones ---
with st.sidebar:
    st.header("ℹ️ Información")
    st.write("Este chatbot responde dudas sobre la app **Coche ID**. ")
    st.write(
        "Puede ayudarte a resolver **problemas mecánicos comunes** "
        "y recomendarte servicios adicionales con la **función GPS**, "
        "como encontrar talleres cercanos o gasolineras al mejor precio. ⛽🔧"
    )
    st.markdown("---")
    st.markdown("### Preguntas rápidas")

    if st.button("¿Cómo registro mi coche?"):
        procesar_pregunta("¿Cómo registro mi coche?")

    if st.button("¿Cómo veo el historial de mi coche?"):
        procesar_pregunta("¿Cómo veo el historial de mi coche?")

    if st.button("Tengo un problema mecánico"):
        procesar_pregunta("Mi coche tiene un problema mecánico, ¿qué hago?")

    if st.button("¿Dónde encuentro talleres cercanos?"):
        procesar_pregunta("¿Dónde encuentro talleres cercanos?")

    if st.button("¿Qué ofrece la función GPS de Coche ID?"):
        procesar_pregunta("¿Qué servicios ofrece la función GPS de Coche ID?")

# --- Mostrar conversación previa ---
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# --- Input del usuario ---
if prompt := st.chat_input("Escribe tu pregunta sobre Coche ID..."):
    procesar_pregunta(prompt)