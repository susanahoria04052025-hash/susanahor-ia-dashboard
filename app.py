import streamlit as st

# Configuración de la página web
st.set_page_config(page_title="SUSANAHOR IA - CTO Interno", page_icon="🥕", layout="wide")

# Título
st.title("🥕 SUSANAHOR IA: Centro de Mando")
st.write("Bienvenido al sistema de análisis predictivo y SEO de nuestro canal.")

# Menú lateral
st.sidebar.header("Módulos del Sistema")
modulo = st.sidebar.radio("Navegación:", ["Análisis de Vistas", "Generador de SEO", "Chat IA"])

# Pantallas según el módulo seleccionado
if modulo == "Análisis de Vistas":
    st.subheader("📊 Módulo de Analíticas")
    st.info("Aquí conectaremos los datos de YouTube v3 pronto.")

elif modulo == "Generador de SEO":
    st.subheader("✨ Módulo de SEO Mágico")
    idea = st.text_input("Ingresa de qué trata el próximo video:")
    if st.button("Generar Títulos"):
        st.success("Aquí Gemini nos dará 3 títulos virales basados en tu idea.")

elif modulo == "Chat IA":
    st.subheader("🤖 Consultor CTO IA")
    st.chat_message("assistant").write("¡Hola equipo! Soy su CTO. ¿En qué trabajaremos hoy?")
    st.chat_input("Escribe tu pregunta...")
