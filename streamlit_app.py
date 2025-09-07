import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# Cargar clave secreta (desde .env en local o desde Secrets en la nube)
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Configuración de la página
st.set_page_config(page_title="Chatbot Coche ID", page_icon="🚗")
st.title("🚗 Chatbot de Coche ID")
st.caption("Demo del Chatbot que integrará Coche ID")

# Mensaje de sistema (personalidad del bot)
SYSTEM_PROMPT = (
    "Eres el asistente oficial de la app Coche ID. "
    "Respondes en español, de forma clara y sencilla. "
    "Puedes explicar funciones como registrar un coche, ver el historial o configurar recordatorios, además puedes resolver dudas de mecanica"
)

# Guardar mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "¡Hola! Soy el asistente de Coche ID. ¿En qué puedo ayudarte?"}
    ]

# Mostrar conversación anterior
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu pregunta sobre Coche ID..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Llamada al modelo de Groq
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # modelo de Groq (puedes cambiarlo)
            messages=st.session_state.messages
        )
        reply = chat_completion.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
