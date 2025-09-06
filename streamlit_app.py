import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# Cargar clave secreta desde .env (en local) o desde Secrets (en la nube)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuración de la página
st.set_page_config(page_title="Chatbot Coche ID", page_icon="🚗")
st.title("🚗 Chatbot de Coche ID")
st.caption("Demo interactiva para el TFM de Pepe")

# Mensaje de sistema (personalidad del bot)
SYSTEM_PROMPT = (
    "Eres el asistente oficial de la app Coche ID. "
    "Respondes en español, de forma clara y sencilla. "
    "Puedes explicar funciones como registrar un coche, ver el historial o configurar recordatorios."
)

# Guardar mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "¡Hola! Soy el asistente de Coche ID. ¿En qué te ayudo?"}
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
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})