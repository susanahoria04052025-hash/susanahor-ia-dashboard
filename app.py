import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
import json 
import os

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
st.set_page_config(page_title="SUSANAHOR IA - Centro de Mando", page_icon="🥕", layout="wide")

# ==========================================
# 2. BASE DE DATOS Y PERFILES DEL EQUIPO
# ==========================================
USUARIOS_EQUIPO = {
    "luis": "papa123",
    "maridel": "mama123",
    "natalia": "nata123",
    "jose": "jose123",
    "susana": "susi123",
    "neider": "manager123"
}

PERFILES_EQUIPO = {
    "luis": "Luis Mariano Florez (Papá). Apoya económicamente, tiene visión de negocio y quiere que el canal crezca para futuras ventas.",
    "maridel": "Maridel Castellanos Corzo (Madre). Busca ideas, apoya incondicionalmente y es la reina de la difusión en Facebook y estados.",
    "natalia": "Natalia Flores Castellanos (Hermana). Directora de arte, apoya en vestuario, es estricta y cuida que Susana siempre salga perfecta.",
    "jose": "José Luis Florez Castellanos (Hermano). El monstruo de la edición. Encargado de grabar, planos, música y ritmo visual.",
    "susana": "Susana Florez Castellanos (Hija menor). La protagonista, la estrella del canal, siempre dispuesta a colaborar y dar ideas.",
    "neider": "Néider Tarazona (Manager). Amigo de la familia y líder del proyecto. Busca métodos y estrategias. Él creó este sistema de IA."
}

if 'usuario_activo' not in st.session_state:
    st.session_state['usuario_activo'] = None

# ==========================================
# NUEVO: LÓGICA DEL TABLERO DE IDEAS (BOMBILLOS)
# ==========================================
ARCHIVO_TABLERO = "tablero_ideas.json"

def cargar_tablero():
    if os.path.exists(ARCHIVO_TABLERO):
        with open(ARCHIVO_TABLERO, "r") as f:
            return json.load(f)
    return []

