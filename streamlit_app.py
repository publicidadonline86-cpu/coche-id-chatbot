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

# --- Encabezado principal ---
st.image(
    "https://raw.githubusercontent.com/TU-USUARIO/coche-id-chatbot/main/logo.png",
    width=120
)  # Cambia por tu logo en GitHub
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

# --- Inicializar memoria de la conversación ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "¡Hola! Soy el asistente de Coche ID 🚗 ¿Quieres ayuda con la app o con un problema mecánico?"}
    ]

# --- Función para mostrar mensajes en burbujas ---
def mostrar_mensaje(role, content):
    if role == "user":
        st.markdown(
            f"""
            <div style="
                background-color: #ff9800;
                color: #212121;
                border-radius: 16px;
                padding: 12px;
                margin: 8px 0;
                max-width: 75%;
                margin-left: auto;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.15);
            ">
                {content}
            </div>
            """,
            unsafe_allow_html=True
        )
    elif role == "assistant":
        st.markdown(
            f"""
            <div style="
                background-color: #1976d2;
                color: #ffffff;
                border-radius: 16px;
                padding: 12px;
                margin: 8px 0;
                max-width: 75%;
                margin-right: auto;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.15);
            ">
                {content}
            </div>
            """,
            unsafe_allow_html=True
        )

# --- Mostrar conversación previa ---
for msg in st.session_state.messages:
    if msg["role"] != "system":
        mostrar_mensaje(msg["role"], msg["content"])

# --- Función para procesar preguntas ---
def procesar_pregunta(pregunta):
    # Mostrar pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": pregunta})
    mostrar_mensaje("user", pregunta)

    # Llamada al modelo de Groq
    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )
        reply = chat_completion.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    # Mostrar respuesta del asistente
    st.session_state.messages.append({"role": "assistant", "content": reply})
    mostrar_mensaje("assistant", reply)

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

# --- Input del usuario ---
if prompt := st.chat_input("Escribe tu pregunta sobre Coche ID..."):
    procesar_pregunta(prompt)
