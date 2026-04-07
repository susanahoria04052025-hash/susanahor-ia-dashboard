import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
import json # <-- NUEVO: Para crear el cerebro compartido del equipo
import os

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
st.set_page_config(page_title="SUSANAHOR IA - Centro de Mando", page_icon="🥕", layout="wide")

# ==========================================
# 2. BASE DE DATOS Y PERFILES DEL EQUIPO
# ==========================================
# Aquí definimos los usuarios y contraseñas (¡Cámbialas luego por seguridad!)
USUARIOS_EQUIPO = {
    "luis": "papa123",
    "maridel": "mama123",
    "natalia": "nata123",
    "jose": "jose123",
    "susana": "susi123",
    "neider": "manager123"
}

# La IA leerá esto para saber con quién habla exactamente
PERFILES_EQUIPO = {
    "luis": "Luis Mariano Florez (Papá). Apoya económicamente, tiene visión de negocio y quiere que el canal crezca para futuras ventas.",
    "maridel": "Maridel Castellanos Corzo (Madre). Busca ideas, apoya incondicionalmente y es la reina de la difusión en Facebook y estados.",
    "natalia": "Natalia Flores Castellanos (VESTUARIO). Directora de arte, apoya en vestuario, es estricta y cuida que Susana siempre salga perfecta.",
    "jose": "José Luis Florez Castellanos (EDITOR). El monstruo de la edición. Encargado de grabar, planos, música y ritmo visual.",
    "susana": "Susana Florez Castellanos (SUSANAHORIA). La protagonista, la estrella del canal, siempre dispuesta a colaborar y dar ideas.",
    "neider": "Néider Tarazona (MANAGER). Amigo de la familia y líder del proyecto. Busca métodos y estrategias. Él creó este sistema de IA."
}

# Inicializar sesión
if 'usuario_activo' not in st.session_state:
    st.session_state['usuario_activo'] = None

# Funciones del Cerebro Compartido (Grupo de WhatsApp del equipo)
ARCHIVO_CHAT = "chat_equipo.json"

def cargar_chat():
    if os.path.exists(ARCHIVO_CHAT):
        with open(ARCHIVO_CHAT, "r") as f:
            return json.load(f)
    return []

def guardar_chat(mensajes):
    with open(ARCHIVO_CHAT, "w") as f:
        json.dump(mensajes, f)

# ==========================================
# 3. DISEÑO CORPORATIVO (APPLE STYLE)
# ==========================================
estilo_apple = """
<style>
    .stApp { background-color: #FAFAFC; background-image: radial-gradient(#D1D1D6 1px, transparent 1px); background-size: 20px 20px; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E5E5EA; }
    h1, h2, h3, p, span, div { color: #1C1C1E !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important; }
    [data-testid="metric-container"] { background-color: #FFFFFF; border: 1px solid #E5E5EA; padding: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    .stButton>button { background-color: #00C853; color: white !important; border-radius: 12px; border: none; padding: 10px 24px; font-weight: 600; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #009624; transform: scale(1.02); }
    .caja-login { background-color: rgba(255, 255, 255, 0.95); padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); border: 1px solid #E5E5EA; text-align: center; backdrop-filter: blur(10px); }
</style>
"""
st.markdown(estilo_apple, unsafe_allow_html=True)

