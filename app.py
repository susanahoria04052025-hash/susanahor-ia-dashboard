import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai

# ==========================================
# 1. CONFIGURACIÓN INICIAL (Siempre va primero)
# ==========================================
st.set_page_config(page_title="SUSANAHOR IA - Centro de Mando", page_icon="🥕", layout="wide")

# ==========================================
# 2. BASE DE DATOS DEL EQUIPO (Diccionario)
# ==========================================
# Aquí creas los usuarios. El sistema diferenciará quién entra.
USUARIOS_EQUIPO = {
    "admin": "zanahoria2026*",
    "guionista": "guion123",
    "editor": "video123",
    "seo": "seo123",
    "produccion": "rodaje123"
}

# Inicializamos la "memoria" del navegador para saber si hay alguien dentro
if 'usuario_activo' not in st.session_state:
    st.session_state['usuario_activo'] = None

# ==========================================
# 3. DISEÑO CORPORATIVO (APPLE STYLE)
# ==========================================
estilo_apple = """
<style>
    .stApp {
        background-color: #FAFAFC;
        background-image: radial-gradient(#D1D1D6 1px, transparent 1px);
        background-size: 20px 20px;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E5EA;
    }
    h1, h2, h3, p, span, div {
        color: #1C1C1E !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    [data-testid="metric-container"] {
        background-color: #FFFFFF; border: 1px solid #E5E5EA; padding: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .stButton>button {
        background-color: #00C853; color: white !important; border-radius: 12px; border: none; padding: 10px 24px; font-weight: 600; transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #009624; transform: scale(1.02); }
    
    /* Diseño específico para la caja de Login flotante */
    .caja-login {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 40px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        border: 1px solid #E5E5EA; text-align: center;
        backdrop-filter: blur(10px);
    }
</style>
"""
st.markdown(estilo_apple, unsafe_allow_html=True)

