# CanaryAir Studio — Dashboard profesional y elegante
# Requisitos recomendados:
# pip install streamlit pandas sqlalchemy plotly pydeck streamlit-keplergl keplergl
# Opcional para exportación de imágenes: pip install -U kaleido

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.express as px
import pydeck as pdk

# Kepler.gl opcional
try:
    from keplergl import KeplerGl
    import streamlit_keplergl as skgl
    KEPLER_AVAILABLE = True
except Exception:
    KEPLER_AVAILABLE = False

# ---------------------------------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------------------------------
st.set_page_config(
    page_title="CanaryAir Studio",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema elegante sobrio
st.markdown("""
<style>
    /* Tipografía elegante y colores discretos */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, .stApp { font-family: 'Inter', sans-serif; }
    .stApp { background: #0F141B; color: #E6E8EB; }

    /* Contenedores */
    .card {
        background: #121820;
        border: 1px solid #1C2430;
        border-radius: 16px;
        padding: 20px;
    }
    .soft {
        background: #11171E;
        border: 1px solid #202A36;
        border-radius: 12px;
        padding: 16px;
    }

    /* Títulos */
    h1, h2, h3 { color: #E6E8EB; }
    .title-xl {
        font-size: 34px; font-weight: 700; letter-spacing: -0.02em;
    }
    .title-md {
        font-size: 20px; font-weight: 700; letter-spacing: -0.01em;
    }

    /* Métricas */
    div[data-testid="stMetric"] {
        background: #121820;
        border: 1px solid #1C2430;
        border-radius: 14px;
        padding: 18px 16px;
        box-shadow: none;
    }
    div[data-testid="stMetric"] label {
        color: #9AA6B2 !important;
        text-transform: none !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #E6E8EB !important;
        font-size: 26px !important;
        font-weight: 700 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; background: #11171E; border: 1px solid #202A36;
        padding: 8px; border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent; border-radius: 8px; color: #CBD5E1;
        font-weight: 600; padding: 10px 14px;
    }
    .stTabs [data-baseweb="tab"]:hover { background: #16202A; color: #E6E8EB; }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #182230 0%, #141A22 100%) !important; color: #E6E8EB !important;
        border: 1px solid #2A3646;
    }

    /* Botones */
    .stButton > button {
        background: linear-gradient(180deg, #1B2A38 0%, #182230 100%);
        color: #E6E8EB; border: 1px solid #2A3646;
        border-radius: 10px; padding: 10px 16px; font-weight: 700;
    }
    .stButton > button:hover { border-color: #3A4B62; background: #1E2D3D; }

    /* Dataframe */
    .stDataFrame { background: #11171E; border-radius: 12px; overflow: hidden; }
    .stDataFrame [class*="rowHeading"], .stDataFrame [class*="colHeading"] {
        background: #10161D !important; color: #9AA6B2 !important;
        border-color: #1C2430 !important;
    }

    /* Ocultar marcas de Streamlit */
    #MainMenu, header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------------------
# Parámetros y utilidades
# ---------------------------------------------------------------------------------------
DB_CONNECTION = "postgresql://admin_canary:CanaryIslands2025!@localhost:5433/canaryair"

@st.cache_data(ttl=300)
def cargar_datos(limit=5000):
    try:
        engine = create_engine(DB_CONNECTION)
        df = pd.read_sql(
            f"SELECT * FROM mediciones_aire ORDER BY fecha ASC LIMIT {limit}",
            engine
        )
        df['fecha'] = pd.to_datetime(df['fecha'])
        # Limpieza básica
        df = df.dropna(subset=['pm10', 'pm2_5', 'dust'])
        df = df.sort_values('fecha')
        return df
    except Exception as e:
        st.warning("No se pudo conectar con la base de datos o cargar datos.")
        return pd.DataFrame()

def obtener_estado(pm10):
    if pm10 <= 20: return "Excelente", "#21C18D"
    elif pm10 <= 50: return "Bueno", "#2BBE72"
    elif pm10 <= 100: return "Moderado", "#E7B03A"
    elif pm10 <= 200: return "Malo", "#E07B2C"
    else: return "Severo", "#D84B4B"

def aqi_simple(pm10, pm25):
    # Índice simple para comunicación (no regulatorio)
    return max(pm25 * 1.4, pm10 * 0.9)

def plot_timeline(df, rango=None):
    dfx = df.copy()
    if rango:
        dfx = dfx[(dfx['fecha'] >= rango[0]) & (dfx['fecha'] <= rango[1])]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dfx['fecha'], y=dfx['pm10'], name='PM10',
        mode='lines', line=dict(color='#56B1F2', width=2.6)
    ))
    fig.add_trace(go.Scatter(
        x=dfx['fecha'], y=dfx['pm2_5'], name='PM2.5',
        mode='lines', line=dict(color='#7F8CFF', width=2.6)
    ))
    fig.add_trace(go.Scatter(
        x=dfx['fecha'], y=dfx['dust'], name='Polvo',
        mode='lines', line=dict(color='#E96A97', width=1.8, dash='dot')
    ))
    # Bandas guía discretas
    fig.add_hline(y=50, line_dash="dot", line_color="#8F9BAA")
    fig.add_hline(y=100, line_dash="dot", line_color="#8F9BAA")
    fig.update_layout(
        height=420,
        paper_bgcolor="#0F141B", plot_bgcolor="#121820",
        font=dict(color="#E6E8EB"),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(gridcolor="#1C2430"),
        yaxis=dict(gridcolor="#1C2430"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="#0F141B", bordercolor="#1C2430", borderwidth=1)
    )
    return fig

def plot_heatmap(df):
    dfh = df.copy()
    dfh['hora'] = dfh['fecha'].dt.hour
    dfh['dia'] = dfh['fecha'].dt.day_name()
    # Orden internacional en inglés para consistencia
    order_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    dfh['dia'] = pd.Categorical(dfh['dia'], categories=order_days, ordered=True)
    # CORRECCIÓN: añadir observed=False para evitar la advertencia de pandas
    pivot = dfh.pivot_table(values='pm10', index='dia', columns='hora', aggfunc='mean', observed=False)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index.astype(str),
        colorscale='Viridis',
        colorbar=dict(title="PM10")
    ))
    fig.update_layout(
        title=None, height=420,
        paper_bgcolor="#0F141B", plot_bgcolor="#121820", font=dict(color="#E6E8EB"),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor="#1C2430"),
        yaxis=dict(gridcolor="#1C2430")
    )
    return fig

def plot_distribution(df):
    fig = px.box(
        df.melt(id_vars='fecha', value_vars=['pm10','pm2_5','dust'], var_name='variable', value_name='valor'),
        x='variable', y='valor', color='variable',
        color_discrete_map={'pm10':'#56B1F2','pm2_5':'#7F8CFF','dust':'#E96A97'}
    )
    fig.update_layout(
        height=420, paper_bgcolor="#0F141B", plot_bgcolor="#121820",
        font=dict(color="#E6E8EB"), margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor="#1C2430"), yaxis=dict(gridcolor="#1C2430"), showlegend=False
    )
    return fig

def create_kepler_map(df):
    # Construye una capa hexbin y puntos si hay lat/lon (simulamos Maspalomas si no hay)
    base_lat, base_lon = 27.9576, -15.5995
    if 'lat' not in df.columns or 'lon' not in df.columns:
        dfg = df.copy()
        dfg['lat'] = base_lat + np.random.normal(0, 0.02, len(dfg))
        dfg['lon'] = base_lon + np.random.normal(0, 0.02, len(dfg))
    else:
        dfg = df.copy()

    m = KeplerGl(height=520, data={"mediciones": dfg})
    # Configuración visual básica sobria (se puede exportar desde Kepler y pegar aquí)
    # Para un setup instantáneo, dejamos que Kepler detecte columnas automáticamente.
    return m

def create_pydeck_map(df):
    # Mapa elegante de pydeck centrado en Maspalomas
    ultimo = df.iloc[-1]
    lat, lon = 27.9576, -15.5995
    radius = float(max(250, min(2000, ultimo['pm10'] * 80)))

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame({"lat":[lat], "lon":[lon], "pm10":[ultimo['pm10']], "pm25":[ultimo['pm2_5']]}),
        get_position='[lon, lat]',
        get_radius=radius,
        get_fill_color='[86,177,242,160]',  # azul suave
        stroked=True, get_line_color='[42,54,70]'
    )
    text_layer = pdk.Layer(
        "TextLayer",
        data=pd.DataFrame({"lat":[lat], "lon":[lon], "text":[f"PM10 {ultimo['pm10']:.1f} • PM2.5 {ultimo['pm2_5']:.1f}"]}),
        get_position='[lon, lat]', get_text='text',
        get_color='[230,232,235,220]', get_size=16
    )
    view = pdk.ViewState(latitude=lat, longitude=lon, zoom=10.5, pitch=35, bearing=0)
    return pdk.Deck(layers=[layer, text_layer], initial_view_state=view, map_style='mapbox://styles/mapbox/dark-v10')

def main():
    # ---------------------------------------------------------------------------------------
    # Sidebar — Filtros y opciones
    # ---------------------------------------------------------------------------------------
    st.sidebar.markdown("<div class='title-md'>CanaryAir Studio</div>", unsafe_allow_html=True)
    st.sidebar.write("Panel de análisis elegante y profesional para calima y calidad del aire.")
    
    df = cargar_datos(limit=5000)
    if df.empty:
        st.error("No hay datos disponibles. Verifica la conexión a PostgreSQL.")
        st.stop()
    
    min_date = df['fecha'].min().date()
    max_date = df['fecha'].max().date()
    
    rango = st.sidebar.date_input(
        "Rango de fechas",
        value=(max(min_date, max_date - timedelta(days=7)), max_date),
        min_value=min_date, max_value=max_date
    )
    
    live_mode = st.sidebar.checkbox("Modo en vivo (auto-actualización cada 60s)", value=False)
    if live_mode:
        st.cache_data.clear()
        if st.sidebar.button("Forzar refresh"):
            st.rerun()
        
        # Auto-refresh cada 60 segundos
        import time
        time.sleep(60)
        st.rerun()
    
    # ---------------------------------------------------------------------------------------
    # Encabezado
    # ---------------------------------------------------------------------------------------
    st.markdown("<div class='title-xl'>🌬️ CanaryAir Studio</div>", unsafe_allow_html=True)
    st.write("Un dashboard sobrio y profesional para monitorizar PM10, PM2.5 y polvo en Gran Canaria.")
    
    # ---------------------------------------------------------------------------------------
    # KPIs principales
    # ---------------------------------------------------------------------------------------
    mask = (df['fecha'].dt.date >= rango[0]) & (df['fecha'].dt.date <= rango[1])
    df_sel = df.loc[mask].copy()
    df_sel = df_sel if len(df_sel) > 0 else df.copy()
    
    ultimo = df_sel.iloc[-1]
    estado, color_estado = obtener_estado(ultimo['pm10'])
    aqi = aqi_simple(ultimo['pm10'], ultimo['pm2_5'])
    prom_24_pm10 = df_sel.tail(24)['pm10'].mean() if len(df_sel) >= 24 else df_sel['pm10'].mean()
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Última lectura", ultimo['fecha'].strftime('%Y-%m-%d %H:%M'), None)
    with c2:
        delta_pm10 = ultimo['pm10'] - df_sel.iloc[-2]['pm10'] if len(df_sel) > 1 else 0
        st.metric("PM10 (µg/m³)", f"{ultimo['pm10']:.1f}", f"{delta_pm10:+.1f}")
    with c3:
        delta_pm25 = ultimo['pm2_5'] - df_sel.iloc[-2]['pm2_5'] if len(df_sel) > 1 else 0
        st.metric("PM2.5 (µg/m³)", f"{ultimo['pm2_5']:.1f}", f"{delta_pm25:+.1f}")
    with c4:
        st.metric("Polvo (µg/m³)", f"{ultimo['dust']:.1f}", f"Ø 24h {prom_24_pm10:.1f}")
    with c5:
        st.metric("AQI (comunicativo)", f"{aqi:.0f}", estado)
    
    st.markdown(
        f"<div class='soft' style='border-left: 4px solid {color_estado}; margin-top: 10px;'>"
        f"<b>Estado actual:</b> {estado}. Rango visual guiado: 50/100 µg/m³ como bandas de referencia.</div>",
        unsafe_allow_html=True
    )
    
    # ---------------------------------------------------------------------------------------
    # Visualización
    # ---------------------------------------------------------------------------------------
    tab1, tab2, tab3 = st.tabs(["Evolución temporal", "Mapa geoespacial", "Patrones y distribución"])
    
    with tab1:
        st.plotly_chart(plot_timeline(df_sel), width='stretch')
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("PM10 máximo", f"{df_sel['pm10'].max():.1f}")
        with m2:
            st.metric("PM10 promedio", f"{df_sel['pm10'].mean():.1f}")
        with m3:
            st.metric("PM10 mínimo", f"{df_sel['pm10'].min():.1f}")
        with m4:
            st.metric("Std PM10", f"{df_sel['pm10'].std():.1f}")
    
    with tab2:
        col_map1, col_map2 = st.columns([2, 1])
        with col_map1:
            st.markdown("<div class='title-md'>Mapa interactivo</div>", unsafe_allow_html=True)
            if KEPLER_AVAILABLE:
                st.info("Kepler.gl activado: visual geoespacial avanzada.")
                kmap = create_kepler_map(df_sel)
                skgl.keplergl_static(kmap)
            else:
                st.info("Kepler.gl no disponible. Mostrando mapa elegante con PyDeck.")
                st.pydeck_chart(create_pydeck_map(df_sel), width='stretch')
        with col_map2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='title-md'>Ubicación</div>", unsafe_allow_html=True)
            st.write("- Zona: Maspalomas, Gran Canaria")
            st.write("- Coordenadas: 27.96°N, 15.60°W")
            st.write("- Frecuencia: actualización horaria")
            st.write("- Origen de datos: PostgreSQL")
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        colp1, colp2 = st.columns(2)
        with colp1:
            st.markdown("<div class='title-md'>Mapa de calor (PM10)</div>", unsafe_allow_html=True)
            if len(df_sel) >= 24:
                st.plotly_chart(plot_heatmap(df_sel), width='stretch')
            else:
                st.warning("Se necesitan al menos 24 horas de datos para el heatmap.")
        with colp2:
            st.markdown("<div class='title-md'>Distribución</div>", unsafe_allow_html=True)
            st.plotly_chart(plot_distribution(df_sel), width='stretch')
    
    # ---------------------------------------------------------------------------------------
    # Comparativa de periodos
    # ---------------------------------------------------------------------------------------
    st.markdown("<div class='title-md' style='margin-top: 18px;'>Comparativa</div>", unsafe_allow_html=True)
    colc1, colc2 = st.columns(2)
    
    with colc1:
        dias_a = st.slider("Periodo A (días hacia atrás)", min_value=1, max_value=14, value=7)
        ini_a = df['fecha'].max() - timedelta(days=dias_a)
        df_a = df[(df['fecha'] >= ini_a) & (df['fecha'] <= df['fecha'].max())]
        fig_a = plot_timeline(df_a)
        fig_a.update_layout(title="Periodo A (reciente)")
        st.plotly_chart(fig_a, width='stretch')
        st.metric("Promedio PM10 A", f"{df_a['pm10'].mean():.1f}")
    
    with colc2:
        dias_b = st.slider("Periodo B (días hacia atrás desde A)", min_value=1, max_value=14, value=7)
        fin_b = ini_a
        ini_b = fin_b - timedelta(days=dias_b)
        df_b = df[(df['fecha'] >= ini_b) & (df['fecha'] <= fin_b)]
        fig_b = plot_timeline(df_b)
        fig_b.update_layout(title="Periodo B (previo)")
        st.plotly_chart(fig_b, width='stretch')
        st.metric("Promedio PM10 B", f"{df_b['pm10'].mean():.1f}" if len(df_b) else "—")
    
    # Delta comparativo
    if len(df_a) and len(df_b):
        delta_comp = df_a['pm10'].mean() - df_b['pm10'].mean()
        st.markdown(
            f"<div class='soft' style='border-left: 4px solid #3A4B62;'>"
            f"<b>Cambio entre periodos:</b> {delta_comp:+.1f} µg/m³ en PM10.</div>",
            unsafe_allow_html=True
        )
    
    # ---------------------------------------------------------------------------------------
    # Datos recientes y exportación
    # ---------------------------------------------------------------------------------------
    st.markdown("<div class='title-md' style='margin-top: 18px;'>Datos recientes</div>", unsafe_allow_html=True)
    t1, t2 = st.columns([3, 1])
    
    with t1:
        df_display = df_sel.tail(30)[['fecha','pm10','pm2_5','dust']].copy()
        df_display['fecha'] = df_display['fecha'].dt.strftime('%Y-%m-%d %H:%M')
        df_display.columns = ['Fecha','PM10 (µg/m³)','PM2.5 (µg/m³)','Polvo (µg/m³)']
        st.dataframe(df_display, width='stretch', height=460)
    
    with t2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='title-md'>Exportar</div>", unsafe_allow_html=True)
        csv = df_sel.to_csv(index=False)
        st.download_button("Descargar CSV", csv, file_name=f"canaryair_{datetime.now().strftime('%Y%m%d')}.csv")
        json_data = df_sel.to_json(orient='records', date_format='iso')
        st.download_button("Descargar JSON", json_data, file_name=f"canaryair_{datetime.now().strftime('%Y%m%d')}.json", mime="application/json")
        # Exportación de figuras como PNG (opcional, requiere kaleido)
        try:
            fig = plot_timeline(df_sel)
            import io
            import plotly.io as pio
            buf = io.BytesIO()
            pio.write_image(fig, buf, format="png", width=1200, height=500, scale=2)
            st.download_button("Timeline PNG", buf.getvalue(), file_name="timeline.png", mime="image/png")
        except Exception:
            st.caption("Para exportar PNG instala 'kaleido'.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------------------------------------
    # Footer
    # ---------------------------------------------------------------------------------------
    st.markdown(
        "<div style='margin-top: 24px; color:#9AA6B2;'>"
        "CanaryAir Studio · Diseño elegante y profesional · Gran Canaria"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()