# ==========================================
# 4. PANTALLA DE LOGIN
# ==========================================
def pantalla_login():
    st.markdown("<br><br><br>", unsafe_allow_html=True) 
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='caja-login'>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🥕</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Acceso al Sistema</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8E8E93 !important;'>Ingresa tus credenciales del equipo</p>", unsafe_allow_html=True)
        
        usuario_input = st.text_input("Usuario (Ej: neider, luis, susana)").lower()
        password_input = st.text_input("Contraseña", type="password") 
        
        if st.button("🚀 Ingresar al Centro de Mando", use_container_width=True):
            if usuario_input in USUARIOS_EQUIPO and USUARIOS_EQUIPO[usuario_input] == password_input:
                st.session_state['usuario_activo'] = usuario_input
                st.rerun() 
            else:
                st.error("Credenciales incorrectas. Intenta de nuevo.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. EL NÚCLEO DE LA APLICACIÓN
# ==========================================
def aplicacion_principal():
    YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    CANAL_ID = "UCbp_1QxjyzT8cG7_0jy4NUg" 
    
    usuario_id = st.session_state['usuario_activo']
    nombre_perfil = PERFILES_EQUIPO[usuario_id].split(".")[0] # Saca solo el nombre para saludar

    st.title("🥕 SUSANAHOR IA: Centro de Mando")
    st.write(f"Bienvenido al panel, **{nombre_perfil}**.") 

    st.sidebar.markdown("### Perfil de Equipo")
    st.sidebar.info(f"Conectado como:\n**{nombre_perfil}**")
    
    if st.sidebar.button("🔒 Cerrar Sesión"):
        st.session_state['usuario_activo'] = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("Módulos del Sistema")
    modulo = st.sidebar.radio("Navegación:", ["Análisis de Vistas", "Generador de SEO", "Mesa Redonda IA"])

    # --- MÓDULO 1: ANALÍTICAS ---
    if modulo == "Análisis de Vistas":
        st.subheader("📊 Módulo de Analíticas Reales")
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
                    st.error(f"Error interno: {e}")

    # --- MÓDULO 2: GENERADOR SEO ---
    elif modulo == "Generador de SEO":
        st.subheader("✨ Módulo de SEO Mágico")
        idea = st.text_area("¿De qué trata el video?", placeholder="Ej: Alquilamos un caballo para la historia de Saulo...")
        if st.button("🌟 Generar Paquete SEO"):
            if idea:
                with st.spinner("Despertando al cerebro de Gemini..."):
                    try:
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        modelo_ia = genai.GenerativeModel('gemini-2.5-flash') 
                        instruccion_seo = f"Eres el CTO de SUSANAHORIA. Crea SEO para un video familiar cristiano y de campo sobre: {idea}. Dame 3 títulos, descripción y 15 tags."
                        st.write(modelo_ia.generate_content(instruccion_seo).text)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Escribe la idea primero.")
                
    # --- MÓDULO 3: MESA REDONDA IA ---
    elif modulo == "Mesa Redonda IA":
        st.subheader("🗣️ Mesa Redonda con el CTO")
        st.write("Este chat es compartido. Lo que escribas aquí, lo verá todo el equipo y el CTO.")
        
        # 1. El ADN que la IA siempre lee en secreto
        ADN_CANAL = f"""
        INSTRUCCIÓN MAESTRA: Eres el 'CTO y Consultor IA' de la familia y canal 'SUSANAHORIA'.
        
        NUESTRO EQUIPO (Conócelos a todos, trátalos por su nombre si hablan):
        1. Luis Mariano Florez (Papá): Financia, busca negocio.
        2. Maridel Castellanos (Mamá): Difusión, redes sociales, busca ideas.
        3. Natalia Flores (Hermana): Directora de Arte, vestuario, estética.
        4. José Luis Florez (Hermano): Editor Maestro, grabación, música.
        5. Susana Florez (Hija menor): La ESTRELLA y protagonista (10 años).
        6. Néider Tarazona: Manager del canal, mente maestra detrás de este sistema de IA.
        
        EL CANAL: Vida en el campo, valores cristianos, aventuras infantiles, naturaleza. Cero clickbait tóxico.
        
        CONTEXTO DE ESTE MENSAJE:
        Te está hablando directamente: {nombre_perfil}. Respóndele amablemente por su nombre y enfoca tu respuesta en su área de trabajo.
        """

        # 2. Cargar el historial global del equipo
        historial = cargar_chat()

        # 3. Mostrar la conversación en pantalla
        for msj in historial:
            # Si el rol es 'user', mostramos quién lo escribió. Si es 'assistant', es el CTO.
            if msj["rol"] == "user":
                with st.chat_message("user"):
                    st.markdown(f"**{msj['nombre']}** dijo:\n{msj['texto']}")
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msj['texto'])

        # 4. Caja de texto para hablar
        mensaje_nuevo = st.chat_input(f"Escribe tu idea para el equipo, {nombre_perfil.split()[0]}...")

        if mensaje_nuevo:
            # Mostrar el mensaje del usuario al instante
            with st.chat_message("user"):
                st.markdown(f"**{nombre_perfil}** dijo:\n{mensaje_nuevo}")
            
            # Guardar el mensaje en el historial JSON
            historial.append({"rol": "user", "nombre": nombre_perfil, "texto": mensaje_nuevo})
            guardar_chat(historial)

            # Generar respuesta de la IA
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner(f"El CTO está pensando en la idea de {nombre_perfil.split()[0]}..."):
                    try:
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        modelo_chat = genai.GenerativeModel('gemini-2.5-flash')
                        
                        # Armar el documento invisible para enviar a la IA
                        contexto_invisible = ADN_CANAL + "\n\nCONVERSACIÓN DEL EQUIPO:\n"
                        for m in historial:
                            contexto_invisible += f"{m['nombre'] if m['rol']=='user' else 'CTO IA'}: {m['texto']}\n"
                        
                        respuesta_ia = modelo_chat.generate_content(contexto_invisible).text
                        
                        # Mostrar y guardar respuesta
                        st.markdown(respuesta_ia)
                        historial.append({"rol": "assistant", "nombre": "CTO IA", "texto": respuesta_ia})
                        guardar_chat(historial)
                        
                    except Exception as e:
                        st.error(f"Error en la IA: {e}")

# ==========================================
# 6. LÓGICA DE BARRERA
# ==========================================
if st.session_state['usuario_activo'] is None:
    pantalla_login()
else:
    aplicacion_principal()