# ==========================================
# 4. PANTALLA DE LOGIN (La Puerta de Entrada)
# ==========================================
def pantalla_login():
    st.markdown("<br><br><br>", unsafe_allow_html=True) # Espacio para centrar
    
    # Usamos columnas para que la caja de login quede al centro
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<div class='caja-login'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🥕</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Acceso al Sistema</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8E8E93 !important;'>Ingresa tus credenciales del equipo</p>", unsafe_allow_html=True)
        
        usuario_input = st.text_input("Usuario")
        # El type='password' activa automáticamente el TouchID/FaceID del dispositivo para autocompletar
        password_input = st.text_input("Contraseña", type="password") 
        
        if st.button("🚀 Ingresar al Centro de Mando", use_container_width=True):
            # Validamos contra nuestra pequeña "Base de Datos" de arriba
            if usuario_input in USUARIOS_EQUIPO and USUARIOS_EQUIPO[usuario_input] == password_input:
                st.session_state['usuario_activo'] = usuario_input
                st.rerun() # Recarga la app y le quita el seguro
            else:
                st.error("Credenciales incorrectas. Intenta de nuevo.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. EL NÚCLEO DE LA APLICACIÓN (Si pasa la puerta)
# ==========================================
def aplicacion_principal():
    YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    CANAL_ID = "UCbp_1QxjyzT8cG7_0jy4NUg" 

    st.title("🥕 SUSANAHOR IA: Centro de Mando")
    st.write(f"Bienvenido de nuevo, **{st.session_state['usuario_activo'].upper()}**.") # Saluda al usuario!

    # Menú lateral
    st.sidebar.markdown("### Perfil")
    st.sidebar.info(f"Conectado como:\n**{st.session_state['usuario_activo']}**")
    
    if st.sidebar.button("🔒 Cerrar Sesión"):
        st.session_state['usuario_activo'] = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("Módulos del Sistema")
    modulo = st.sidebar.radio("Navegación:", ["Análisis de Vistas", "Generador de SEO", "Chat IA"])

    # --- MÓDULO 1: ANALÍTICAS ---
    if modulo == "Análisis de Vistas":
        st.subheader("📊 Módulo de Analíticas Reales")
        st.write("Toca el botón para extraer los datos frescos directamente desde YouTube:")
        
        if st.button("🚀 Extraer Datos Ahora"):
            with st.spinner("Conectando con YouTube..."):
                try:
                    respuesta = youtube.channels().list(part='snippet,statistics', id=CANAL_ID).execute()
                    if 'items' in respuesta:
                        stats = respuesta['items'][0]['statistics']
                        st.success("¡Datos obtenidos con éxito!")
                        col1, col2, col3 = st.columns(3)
                        col1.metric(label="👥 Suscriptores", value=stats['subscriberCount'])
                        col2.metric(label="👁️ Vistas Totales", value=stats['viewCount'])
                        col3.metric(label="🎬 Videos Subidos", value=stats['videoCount'])
                except Exception as e:
                    st.error(f"Error interno del sistema: {e}")

    # --- MÓDULO 2: GENERADOR SEO CON IA ---
    elif modulo == "Generador de SEO":
        st.subheader("✨ Módulo de SEO Mágico (Con tecnología Gemini AI)")
        st.write("Escribe una idea cruda y nuestro CTO IA la convertirá en oro para el algoritmo.")
        
        idea = st.text_area("¿De qué trata el video?", placeholder="Ej: Alquilamos un caballo para la historia de Saulo...")
        
        if st.button("🌟 Generar Paquete SEO"):
            if idea:
                with st.spinner("Despertando al cerebro de Gemini..."):
                    try:
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        modelo_ia = genai.GenerativeModel('gemini-2.5-flash') 
                        
                        instruccion_cto = f"""Eres el CTO y Manager de contenido del canal de YouTube 'SUSANAHORIA'. Este es un canal familiar donde una niña de 10 años (Susana) explora la naturaleza, su granja, reflexiones de vida y valores cristianos, de forma sana y aventurera. Mi idea para el video es: {idea} Tu trabajo es generarme lo siguiente optimizado para SEO: 1. TRES (3) OPCIONES DE TÍTULOS (Atractivos y aptos para familia). 2. DESCRIPCIÓN OPTIMIZADA. 3. LISTA DE 15 TAGS."""
                        
                        respuesta_ia = modelo_ia.generate_content(instruccion_cto)
                        st.success("¡Análisis SEO completado! 🎯")
                        st.write(respuesta_ia.text)
                    except Exception as e:
                        st.error(f"Error de IA: {e}")
            else:
                st.warning("Escribe la idea primero.")
                
    # ==========================================
    # --- MÓDULO 3: SALA DE IDEAS (CHAT IA CON MEMORIA) ---
    # ==========================================
    elif modulo == "Chat IA":
        st.subheader("🤖 Consultor CTO IA (Sala de Ideas)")
        st.write("Tu CTO tiene en cuenta los valores del canal, el nicho y quién eres en el equipo.")
        
        # 1. Definimos el ADN del Canal (El Entrenamiento)
        ADN_CANAL = f"""
        INSTRUCCIÓN MAESTRA: Eres el CTO y Consultor Estratégico del canal de YouTube 'SUSANAHORIA'.
        
        INFORMACIÓN DEL CANAL:
        - Protagonista: Susana, una niña de 10 años muy carismática, apoyada por sus papás.
        - Nicho: Vida en el campo, naturaleza, animales, aventuras en la granja, valores familiares y reflexiones cristianas.
        - Misión: Entretener y educar sanamente a las familias, fomentando el amor por la naturaleza y los buenos valores.
        - Tono: Profesional, motivador, creativo, pero siempre manteniendo la inocencia y el respeto familiar. NUNCA sugieras clickbait engañoso, bromas pesadas o contenido que no sea apto para niños.
        
        USUARIO ACTUAL:
        Te está hablando el miembro del equipo logeado como: '{st.session_state['usuario_activo']}'.
        Adapta tus consejos a su rol (si es admin, habla de estrategia; si es guionista, habla de retención y guiones; si es editor, habla de ritmo visual).
        """

        # 2. Inicializar la memoria del chat en esta sesión
        if "memoria_chat" not in st.session_state:
            st.session_state.memoria_chat = []

        # 3. Mostrar el historial de la conversación en pantalla
        for mensaje in st.session_state.memoria_chat:
            with st.chat_message(mensaje["rol"]):
                st.markdown(mensaje["texto"])

        # 4. Caja de texto para que el usuario escriba
        pregunta_usuario = st.chat_input("Escribe tu idea o pregunta al CTO aquí...")

        if pregunta_usuario:
            # A. Mostrar la pregunta del usuario inmediatamente
            with st.chat_message("user"):
                st.markdown(pregunta_usuario)
            
            # B. Guardar la pregunta en la memoria
            st.session_state.memoria_chat.append({"rol": "user", "texto": pregunta_usuario})

            # C. Conectar con Gemini y enviarle la memoria + el ADN
            with st.chat_message("assistant"):
                with st.spinner("El CTO está analizando tu solicitud..."):
                    try:
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        modelo_chat = genai.GenerativeModel('gemini-2.5-flash')
                        
                        # Construimos el contexto completo invisible para enviar a la IA
                        historial_invisible = ADN_CANAL + "\n\nHISTORIAL DE LA CONVERSACIÓN:\n"
                        for m in st.session_state.memoria_chat:
                            historial_invisible += f"{m['rol']}: {m['texto']}\n"
                        
                        # Pedimos la respuesta
                        respuesta = modelo_chat.generate_content(historial_invisible)
                        
                        # Mostramos y guardamos la respuesta
                        st.markdown(respuesta.text)
                        st.session_state.memoria_chat.append({"rol": "assistant", "texto": respuesta.text})
                        
                    except Exception as e:
                        st.error(f"Error de conexión neuronal: {e}")

# ==========================================

# 6. LÓGICA DEL CEREBRO BARRERA
# ==========================================
# El código siempre lee esta parte al inicio. Si nadie se ha logeado, lanza la pantalla 4. Si están logeados, lanza la 5.
if st.session_state['usuario_activo'] is None:
    pantalla_login()
else:
    aplicacion_principal()
