import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
import json 
import os
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from streamlit_option_menu import option_menu # NUEVA LIBRERÍA DE MENÚ MÓVIL

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
st.set_page_config(page_title="SUSANAHOR IA", page_icon="🥕", layout="centered", initial_sidebar_state="collapsed")

# ==========================================
# 2. BASE DE DATOS Y PERFILES
# ==========================================
USUARIOS_EQUIPO = {
    "luis": "papa123", "maridel": "mama123", "natalia": "nata123",
    "jose": "jose123", "susana": "susi123", "neider": "manager123"
}

PERFILES_EQUIPO = {
    "luis": "Luis Mariano Florez (Papá)", "maridel": "Maridel (Mamá)",
    "natalia": "Natalia (Hermana)", "jose": "José (Hermano)",
    "susana": "Susana (Estrella)", "neider": "Néider Tarazona (Manager)"
}

if 'usuario_activo' not in st.session_state:
    st.session_state['usuario_activo'] = None

ARCHIVO_TABLERO = "tablero_ideas.json"
ARCHIVO_CALENDARIO = "calendario_equipo.json"
ARCHIVO_TOKEN_YT = "youtube_token.json"
ARCHIVO_TEMP_OAUTH = "temp_oauth.json"

def cargar_json(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r") as f: return json.load(f)
    return []

def guardar_json(archivo, datos):
    with open(archivo, "w") as f: json.dump(datos, f)

# ==========================================
# 3. DISEÑO UI/UX MOBILE-FIRST (APP NATIVA)
# ==========================================
st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');</style>", unsafe_allow_html=True)

tema_app_movil = """
<style>
    /* Fondo de la App (Gris muy claro/crema) */
    .stApp { background-color: #F4F7F6; }
    
    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;} /* Ocultar flecha del sidebar */
    
    /* Tipografía global limpia */
   html, body, p, h1, h2, h3, h4, h5, h6, label {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        color: #1C1C1E;
    }

    /* ESTILO DE TARJETAS (CARDS) */
    .card-susanahoria {
        background-color: #FFFFFF;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        border: 1px solid #F0F0F0;
    }

    /* LOGO SUSANAHORIA */
    .logo-container { display: flex; align-items: center; justify-content: center; margin-bottom: 10px; }
    .logo-icon { font-size: 2.5rem; margin-right: 8px; }
    .logo-text-1 { font-weight: 900; color: #1C1C1E; font-size: 2.2rem; letter-spacing: -0.5px; }
    .logo-text-2 { font-family: 'Pacifico', cursive !important; color: #00C853 !important; font-size: 2.6rem; margin-left: 2px; text-transform: lowercase; font-weight: normal;}

    /* BOTONES PREMIUM (Naranja Zanahoria) */
    .stButton>button { 
        background: linear-gradient(135deg, #FF8A65 0%, #FF5722 100%);
        color: white !important; 
        border-radius: 16px; 
        border: none; 
        padding: 12px 24px; 
        font-weight: bold; 
        font-size: 1.1rem;
        box-shadow: 0 4px 12px rgba(255, 87, 34, 0.3);
        transition: all 0.3s ease; 
        width: 100%;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(255, 87, 34, 0.4); }
    
    /* Botón secundario (Google/Cerrar sesión) */
    .btn-secundario>button { background: #F4F7F6 !important; color: #1C1C1E !important; box-shadow: none !important; border: 1px solid #E5E5EA !important; }
    
    /* Inputs de texto */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { border-radius: 12px; border: 1px solid #E5E5EA; padding: 12px; background-color: #FAFAFC;}
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus { border-color: #00C853; box-shadow: 0 0 0 1px #00C853;}

    /* Calendario Mobile */
    .fc-toolbar-title { font-size: 1.2rem !important; color: #1C1C1E !important; }
    .fc-button-primary { background-color: #00C853 !important; border: none !important; border-radius: 8px !important; }
    .fc-event { border-radius: 6px !important; border: none !important; padding: 2px 4px !important; }
    .fc-event-title { font-weight: 600; color: white !important; font-size: 0.75rem; white-space: normal !important; }
    .fc-daygrid-day-number { color: #1C1C1E !important; font-weight: 500; }
</style>
"""
st.markdown(tema_app_movil, unsafe_allow_html=True)

# ==========================================
# 4. PANTALLA DE LOGIN (ESTILO APP)
# ==========================================
def pantalla_login():
    st.markdown("<br><br>", unsafe_allow_html=True) 
    st.markdown("""
        <div class='card-susanahoria' style='max-width: 400px; margin: 0 auto;'>
            <div class='logo-container'>
                <span class='logo-icon'>🥕</span>
                <span class='logo-text-1'>SUSANAHOR</span><span class='logo-text-2'>ia</span>
            </div>
            <p style='text-align: center; color: #8E8E93; margin-bottom: 30px; font-size: 0.9rem;'>Ingresa tus credenciales para continuar</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        usuario_input = st.text_input("Usuario", placeholder="Ej: neider")
        password_input = st.text_input("Contraseña", type="password", placeholder="••••••••") 
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Ingresar"):
            if usuario_input.lower() in USUARIOS_EQUIPO and USUARIOS_EQUIPO[usuario_input.lower()] == password_input:
                st.session_state['usuario_activo'] = usuario_input.lower()
                st.rerun() 
            else:
                st.error("Credenciales incorrectas.")

# ==========================================
# 5. NÚCLEO DE LA APP (INTERFAZ PRINCIPAL)
# ==========================================
def aplicacion_principal():
    usuario_id = st.session_state['usuario_activo']
    nombre_perfil = PERFILES_EQUIPO[usuario_id]

    # --- HEADER CARD (Logo y Perfil) ---
    st.markdown(f"""
        <div class='card-susanahoria' style='padding: 15px 20px; display: flex; justify-content: space-between; align-items: center;'>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 1.8rem; margin-right: 5px;'>🥕</span>
                <span style='font-weight: 900; color: #1C1C1E; font-size: 1.4rem; letter-spacing: -0.5px;'>SUSANAHOR</span><span style="font-family: 'Pacifico', cursive; color: #00C853; font-size: 1.6rem; margin-left: 1px;">ia</span>
            </div>
            <div style='text-align: right;'>
                <span style='font-size: 0.8rem; color: #8E8E93; display: block;'>Hola,</span>
                <span style='font-weight: bold; color: #1C1C1E; font-size: 0.9rem;'>{nombre_perfil.split()[0]} 👋</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Botón de cerrar sesión discreto
    col_vacio, col_salir = st.columns([3, 1])
    with col_salir:
        st.markdown("<div class='btn-secundario'>", unsafe_allow_html=True)
        if st.button("🚪 Salir"):
            st.session_state['usuario_activo'] = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- MENÚ DE NAVEGACIÓN MÓVIL (TABS) ---
    modulo = option_menu(
        menu_title=None, 
        options=["Auditoría", "SEO", "Ideas", "Agenda"], 
        icons=["graph-up-arrow", "magic", "lightbulb", "calendar2-week"], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "margin-bottom": "20px"},
            "icon": {"color": "#8E8E93", "font-size": "18px"}, 
            "nav-link": {"font-size": "12px", "text-align": "center", "margin":"0px", "--hover-color": "#E5E5EA", "color": "#1C1C1E", "font-weight": "600"},
            "nav-link-selected": {"background-color": "#00C853", "color": "white", "icon-color": "white"},
        }
    )

    # ==========================================
    # --- MÓDULO 1: AUDITORÍA ---
    # ==========================================
    if modulo == "Auditoría":
        st.markdown("<div class='card-susanahoria'>", unsafe_allow_html=True)
        st.markdown("### 🕵️‍♂️ Auditoría Real del Canal")
        st.write("Analiza la retención real de los últimos 30 días.")

        SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
        info_cliente = json.loads(st.secrets["GOOGLE_OAUTH_JSON"])
        URL_REDIRECCION = "https://susanahor-ia-dashboard-bqf4sggyp3jgoifnfyduyr.streamlit.app" 

        if "code" in st.query_params:
            try:
                flow = Flow.from_client_config(info_cliente, scopes=SCOPES, redirect_uri=URL_REDIRECCION)
                datos_temp = cargar_json(ARCHIVO_TEMP_OAUTH)
                if datos_temp and "code_verifier" in datos_temp: flow.code_verifier = datos_temp["code_verifier"]
                flow.fetch_token(code=st.query_params["code"])
                guardar_json(ARCHIVO_TOKEN_YT, json.loads(flow.credentials.to_json()))
                st.query_params.clear() 
                st.success("¡✅ Llave guardada! Recarga la página.")
                st.stop()
            except Exception as e: st.error(f"Error: {e}")

        token_guardado = cargar_json(ARCHIVO_TOKEN_YT)
        
        if not token_guardado:
            flow = Flow.from_client_config(info_cliente, scopes=SCOPES, redirect_uri=URL_REDIRECCION)
            url_autorizacion, estado = flow.authorization_url(prompt='consent', access_type='offline')
            guardar_json(ARCHIVO_TEMP_OAUTH, {"code_verifier": flow.code_verifier})
            st.link_button("🔐 Conectar con Google", url_autorizacion, type="primary")
        else:
            if st.button("🚀 Extraer y Auditar"):
                with st.spinner("Hackeando YouTube..."):
                    try:
                        creds = Credentials.from_authorized_user_info(token_guardado, SCOPES)
                        youtube_analytics = build('youtubeAnalytics', 'v2', credentials=creds)
                        hoy = datetime.today().strftime('%Y-%m-%d')
                        hace_30_dias = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
                        
                        respuesta_analiticas = youtube_analytics.reports().query(
                            ids='channel==MINE', startDate=hace_30_dias, endDate=hoy,
                            metrics='views,estimatedMinutesWatched,averageViewDuration', dimensions='video',
                            maxResults=10, sort='-views' 
                        ).execute()

                       # Creamos un diccionario para traducir IDs a Títulos reales
                        mapa_titulos = dict(zip(ids_videos, titulos))

                        reporte_privado = "MÉTRICAS PRIVADAS DE RETENCIÓN (Últimos 30 días):\n"
                        if 'rows' in respuesta_analiticas:
                            for fila in respuesta_analiticas['rows']:
                                id_vid = fila[0]
                                titulo_real = mapa_titulos.get(id_vid, "Video Antiguo/Desconocido")
                                reporte_privado += f"- Video: '{titulo_real}' | Vistas: {fila[1]} | Retención: {fila[3]} segundos\n"
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        prompt = f"Eres CTO de SUSANAHORIA. Analiza estos datos privados de retención (averageViewDuration en seg): {reporte_privado}. Da instrucciones agresivas a José (Edición) y Natalia (Arte) para mejorar la retención en los primeros 15 segundos."
                        auditoria = genai.GenerativeModel('gemini-2.5-flash').generate_content(prompt).text
                        
                        st.markdown(f"<div style='background:#F4F7F6; padding:20px; border-radius:16px; border-left:6px solid #FF8A65; margin-top:20px;'>{auditoria}</div>", unsafe_allow_html=True)
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error: {e}")
                        if st.button("🔄 Reiniciar Conexión"): os.remove(ARCHIVO_TOKEN_YT); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================
    # --- MÓDULO 2: SEO ---
    # ==========================================
    elif modulo == "SEO":
        st.markdown("<div class='card-susanahoria'>", unsafe_allow_html=True)
        st.markdown("### ✨ Generador SEO")
        idea = st.text_area("¿De qué trata el video?", placeholder="Ej: Susana encuentra un nido...")
        if st.button("🌟 Generar Paquete SEO") and idea:
            with st.spinner("Creando magia..."):
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                st.write(genai.GenerativeModel('gemini-2.5-flash').generate_content(f"Crea SEO para SUSANAHORIA sobre: {idea}. 3 títulos, descripción y 15 tags.").text)
        st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================
    # --- MÓDULO 3: IDEAS ---
    # ==========================================
    elif modulo == "Ideas":
        st.markdown("<div class='card-susanahoria'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["💬 Privado", "🗂️ Tablero"])
        with tab1:
            if "chat_privado" not in st.session_state: st.session_state.chat_privado = []
            for msj in st.session_state.chat_privado: st.chat_message(msj["rol"]).markdown(msj["texto"])
            mensaje = st.chat_input("Habla con el CTO...")
            if mensaje:
                st.chat_message("user").markdown(mensaje)
                st.session_state.chat_privado.append({"rol": "user", "texto": mensaje})
                with st.spinner("Pensando..."):
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    contexto = f"Eres CTO de SUSANAHORIA. Ayuda a {nombre_perfil}.\nCHAT:\n" + "\n".join([f"{m['rol']}: {m['texto']}" for m in st.session_state.chat_privado])
                    respuesta = genai.GenerativeModel('gemini-2.5-flash').generate_content(contexto).text
                    st.chat_message("assistant").markdown(respuesta)
                    st.session_state.chat_privado.append({"rol": "assistant", "texto": respuesta})
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💡 Enviar al Tablero") and len(st.session_state.chat_privado) > 0:
                with st.spinner("Resumiendo..."):
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    resumen = genai.GenerativeModel('gemini-2.5-flash').generate_content(f"Resume esta idea de {nombre_perfil} en 1 párrafo: " + "\n".join([m['texto'] for m in st.session_state.chat_privado])).text
                    tablero = cargar_json(ARCHIVO_TABLERO)
                    tablero.insert(0, {"autor": nombre_perfil.split()[0], "idea": resumen})
                    guardar_json(ARCHIVO_TABLERO, tablero)
                    st.success("¡Enviado!")

        with tab2:
            for item in cargar_json(ARCHIVO_TABLERO):
                st.markdown(f"<div style='background:#F4F7F6; padding:15px; border-left:5px solid #00C853; margin-bottom:10px; border-radius:12px;'><b>De: {item['autor']}</b><br>{item['idea']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================
    # --- MÓDULO 4: AGENDA ---
    # ==========================================
    elif modulo == "Agenda":
        st.markdown("<div class='card-susanahoria'>", unsafe_allow_html=True)
        st.markdown("### 📅 Cronograma")
        
        with st.expander("➕ Añadir Tarea", expanded=False):
            fecha_sel = st.date_input("Fecha", datetime.today())
            nombre_tarea = st.text_input("Video / Tarea")
            tipo_tarea = st.selectbox("Estado", ["🟩 SUBIR VIDEO", "🟪 GRABAR / EDITAR", "🟨 IDEA"])
            if st.button("Agendar"):
                if nombre_tarea:
                    agenda = cargar_json(ARCHIVO_CALENDARIO)
                    agenda.append({"fecha": fecha_sel.strftime("%Y-%m-%d"), "tarea": nombre_tarea, "tipo": tipo_tarea, "responsable": nombre_perfil.split()[0]})
                    guardar_json(ARCHIVO_CALENDARIO, agenda)
                    st.rerun() 

        st.markdown("<br>", unsafe_allow_html=True)
        agenda_actual = cargar_json(ARCHIVO_CALENDARIO)
        eventos_calendario = []
        for item in agenda_actual:
            color_fondo = "#00C853" if "🟩" in item['tipo'] else "#AF52DE" if "🟪" in item['tipo'] else "#FFCC00"
            eventos_calendario.append({"title": f"{item['tarea']} ({item['responsable']})", "start": item['fecha'], "backgroundColor": color_fondo, "borderColor": color_fondo})

        opciones_calendario = {
            "headerToolbar": {"left": "prev,next", "center": "title", "right": "dayGridMonth,listMonth"},
            "initialView": "listMonth", # Vista de lista por defecto para móviles (más elegante)
            "locale": "es",
            "height": "auto"
        }
        from streamlit_calendar import calendar
        calendar(events=eventos_calendario, options=opciones_calendario)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
if st.session_state['usuario_activo'] is None: pantalla_login()
else: aplicacion_principal()
