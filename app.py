import streamlit as st
from googleapiclient.discovery import build

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="SUSANAHOR IA - CTO Interno", page_icon="🥕", layout="wide")

# --- CONEXIÓN SEGURA CON YOUTUBE ---
# La app va a leer la llave secreta que guardaste en Settings > Secrets
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# !!! REEMPLAZA ESTO CON EL ID DEL CANAL DE SUSANAHORIA (Empieza por UC...) !!!
CANAL_ID = "UCbp_1QxjyzT8cG7_0jy4NUg" 

# --- INTERFAZ VISUAL ---
st.title("🥕 SUSANAHOR IA: Centro de Mando")
st.write("Bienvenido al sistema de análisis predictivo y SEO de nuestro canal.")

st.sidebar.header("Módulos del Sistema")
modulo = st.sidebar.radio("Navegación:", ["Análisis de Vistas", "Generador de SEO", "Chat IA"])

# --- MÓDULO 1: ANALÍTICAS ---
if modulo == "Análisis de Vistas":
    st.subheader("📊 Módulo de Analíticas Reales")
    st.write("Toca el botón para extraer los datos frescos directamente desde YouTube:")
    
    if st.button("🚀 Extraer Datos Ahora"):
        with st.spinner("Conectando con los servidores de YouTube..."):
            try:
                # Pidiendo datos a YouTube
                respuesta = youtube.channels().list(
                    part='snippet,statistics',
                    id=CANAL_ID
                ).execute()
                
                # --- NUEVA LÓGICA DE IA INTELIGENTE ---
                if 'items' not in respuesta:
                    st.warning(f"⚠️ YouTube aceptó la llave, pero dice que el ID '{CANAL_ID}' no existe o está oculto. Verifica el ID.")
                else:
                    # Extrayendo la información
                    canal = respuesta['items'][0]
                    stats = canal['statistics']
                    
                    # --- MAGIA VISUAL: TARJETAS DE MÉTRICAS ---
                    st.success("¡Datos obtenidos con éxito!")
                    st.markdown("### El Pulso del Canal Hoy")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric(label="👥 Suscriptores", value=stats['subscriberCount'])
                    col2.metric(label="👁️ Vistas Totales", value=stats['viewCount'])
                    col3.metric(label="🎬 Videos Subidos", value=stats['videoCount'])

            except Exception as e:
                st.error(f"Error interno del sistema: {e}")
