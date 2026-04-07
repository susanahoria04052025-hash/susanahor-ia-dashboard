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
# --- DISEÑO UI CORPORATIVO (ESTILO APPLE / CLEAN) ---
# Usamos CSS inyectado para crear el fondo de puntos y ajustar los colores
estilo_apple = """
<style>
    /* Forzar fondo blanco y patrón de puntos sutil */
    .stApp {
        background-color: #FAFAFC;
        background-image: radial-gradient(#D1D1D6 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    /* Cambiar el color de fondo del menú lateral (Sidebar) a un blanco sólido */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E5EA;
    }

    /* Estilo para los títulos y letras (Modo Claro) */
    h1, h2, h3, p, span, div {
        color: #1C1C1E !important; /* Gris súper oscuro casi negro estilo Apple */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* Estilizar las cajas métricas para que parezcan tarjetas modernas */
    [data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E5EA;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    /* Estilizar botones para que tengan tu color verde o bordes redondeados */
    .stButton>button {
        background-color: #00C853; /* Verde Biosaludable */
        color: white !important;
        border-radius: 12px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #009624;
        transform: scale(1.02);
    }
</style>
"""
# Aplicamos el estilo
st.markdown(estilo_apple, unsafe_allow_html=True)
# ----------------------------------------------------
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
    
    # --- BOTÓN DE DIAGNÓSTICO SECRETO PARA EL CTO ---
    with st.expander("🛠️ Herramientas de CTO (Clic para abrir)"):
        if st.button("🔍 Diagnosticar Modelos Disponibles"):
            with st.spinner("Preguntándole a Google..."):
                try:
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    modelos = []
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            modelos.append(m.name)
                    st.success("✅ Conexión exitosa. Modelos que Google autoriza para tu llave:")
                    st.write(modelos)
                except Exception as e:
                    st.error(f"Error al verificar la llave: {e}")
    # ------------------------------------------------

    idea = st.text_area("¿De qué trata el video?", placeholder="Ej: Alquilamos un caballo para la historia de Saulo de Tarso...")
    
    if st.button("🌟 Generar Paquete SEO"):
        if idea:
            with st.spinner("Despertando al cerebro de Gemini... consultando el algoritmo..."):
                try:
                    # 1. Conectando
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    
                    # 2. Seleccionando el modelo base más seguro garantizado por Google
                    modelo_ia = genai.GenerativeModel('gemini-2.5-flash') 
                    
                    # 3. El Prompt Mágico 
                    instruccion_cto = f"""
                    Eres el CTO y Manager de contenido del canal de YouTube 'SUSANAHORIA'. 
                    Este es un canal familiar donde una niña de 10 años (Susana) explora la naturaleza, su granja, reflexiones de vida y valores cristianos, de forma sana y aventurera.
                    
                    Mi idea para el video es: {idea}
                    
                    Tu trabajo es generarme lo siguiente optimizado para SEO:
                    1. TRES (3) OPCIONES DE TÍTULOS (Atractivos y aptos para familia).
                    2. DESCRIPCIÓN OPTIMIZADA.
                    3. LISTA DE 15 TAGS separados por comas.
                    """
                    
                    # 4. Generando contenido
                    respuesta_ia = modelo_ia.generate_content(instruccion_cto)
                    
                    # 5. Mostrando
                    st.success("¡Análisis SEO completado! 🎯")
                    st.markdown("---")
                    st.write(respuesta_ia.text)
                    
                except Exception as e:
                    st.error(f"El error persiste. Detalle exacto para diagnóstico: {e}")
        else:
            st.warning("¡Oye! Tienes que escribirme la idea primero. ✍️")

# ==========================================
# --- MÓDULO 3: CHAT CTO INTERNO ---
# ==========================================
elif modulo == "Chat IA":
    st.subheader("🤖 Consultor CTO IA (Próximamente Chat Dinámico)")
    st.chat_message("assistant").write("¡Hola equipo! Soy su CTO virtual. Aún me están construyendo este módulo para poder hablar fluido con ustedes, ¡pero el SEO ya está funcionando!")
