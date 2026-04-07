import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai  # <-- LIBRERÍA DE IA DE GOOGLE

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="SUSANAHOR IA - CTO Interno", page_icon="🥕", layout="wide")

# --- CONEXIÓN SEGURA CON YOUTUBE ---
# La app va a leer la llave secreta que guardaste en Settings > Secrets
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# !!! ID DEL CANAL DE SUSANAHORIA !!!
CANAL_ID = "UCbp_1QxjyzT8cG7_0jy4NUg" 

# --- INTERFAZ VISUAL PRINCIPAL ---
st.title("🥕 SUSANAHOR IA: Centro de Mando")
st.write("Bienvenido al sistema de análisis predictivo y SEO de nuestro canal.")

# Menú lateral izquierdo
st.sidebar.header("Módulos del Sistema")
modulo = st.sidebar.radio("Navegación:", ["Análisis de Vistas", "Generador de SEO", "Chat IA"])

# ==========================================
# --- MÓDULO 1: ANALÍTICAS ---
# ==========================================
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
                
                # Lógica de validación
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

# ==========================================
# --- MÓDULO 2: GENERADOR SEO CON IA ---
# ==========================================
elif modulo == "Generador de SEO":
    st.subheader("✨ Módulo de SEO Mágico (Con tecnología Gemini AI)")
    st.write("Escribe una idea cruda y nuestro CTO IA la convertirá en oro para el algoritmo.")
    
    idea = st.text_area("¿De qué trata el video?", placeholder="Ej: Fuimos al zoológico de Barranquilla y a Susana la persiguió un mono...")
    
    if st.button("🌟 Generar Paquete SEO"):
        if idea:
            with st.spinner("Despertando al cerebro de Gemini... consultando el algoritmo..."):
                try:
                    # 1. Conectando con la IA de Google usando tu clave secreta de Gemini
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    modelo_ia = genai.GenerativeModel('gemini-pro') 
                    
                    # 2. El Prompt Mágico (Instrucciones precisas para la IA)
                    instruccion_cto = f"""
                    Eres el CTO y Manager de contenido del canal de YouTube 'SUSANAHORIA'. 
                    Este es un canal familiar donde una niña de 10 años (Susana) explora la naturaleza, su granja, reflexiones de vida y valores cristianos, de forma sana y aventurera.
                    
                    Mi idea para el próximo video es: {idea}
                    
                    Tu trabajo es generarme lo siguiente optimizado para el algoritmo de YouTube (para atraer clics sin engañar):
                    
                    1. TRES (3) OPCIONES DE TÍTULOS: Que sean atractivos, que generen curiosidad, ideal para público familiar. Que no superen los 60 caracteres.
                    2. DESCRIPCIÓN OPTIMIZADA: Los primeros 2 renglones súper gancheros, luego un resumen, llamado a suscribirse y reflexiones de la naturaleza.
                    3. LISTA DE TAGS (Etiquetas): Dame 15 palabras clave, separadas por comas, combinando búsqueda larga (ej. "aventura en granja para niños") y corta (ej. "susanahoria").
                    """
                    
                    # 3. Enviando la petición a Gemini
                    respuesta_ia = modelo_ia.generate_content(instruccion_cto)
                    
                    # 4. Mostrando la respuesta en pantalla con estilo
                    st.success("¡Análisis SEO completado! 🎯")
                    st.markdown("---")
                    st.write(respuesta_ia.text)
                    
                except Exception as e:
                    st.error(f"Error de conexión con la mente maestra (Gemini): Verifica si guardaste tu llave en secrets. Detalle: {e}")
        else:
            st.warning("¡Oye! Tienes que escribirme la idea primero. ✍️")

# ==========================================
# --- MÓDULO 3: CHAT CTO INTERNO ---
# ==========================================
elif modulo == "Chat IA":
    st.subheader("🤖 Consultor CTO IA (Próximamente Chat Dinámico)")
    st.chat_message("assistant").write("¡Hola equipo! Soy su CTO virtual. Aún me están construyendo este módulo para poder hablar fluido con ustedes, ¡pero el SEO ya está funcionando!")
