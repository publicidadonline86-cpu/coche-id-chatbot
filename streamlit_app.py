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

# --- CSS para botones del sidebar en azul ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] button {
        background-color: #1976d2 !important;
        color: #ffffff !important;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 6px 12px;
        margin: 4px 0;
    }
    [data-testid="stSidebar"] button:hover {
        background-color: #0d47a1 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] button * {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Encabezado principal ---
st.image(
    "https://raw.githubusercontent.com/publicidadonline86-cpu/coche-id-chatbot/refs/heads/main/Logo.pn",
    width=220
)
st.title("🚗 Chatbot de Coche ID")
st.caption("Demo de Chatbot de Coche ID – Tu Asistente Interactivo")

# --- Respuestas predefinidas para mecánica ---
RESPUESTAS_MECANICAS = {
    "no arranca": "🔧 Si tu coche no arranca:\n\n- Revisa la batería (puede estar descargada).\n- Comprueba que tienes combustible suficiente.\n- Verifica que no haya luces extrañas en el tablero.\n\n👉 En la app Coche ID, con la función **GPS**, puedes localizar talleres cercanos que te ayuden rápidamente.",
    "batería descargada": "🔋 Si la batería está descargada:\n\n- Intenta arrancar con pinzas y otra batería.\n- Si no funciona, necesitarás cambiarla.\n\n👉 Con la app Coche ID puedes buscar talleres en tu zona para asistencia inmediata.",
    "pinchazo": "🛞 Si has tenido un pinchazo:\n\n- Coloca el coche en un lugar seguro y señaliza.\n- Cambia la rueda por la de repuesto si sabes hacerlo.\n- Si no, usa la app Coche ID para encontrar un taller o servicio de grúa cercano.",
    "ruidos extraños": "🔊 Si escuchas ruidos extraños:\n\n- Pueden ser frenos, suspensión o motor.\n- No sigas conduciendo mucho sin revisarlo.\n\n👉 Usa la función **GPS de Coche ID** para localizar un taller y recibir ayuda.",
    "luz tablero": "⚠️ Si se enciende una luz en el tablero:\n\n- Consulta el manual de tu coche para identificarla.\n- Puede ser algo menor (ej. presión de neumáticos) o más grave (motor, aceite).\n\n👉 La app Coche ID puede guiarte para encontrar el taller adecuado en tu zona."
}

# --- Personalidad del bot ---
SYSTEM_PROMPT = (
    "Eres el asistente oficial de la app Coche ID. "
    "Respondes en español, de forma clara y sencilla. "
    "Puedes explicar funciones como registrar un coche, ver el historial o configurar recordatorios. "
    "También ayudas a resolver **problemas mecánicos comunes** con consejos prácticos y "
    "explicas que la app tiene una función de **búsqueda de talleres cercanos** y un **GPS con servicios adicionales** "
    "como encontrar gasolineras al mejor precio."
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
    st.session_state.messages.append({"role": "user", "content": pregunta})
    mostrar_mensaje("user", pregunta)

    # --- Buscar si es una pregunta mecánica ---
    respuesta_predefinida = None
    for clave, respuesta in RESPUESTAS_MECANICAS.items():
        if clave in pregunta.lower():
            respuesta_predefinida = respuesta
            break

    if respuesta_predefinida:
        reply = respuesta_predefinida
    else:
        # --- Si no es mecánica, usar Groq ---
        try:
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages
            )
            reply = chat_completion.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    mostrar_mensaje("assistant", reply)

# --- Sidebar con botones ---
pregunta_sidebar = None

with st.sidebar:
    st.header("ℹ️ Información")
    st.write("Este chatbot responde dudas sobre la app **Coche ID**. ")
    st.write(
        "Puede ayudarte a resolver **problemas mecánicos comunes** "
        "y recomendarte servicios adicionales con la **función GPS**, "
        "como encontrar talleres cercanos o gasolineras al mejor precio. ⛽🔧"
    )
    st.markdown("---")
    st.markdown("### Preguntas rápidas – App")

    if st.button("¿Cómo registro mi coche?"):
        pregunta_sidebar = "¿Cómo registro mi coche?"

    if st.button("¿Cómo veo el historial de mi coche?"):
        pregunta_sidebar = "¿Cómo veo el historial de mi coche?"

    if st.button("¿Dónde encuentro talleres cercanos?"):
        pregunta_sidebar = "¿Dónde encuentro talleres cercanos?"

    if st.button("¿Qué ofrece la función GPS de Coche ID?"):
        pregunta_sidebar = "¿Qué servicios ofrece la función GPS de Coche ID?"

    st.markdown("---")
    st.markdown("### Preguntas rápidas – Mecánica")

    if st.button("El coche no arranca"):
        pregunta_sidebar = "Mi coche no arranca"

    if st.button("La batería está descargada"):
        pregunta_sidebar = "La batería está descargada"

    if st.button("Tengo un pinchazo"):
        pregunta_sidebar = "Tengo un pinchazo"

    if st.button("Hace ruidos extraños"):
        pregunta_sidebar = "Hace ruidos extraños"

    if st.button("Se enciende una luz en el tablero"):
        pregunta_sidebar = "Se encendió una luz en el tablero"

# --- Procesar pregunta del sidebar ---
if pregunta_sidebar:
    procesar_pregunta(pregunta_sidebar)

# --- Input del usuario ---
if prompt := st.chat_input("Escribe tu pregunta sobre Coche ID..."):
    procesar_pregunta(prompt)
