import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
import json 
import os
from datetime import datetime, timedelta # Agregado timedelta para fechas precisas
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
st.set_page_config(page_title="SUSANAHOR IA - Centro de Mando", page_icon="🥕", layout="wide")

# ==========================================
# 2. BASE DE DATOS Y PERFILES
# ==========================================
USUARIOS_EQUIPO = {
    "luis": "papa123", "maridel": "mama123", "natalia": "nata123",
    "jose": "jose123", "susana": "susi123", "neider": "manager123"
}

PERFILES_EQUIPO = {
    "luis": "Luis Mariano Florez (Papá). Negocios.", "maridel": "Maridel (Mamá). Difusión.",
    "natalia": "Natalia (Hermana). Arte.", "jose": "José (Hermano). Editor.",
    "susana": "Susana (Estrella).", "neider": "Néider Tarazona (Manager)."
}

if 'usuario_activo' not in st.session_state:
    st.session_state['usuario_activo'] = None

# ==========================================
# 3. LÓGICA DE BASES DE DATOS JSON
# ==========================================
ARCHIVO_TABLERO = "tablero_ideas.json"
ARCHIVO_CALENDARIO = "calendario_equipo.json"

def cargar_json(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            return json.load(f)
    return []

def guardar_json(archivo, datos):
    with open(archivo, "w") as f:
        json.dump(datos, f)

# ==========================================
# 4. RECURSOS VISUALES Y DISEÑO (CSS & LOGOS)
# ==========================================
st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');</style>", unsafe_allow_html=True)

LOGO_LOGIN = """
<div style="display: flex; justify-content: center; align-items: baseline; margin-bottom: 10px;">
    <span style="font-size: 3rem; margin-right: 12px;">🥕</span>
    <span style="font-family: -apple-system, sans-serif; font-weight: 800; color: #1C1C1E; font-size: 3.2rem;">SUSANAHOR</span>
    <span style="font-family: 'Pacifico', cursive; color: #00C853; font-size: 3.8rem; margin-left: 2px; text-transform: lowercase;">ia</span>
</div>
"""

LOGO_PANEL = """
<div style="display: flex; align-items: baseline; margin-bottom: 10px; margin-top: -15px;">
    <span style="font-size: 2.2rem; margin-right: 12px;">🥕</span>
    <span style="font-family: -apple-system, sans-serif; font-weight: 800; color: #1C1C1E; font-size: 2.5rem;">SUSANAHOR</span>
    <span style="font-family: 'Pacifico', cursive; color: #00C853; font-size: 3rem; margin-left: 2px; text-transform: lowercase;">ia</span>
    <span style="color: #8E8E93; font-size: 1.4rem; font-weight: 500; margin-left: 15px; border-left: 2px solid #E5E5EA; padding-left: 15px;">Centro de Mando</span>
</div>
"""

estilo_apple_premium = """
<style>
    .stApp { background-color: #FAFAFC; background-image: radial-gradient(#E5E5EA 1px, transparent 1px); background-size: 25px 25px; }
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E5E5EA; }
    h1, h2, h3, p, label { color: #1C1C1E !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important; }
    [data-testid="metric-container"] { background-color: #FFFFFF; border: 1px solid #E5E5EA; padding: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    .stButton>button { background: linear-gradient(135deg, #00C853 0%, #009624 100%); color: white !important; border-radius: 12px; border: none; padding: 12px 24px; font-weight: 600; box-shadow: 0 4px 10px rgba(0, 200, 83, 0.3); transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0, 200, 83, 0.4); }
    .caja-login { background-color: rgba(255, 255, 255, 0.95); padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #E5E5EA; text-align: center; backdrop-filter: blur(10px); }
</style>
"""
st.markdown(estilo_apple_premium, unsafe_allow_html=True)

# ==========================================
# 5. PANTALLA DE LOGIN
# ==========================================
def pantalla_login():
    st.markdown("<br><br>", unsafe_allow_html=True) 
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='caja-login'>", unsafe_allow_html=True)
        st.markdown(LOGO_LOGIN, unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8E8E93 !important; margin-bottom: 25px;'>Ingresa tus credenciales del equipo</p>", unsafe_allow_html=True)
        
        usuario_input = st.text_input("Usuario").lower()
        password_input = st.text_input("Contraseña", type="password") 
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Ingresar al Sistema", use_container_width=True):
            if usuario_input in USUARIOS_EQUIPO and USUARIOS_EQUIPO[usuario_input] == password_input:
                st.session_state['usuario_activo'] = usuario_input
                st.rerun() 
            else:
                st.error("Credenciales incorrectas.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. NÚCLEO DE LA APLICACIÓN
# ==========================================
def aplicacion_principal():
    usuario_id = st.session_state['usuario_activo']
    nombre_perfil = PERFILES_EQUIPO[usuario_id].split(".")[0] 

    st.markdown(LOGO_PANEL, unsafe_allow_html=True)
    st.write(f"Panel de Control de **{nombre_perfil}**.") 

    st.sidebar.markdown("### Perfil de Equipo")
    st.sidebar.info(f"Conectado como:\n**{nombre_perfil}**")
    if st.sidebar.button("🔒 Cerrar Sesión"):
        st.session_state['usuario_activo'] = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("Módulos del Sistema")
    modulo = st.sidebar.radio("Navegación:", ["Análisis y Auditoría 📈", "Generador de SEO ✨", "Laboratorio de Ideas 💡", "📅 Cronograma de Producción"])

    # ==========================================
    # --- MÓDULO 1: AUDITORÍA NIVEL DIOS (CORREGIDO) ---
    # ==========================================
    if modulo == "Análisis y Auditoría 📈": 
        st.subheader("🕵️‍♂️ Auditoría Nivel Dios (Métricas Privadas)")
        st.write("Conéctate como el administrador del canal para que la IA lea la retención y el tiempo de visualización real.")

        SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
        info_cliente = json.loads(st.secrets["GOOGLE_OAUTH_JSON"])
        
        # ⚠️ NUEVO 1: Usaremos la URL real de Streamlit para que Google no bloquee la seguridad
        URL_REDIRECCION = "https://susanahor-ia-dashboard-bqf4sggyp3jgoifnfyduyr.streamlit.app" 

      # Si regresamos con éxito de Google, atrapamos el código de la URL
        if "code" in st.query_params:
            try:
                flow = Flow.from_client_config(info_cliente, scopes=SCOPES, redirect_uri=URL_REDIRECCION)
                # Extraemos solo el código secreto directamente (LA CORRECCIÓN MÁGICA)
                codigo_secreto = st.query_params["code"]
                flow.fetch_token(code=codigo_secreto)
                
                st.session_state['yt_credenciales_privadas'] = flow.credentials.to_json()
                st.query_params.clear() 
                st.rerun()
            except Exception as e:
                st.error(f"Hubo un error al atrapar la llave de Google: {e}")

        if 'yt_credenciales_privadas' not in st.session_state:
            flow = Flow.from_client_config(info_cliente, scopes=SCOPES, redirect_uri=URL_REDIRECCION)
            url_autorizacion, estado = flow.authorization_url(prompt='consent', access_type='offline')
            
            st.info("Para auditar datos privados, la IA necesita permiso de la cuenta dueña del canal.")
            # ⚠️ NUEVO 2: Cambié target="_self" por target="_top" para romper el iframe de Hostinger y evitar bloqueos.
            st.markdown(f'<a href="{url_autorizacion}" target="_blank" style="display:inline-block; padding:12px 24px; background-color:#4285F4; color:white; border-radius:12px; text-decoration:none; font-weight:bold; box-shadow: 0 4px 6px rgba(66, 133, 244, 0.3);">🔐 Iniciar sesión con Google (Pestaña Nueva)</a>', unsafe_allow_html=True)

        else:
            st.success("✅ Conectado exitosamente a la bóveda privada de YouTube.")
            
            if st.button("🚀 Extraer Retención y Auditar", type="primary"):
                with st.spinner("Hackeando la base de datos privada de YouTube..."):
                    try:
                        creds = Credentials.from_authorized_user_info(json.loads(st.session_state['yt_credenciales_privadas']), SCOPES)
                        youtube_analytics = build('youtubeAnalytics', 'v2', credentials=creds)
                        
                        hoy = datetime.today().strftime('%Y-%m-%d')
                        hace_30_dias = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
                        
                        respuesta_analiticas = youtube_analytics.reports().query(
                            ids='channel==MINE',
                            startDate=hace_30_dias,
                            endDate=hoy,
                            metrics='views,estimatedMinutesWatched,averageViewDuration',
                            dimensions='video',
                            maxResults=10,
                            sort='-views' 
                        ).execute()

                        reporte_privado = "MÉTRICAS PRIVADAS DE RETENCIÓN (Últimos 30 días):\n"
                        if 'rows' in respuesta_analiticas:
                            for fila in respuesta_analiticas['rows']:
                                reporte_privado += f"- ID Video: {fila[0]} | Vistas: {fila[1]} | Minutos totales vistos: {fila[2]} | Duración Promedio Vista: {fila[3]} segundos\n"
                        
                        with st.expander("Ver datos privados extraídos"):
                            st.text(reporte_privado)

                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        prompt_auditor = f"""
                        Eres el CTO y Auditor experto en retención de 'SUSANAHORIA'.
                        Acabo de extraer datos PRIVADOS reales de los últimos 30 días:
                        {reporte_privado}
                        
                        1. Explica al equipo qué significa la 'Duración Promedio Vista' (averageViewDuration en segundos) de los 2 videos principales.
                        2. Dales instrucciones directas y motivadoras sobre cómo mejorar la RETENCIÓN visual (cortes, música, ganchos) en el próximo rodaje basándote ESTRICTAMENTE en estos números.
                        """
                        
                        auditoria = genai.GenerativeModel('gemini-2.5-flash').generate_content(prompt_auditor).text
                        st.markdown(f"<div style='background:#F4F4F5; padding:20px; border-radius:10px; border-left:5px solid #FF3B30; margin-top:20px;'>{auditoria}</div>", unsafe_allow_html=True)
                        st.balloons()

                    except Exception as e:
                        st.error(f"Error al procesar datos: {e}")
    # ==========================================
    # --- MÓDULO 2: SEO ---
    # ==========================================
    elif modulo == "Generador de SEO ✨":
        st.subheader("✨ Módulo de SEO Mágico")
        idea = st.text_area("¿De qué trata el video?")
        if st.button("🌟 Generar Paquete SEO") and idea:
            with st.spinner("Despertando IA..."):
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                st.write(genai.GenerativeModel('gemini-2.5-flash').generate_content(f"Crea SEO para SUSANAHORIA sobre: {idea}. 3 títulos, descripción y 15 tags.").text)

    # ==========================================
    # --- MÓDULO 3: LABORATORIO DE IDEAS ---
    # ==========================================
    elif modulo == "Laboratorio de Ideas 💡":
        tab1, tab2 = st.tabs(["💬 Mi Consultor Privado", "🗂️ Tablero del Equipo"])
        with tab1:
            if "chat_privado" not in st.session_state: st.session_state.chat_privado = []
            for msj in st.session_state.chat_privado: st.chat_message(msj["rol"]).markdown(msj["texto"])
            mensaje = st.chat_input("Consulta...")
            if mensaje:
                st.chat_message("user").markdown(mensaje)
                st.session_state.chat_privado.append({"rol": "user", "texto": mensaje})
                with st.spinner("Analizando..."):
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    contexto = f"Eres CTO de SUSANAHORIA. Ayuda a {nombre_perfil}.\nCHAT:\n" + "\n".join([f"{m['rol']}: {m['texto']}" for m in st.session_state.chat_privado])
                    respuesta = genai.GenerativeModel('gemini-2.5-flash').generate_content(contexto).text
                    st.chat_message("assistant").markdown(respuesta)
                    st.session_state.chat_privado.append({"rol": "assistant", "texto": respuesta})
            
            st.markdown("---")
            if st.button("💡 Enviar resumen al Tablero") and len(st.session_state.chat_privado) > 0:
                with st.spinner("Resumiendo..."):
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    resumen = genai.GenerativeModel('gemini-2.5-flash').generate_content(f"Resume esta idea de {nombre_perfil} en 1 párrafo: " + "\n".join([m['texto'] for m in st.session_state.chat_privado])).text
                    tablero = cargar_json(ARCHIVO_TABLERO)
                    tablero.insert(0, {"autor": nombre_perfil, "idea": resumen})
                    guardar_json(ARCHIVO_TABLERO, tablero)
                    st.success("¡Enviado!")

        with tab2:
            st.markdown("### 🗂️ Ideas Aprobadas")
            for item in cargar_json(ARCHIVO_TABLERO):
                st.markdown(f"<div style='background:white; padding:15px; border-left:5px solid #FFCC00; margin-bottom:10px; border-radius:8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'><b>De: {item['autor']}</b><br>{item['idea']}</div>", unsafe_allow_html=True)

    # ==========================================
    # --- MÓDULO 4: CALENDARIO DE PRODUCCIÓN ---
    # ==========================================
    elif modulo == "📅 Cronograma de Producción":
        st.subheader("📅 Cronograma Interactivo")
        col_sync, col_vacio = st.columns([1, 4])
        with col_sync:
            if st.button("🔄 Sincronizar Calendario"):
                st.rerun()

        with st.expander("➕ Añadir nuevo video o tarea al cronograma", expanded=False):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                fecha_seleccionada = st.date_input("Fecha programada", datetime.today())
            with col2:
                nombre_tarea = st.text_input("Nombre del Video / Tarea", placeholder="Ej: Video de Saulo de Tarso")
            with col3:
                tipo_tarea = st.selectbox("Estado", ["🟩 SUBIR VIDEO (Listo)", "🟪 GRABAR / EDITAR", "🟨 IDEA / FLEXIBLE"])
                
            if st.button("Agendar en el Calendario", type="primary"):
                if nombre_tarea:
                    agenda = cargar_json(ARCHIVO_CALENDARIO)
                    nueva_tarea = {
                        "fecha": fecha_seleccionada.strftime("%Y-%m-%d"),
                        "tarea": nombre_tarea,
                        "tipo": tipo_tarea,
                        "responsable": nombre_perfil
                    }
                    agenda.append(nueva_tarea)
                    guardar_json(ARCHIVO_CALENDARIO, agenda)
                    st.success("¡Agendado correctamente!")
                    st.rerun() 
                else:
                    st.warning("Debes escribir el nombre del video.")

        st.markdown("---")
        agenda_actual = cargar_json(ARCHIVO_CALENDARIO)
        
        eventos_calendario = []
        for item in agenda_actual:
            color_fondo = "#00C853" 
            if "🟪" in item['tipo']: color_fondo = "#AF52DE" 
            elif "🟨" in item['tipo']: color_fondo = "#FFCC00" 

            eventos_calendario.append({
                "title": f"{item['tarea']} ({item['responsable'].split()[0]})",
                "start": item['fecha'],
                "backgroundColor": color_fondo,
                "borderColor": color_fondo,
            })

        opciones_calendario = {
            "headerToolbar": {"left": "prev,next today", "center": "title", "right": "dayGridMonth,timeGridWeek"},
            "initialView": "dayGridMonth",
            "locale": "es",
        }

        css_calendario = """
            .fc-event-title { font-weight: bold; color: white !important; font-size: 0.85rem; padding: 2px;}
            .fc-event-time { display: none; } 
        """

        from streamlit_calendar import calendar
        calendar(events=eventos_calendario, options=opciones_calendario, custom_css=css_calendario)

# ==========================================
# 7. LÓGICA DE BARRERA
# ==========================================
if st.session_state['usuario_activo'] is None:
    pantalla_login()
else:
    aplicacion_principal()