def guardar_en_tablero(idea_nueva):
    tablero = cargar_tablero()
    # Insertamos la nueva idea al principio de la lista
    tablero.insert(0, idea_nueva)
    with open(ARCHIVO_TABLERO, "w") as f:
        json.dump(tablero, f)

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
    
    /* Estilo para las tarjetas del tablero de ideas */
    .tarjeta-idea { background-color: #FFFFFF; border-left: 5px solid #FFCC00; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px;}
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
        st.markdown("<p style='text-align: center; color: #8E8E93 !important;'>Ingresa tus credenciales</p>", unsafe_allow_html=True)
        
        usuario_input = st.text_input("Usuario").lower()
        password_input = st.text_input("Contraseña", type="password") 
        
        if st.button("🚀 Ingresar", use_container_width=True):
            if usuario_input in USUARIOS_EQUIPO and USUARIOS_EQUIPO[usuario_input] == password_input:
                st.session_state['usuario_activo'] = usuario_input
                st.rerun() 
            else:
                st.error("Credenciales incorrectas.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. EL NÚCLEO DE LA APLICACIÓN
# ==========================================
def aplicacion_principal():
    YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    CANAL_ID = "UCbp_1QxjyzT8cG7_0jy4NUg" 
    
    usuario_id = st.session_state['usuario_activo']
    nombre_perfil = PERFILES_EQUIPO[usuario_id].split(".")[0] 

    st.title("🥕 SUSANAHOR IA: Centro de Mando")
    st.write(f"Panel de Control de **{nombre_perfil}**.") 

    st.sidebar.markdown("### Perfil de Equipo")
    st.sidebar.info(f"Conectado como:\n**{nombre_perfil}**")
    
    if st.sidebar.button("🔒 Cerrar Sesión"):
        st.session_state['usuario_activo'] = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("Módulos del Sistema")
    modulo = st.sidebar.radio("Navegación:", ["Análisis de Vistas", "Generador de SEO", "Laboratorio de Ideas 💡"])

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
                        col1.metric("👥 Suscriptores", stats['subscriberCount'])
                        col2.metric("👁️ Vistas Totales", stats['viewCount'])
                        col3.metric("🎬 Videos Subidos", stats['videoCount'])
                except Exception as e:
                    st.error(f"Error interno: {e}")

    # --- MÓDULO 2: GENERADOR SEO ---
    elif modulo == "Generador de SEO":
        st.subheader("✨ Módulo de SEO Mágico")
        idea = st.text_area("¿De qué trata el video?", placeholder="Ej: Alquilamos un caballo...")
        if st.button("🌟 Generar Paquete SEO"):
            if idea:
                with st.spinner("Despertando al cerebro de Gemini..."):
                    try:
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        modelo_ia = genai.GenerativeModel('gemini-2.5-flash') 
                        st.write(modelo_ia.generate_content(f"Eres el CTO de SUSANAHORIA. Crea SEO para este video: {idea}. Dame 3 títulos, descripción y 15 tags.").text)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Escribe la idea primero.")
                
    # --- MÓDULO 3: LABORATORIO DE IDEAS (PRIVADO + PÚBLICO) ---
    elif modulo == "Laboratorio de Ideas 💡":
        
        # Pestañas Superiores
        tab1, tab2 = st.tabs(["💬 Mi Consultor Privado", "🗂️ Tablero del Equipo"])
        
        # EL ADN DE LA IA
        ADN_CANAL = f"""
        INSTRUCCIÓN MAESTRA: Eres el 'CTO y Consultor IA' de la familia 'SUSANAHORIA'.
        NUESTRO EQUIPO:
        1. Luis Mariano Florez (Papá): Financia, busca negocio.
        2. Maridel Castellanos (Mamá): Difusión, busca ideas.
        3. Natalia Flores (Hermana): Directora de Arte.
        4. José Luis Florez (Hermano): Editor Maestro.
        5. Susana Florez (Hija menor): La ESTRELLA (10 años).
        6. Néider Tarazona: Manager del canal.
        EL CANAL: Vida en el campo, valores cristianos, naturaleza. Cero clickbait tóxico.
        CONTEXTO ACTUAL: Te habla {nombre_perfil} EN PRIVADO. Ayúdalo a desarrollar su idea.
        """

        # ================================
        # PESTAÑA 1: CHAT PRIVADO
        # ================================
        with tab1:
            st.markdown("### Tu espacio privado")
            st.write("Nadie más ve este chat. Cocina tu idea aquí con la IA.")
            
            if "chat_privado" not in st.session_state:
                st.session_state.chat_privado = []

            for msj in st.session_state.chat_privado:
                with st.chat_message(msj["rol"], avatar="🤖" if msj["rol"]=="assistant" else "👤"):
                    st.markdown(msj["texto"])

            mensaje_nuevo = st.chat_input("Consulta con tu CTO privado...")

            if mensaje_nuevo:
                with st.chat_message("user", avatar="👤"):
                    st.markdown(mensaje_nuevo)
                st.session_state.chat_privado.append({"rol": "user", "texto": mensaje_nuevo})

                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("Analizando en privado..."):
                        try:
                            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                            modelo_chat = genai.GenerativeModel('gemini-2.5-flash')
                            
                            contexto = ADN_CANAL + "\n\nCHAT PRIVADO:\n"
                            for m in st.session_state.chat_privado:
                                contexto += f"{m['rol']}: {m['texto']}\n"
                            
                            respuesta_ia = modelo_chat.generate_content(contexto).text
                            st.markdown(respuesta_ia)
                            st.session_state.chat_privado.append({"rol": "assistant", "texto": respuesta_ia})
                        except Exception as e:
                            st.error(f"Error: {e}")
            
            # --- BOTÓN PARA PUBLICAR AL TABLERO ---
            st.markdown("---")
            if len(st.session_state.chat_privado) > 0:
                if st.button("💡 Resumir chat y enviar al Tablero del Equipo", type="primary"):
                    with st.spinner("La IA está extrayendo la idea principal..."):
                        try:
                            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                            modelo_resumen = genai.GenerativeModel('gemini-2.5-flash')
                            
                            # Le pedimos a la IA que lea el chat privado y lo resuma
                            texto_a_resumir = ""
                            for m in st.session_state.chat_privado:
                                texto_a_resumir += f"{m['rol']}: {m['texto']}\n"
                                
                            prompt_resumen = f"Lee este chat entre {nombre_perfil} y la IA. Extrae SOLO LA IDEA PRINCIPAL o CONCLUSIÓN a la que llegaron. Redáctalo en un solo párrafo corto, profesional y motivador para que el resto del equipo lo lea. Empieza diciendo 'Propuesta de {nombre_perfil}:'. CHAT: {texto_a_resumir}"
                            
                            resumen_final = modelo_resumen.generate_content(prompt_resumen).text
                            
                            # Guardamos en la base de datos pública
                            guardar_en_tablero({"autor": nombre_perfil, "idea": resumen_final})
                            st.success("¡Tu idea pulida ya está en el Tablero del Equipo!")
                        except Exception as e:
                            st.error("Error al resumir.")

        # ================================
        # PESTAÑA 2: TABLERO PÚBLICO
        # ================================
        with tab2:
            st.markdown("### 🗂️ Ideas Aprobadas del Equipo")
            st.write("Aquí aparecen los resúmenes de las ideas que el equipo ha trabajado con la IA.")
            
            tablero_actual = cargar_tablero()
            
            if len(tablero_actual) == 0:
                st.info("Aún no hay ideas en el tablero. ¡Ve a tu chat privado y genera la primera!")
            else:
                for item in tablero_actual:
                    st.markdown(f"""
                    <div class='tarjeta-idea'>
                        <h4>💡 Idea de: {item['autor']}</h4>
                        <p style='color: #4A4A4A;'>{item['idea']}</p>
                    </div>
                    """, unsafe_allow_html=True)

# ==========================================
if st.session_state['usuario_activo'] is None:
    pantalla_login()
else:
    aplicacion_principal()
