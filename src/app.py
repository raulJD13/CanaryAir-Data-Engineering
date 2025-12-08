# CanaryAir Studio — Dashboard profesional y elegante
# Requisitos recomendados:
# pip install streamlit pandas sqlalchemy plotly
# pip install -U kaleido (opcional para exportar PNG)

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ---------------------------------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------------------------------
st.set_page_config(
    page_title="CanaryAir Studio",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema elegante sobrio con mejor contraste
st.markdown("""
<style>
    /* Tipografía elegante y colores discretos */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, .stApp { 
        font-family: 'Inter', sans-serif;
        background: #0F141B;
        color: #E6E8EB;
    }
    
    /* Mejor contraste para textos */
    .stMarkdown, .stText, .stWrite {
        color: #E6E8EB !important;
    }
    
    /* Textos en sidebar más legibles */
    .css-1d391kg, .css-1v3fvcr, .css-1lcbmhc {
        color: #CBD5E1 !important;
    }
    
    /* Contenedores con mejor contraste */
    .card {
        background: #121820;
        border: 1px solid #2A3646;
        border-radius: 16px;
        padding: 24px;
        color: #E6E8EB;
    }
    .soft {
        background: #131A24;
        border: 1px solid #263040;
        border-radius: 12px;
        padding: 20px;
        color: #E6E8EB;
    }
    
    /* Títulos con mejor contraste */
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    .title-xl {
        font-size: 36px; 
        font-weight: 700; 
        letter-spacing: -0.02em;
        color: #FFFFFF !important;
        margin-bottom: 8px;
    }
    
    .title-md {
        font-size: 22px; 
        font-weight: 600; 
        letter-spacing: -0.01em;
        color: #FFFFFF !important;
        margin-bottom: 12px;
    }
    
    .title-sm {
        font-size: 16px;
        font-weight: 500;
        color: #CBD5E1 !important;
        margin-bottom: 8px;
    }
    
    /* Mejorar métricas */
    div[data-testid="stMetric"] {
        background: #121820;
        border: 1px solid #2A3646;
        border-radius: 14px;
        padding: 20px 16px;
    }
    
    div[data-testid="stMetric"] label {
        color: #9AA6B2 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stMetricDelta"] {
        font-size: 14px !important;
        font-weight: 500 !important;
    }
    
    /* Mejorar tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; 
        background: #11171E; 
        border: 1px solid #2A3646;
        padding: 8px; 
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #9AA6B2 !important;
        font-weight: 500;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: #1A2433 !important;
        color: #FFFFFF !important;
        border: 1px solid #3A4B62;
    }
    
    /* Dataframes mejorados */
    .stDataFrame {
        background: #11171E;
        border: 1px solid #2A3646;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Mejorar inputs */
    .stSelectbox, .stSlider, .stDateInput {
        color: #E6E8EB !important;
    }
    
    .st-bd, .st-ae, .st-ag {
        color: #E6E8EB !important;
    }
    
    /* Tooltips y popovers */
    .stTooltip {
        background: #1A2433 !important;
        color: #E6E8EB !important;
        border: 1px solid #2A3646 !important;
    }
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

# Nuevas funciones para análisis estadístico
def plot_correlation_matrix(df):
    # Calcular correlaciones
    corr_matrix = df[['pm10', 'pm2_5', 'dust']].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 14},
        hoverongaps=False
    ))
    
    fig.update_layout(
        height=500,
        paper_bgcolor="#0F141B",
        plot_bgcolor="#121820",
        font=dict(color="#E6E8EB", size=12),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            tickangle=45,
            gridcolor="#1C2430",
            title_font=dict(size=14)
        ),
        yaxis=dict(
            gridcolor="#1C2430",
            title_font=dict(size=14)
        ),
        title=dict(
            text="Matriz de Correlación entre Variables",
            font=dict(size=18, color="#FFFFFF"),
            x=0.5
        )
    )
    
    # Configurar la barra de color CORRECTAMENTE
    fig.update_coloraxes(
        colorbar=dict(
            title="Correlación",
            tickfont=dict(size=10, color="#E6E8EB")
        )
    )
    
    return fig

def plot_scatter_matrix(df):
    # Crear subplots
    variables = ['pm10', 'pm2_5', 'dust']
    fig = make_subplots(
        rows=len(variables)-1, 
        cols=len(variables)-1,
        subplot_titles=[f"{x} vs {y}" for x in variables[1:] for y in variables[:-1]],
        horizontal_spacing=0.1,
        vertical_spacing=0.1
    )
    
    colors = df['pm10'].values
    color_scale = px.colors.sequential.Viridis
    
    # Agregar scatter plots
    for i, y_var in enumerate(variables[1:], 1):
        for j, x_var in enumerate(variables[:-1], 1):
            if i > j:  # Solo mitad inferior
                fig.add_trace(
                    go.Scatter(
                        x=df[x_var],
                        y=df[y_var],
                        mode='markers',
                        marker=dict(
                            size=5,
                            color=colors,
                            colorscale=color_scale,
                            showscale=(i==1 and j==1),
                            colorbar=dict(title="PM10")
                        ),
                        opacity=0.6,
                        name=f"{x_var} vs {y_var}"
                    ),
                    row=i, col=j
                )
                
                # Agregar línea de tendencia
                z = np.polyfit(df[x_var], df[y_var], 1)
                p = np.poly1d(z)
                x_range = np.linspace(df[x_var].min(), df[x_var].max(), 100)
                fig.add_trace(
                    go.Scatter(
                        x=x_range,
                        y=p(x_range),
                        mode='lines',
                        line=dict(color='#FF6B6B', width=2, dash='dash'),
                        showlegend=False
                    ),
                    row=i, col=j
                )
    
    fig.update_layout(
        height=600,
        paper_bgcolor="#0F141B",
        plot_bgcolor="#121820",
        font=dict(color="#E6E8EB", size=10),
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False,
        title=dict(
            text="Matriz de Dispersión entre Variables",
            font=dict(size=18, color="#FFFFFF"),
            x=0.5
        )
    )
    
    # Actualizar ejes
    for i in range(1, len(variables)):
        for j in range(1, len(variables)):
            fig.update_xaxes(
                gridcolor="#1C2430",
                zerolinecolor="#1C2430",
                row=i, col=j
            )
            fig.update_yaxes(
                gridcolor="#1C2430",
                zerolinecolor="#1C2430",
                row=i, col=j
            )
    
    return fig

def plot_radar_chart(df):
    # Calcular estadísticas normalizadas
    stats = df[['pm10', 'pm2_5', 'dust']].agg(['mean', 'max', 'std']).T
    
    # Normalizar para el radar chart (0-100)
    stats_normalized = (stats['mean'] / stats['max'].max() * 100).fillna(0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=stats_normalized.values,
        theta=stats_normalized.index,
        fill='toself',
        fillcolor='rgba(86, 177, 242, 0.4)',
        line_color='#56B1F2',
        name='Valor Normalizado'
    ))
    
    # Agregar líneas de referencia
    for value in [25, 50, 75]:
        fig.add_trace(go.Scatterpolar(
            r=[value] * len(stats_normalized),
            theta=stats_normalized.index,
            mode='lines',
            line=dict(color='rgba(143, 155, 170, 0.3)', dash='dot'),
            showlegend=False
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="#1C2430",
                tickfont=dict(color="#E6E8EB")
            ),
            angularaxis=dict(
                gridcolor="#1C2430",
                tickfont=dict(color="#E6E8EB")
            ),
            bgcolor="#121820"
        ),
        height=500,
        paper_bgcolor="#0F141B",
        font=dict(color="#E6E8EB"),
        margin=dict(l=40, r=40, t=60, b=40),
        title=dict(
            text="Perfil de Contaminantes (Normalizado)",
            font=dict(size=18, color="#FFFFFF"),
            x=0.5
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(15, 20, 27, 0.8)"
        )
    )
    
    return fig

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
    st.markdown("<div class='title-xl'>CanaryAir Studio</div>", unsafe_allow_html=True)
    st.write("Un dashboard monitorizar PM10, PM2.5 y polvo en Gran Canaria.")
    st.write("PM10 y PM2.5 son partículas en suspensión en el aire. PM10 incluye polvo y polen, mientras que PM2.5 son partículas más finas que penetran más profundamente en los pulmones.")
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
    
    # Línea de estado mejorada
    st.markdown(f"""
    <div class='soft' style='
        border-left: 6px solid {color_estado}; 
        padding: 16px 20px;
        margin: 20px 0;
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.2) 100%);
    '>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h4 style='margin: 0 0 8px 0; color: #FFFFFF;'>Estado Actual: <span style='color: {color_estado}'>{estado}</span></h4>
                <p style='margin: 0; color: #CBD5E1; font-size: 14px;'>
                    PM10: {ultimo['pm10']:.1f} µg/m³ | PM2.5: {ultimo['pm2_5']:.1f} µg/m³ | Polvo: {ultimo['dust']:.1f} µg/m³
                </p>
            </div>
            <div style='text-align: right;'>
                <div style='font-size: 12px; color: #9AA6B2;'>AQI Comunicativo</div>
                <div style='font-size: 24px; font-weight: 700; color: #FFFFFF;'>{aqi:.0f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Barras de progreso para cada contaminante
    st.markdown("<div class='title-sm'>📊 Niveles Actuales (vs Límites)</div>", unsafe_allow_html=True)
    
    # Definir límites
    limites = {
        'pm10': {'excelente': 20, 'bueno': 50, 'moderado': 100, 'malo': 200, 'max': 300},
        'pm2_5': {'excelente': 10, 'bueno': 25, 'moderado': 50, 'malo': 100, 'max': 150},
        'dust': {'excelente': 30, 'bueno': 60, 'moderado': 120, 'malo': 200, 'max': 300}
    }
    
    col_prog1, col_prog2, col_prog3 = st.columns(3)
    
    with col_prog1:
        pm10_pct = min(100, (ultimo['pm10'] / limites['pm10']['max']) * 100)
        st.markdown(f"""
        <div style='margin-bottom: 20px;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                <span style='color: #56B1F2; font-weight: 500;'>PM10</span>
                <span style='color: #FFFFFF; font-weight: 600;'>{ultimo['pm10']:.1f} µg/m³</span>
            </div>
            <div style='background: #1C2430; height: 8px; border-radius: 4px; overflow: hidden;'>
                <div style='background: #56B1F2; height: 100%; width: {pm10_pct}%; border-radius: 4px;'></div>
            </div>
            <div style='display: flex; justify-content: space-between; margin-top: 4px;'>
                <span style='font-size: 11px; color: #8F9BAA;'>0</span>
                <span style='font-size: 11px; color: #8F9BAA;'>{limites['pm10']['max']} µg/m³</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_prog2:
        pm25_pct = min(100, (ultimo['pm2_5'] / limites['pm2_5']['max']) * 100)
        st.markdown(f"""
        <div style='margin-bottom: 20px;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                <span style='color: #7F8CFF; font-weight: 500;'>PM2.5</span>
                <span style='color: #FFFFFF; font-weight: 600;'>{ultimo['pm2_5']:.1f} µg/m³</span>
            </div>
            <div style='background: #1C2430; height: 8px; border-radius: 4px; overflow: hidden;'>
                <div style='background: #7F8CFF; height: 100%; width: {pm25_pct}%; border-radius: 4px;'></div>
            </div>
            <div style='display: flex; justify-content: space-between; margin-top: 4px;'>
                <span style='font-size: 11px; color: #8F9BAA;'>0</span>
                <span style='font-size: 11px; color: #8F9BAA;'>{limites['pm2_5']['max']} µg/m³</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_prog3:
        dust_pct = min(100, (ultimo['dust'] / limites['dust']['max']) * 100)
        st.markdown(f"""
        <div style='margin-bottom: 20px;'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 4px;'>
                <span style='color: #E96A97; font-weight: 500;'>Polvo</span>
                <span style='color: #FFFFFF; font-weight: 600;'>{ultimo['dust']:.1f} µg/m³</span>
            </div>
            <div style='background: #1C2430; height: 8px; border-radius: 4px; overflow: hidden;'>
                <div style='background: #E96A97; height: 100%; width: {dust_pct}%; border-radius: 4px;'></div>
            </div>
            <div style='display: flex; justify-content: space-between; margin-top: 4px;'>
                <span style='font-size: 11px; color: #8F9BAA;'>0</span>
                <span style='font-size: 11px; color: #8F9BAA;'>{limites['dust']['max']} µg/m³</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ---------------------------------------------------------------------------------------
    # Visualización
    # ---------------------------------------------------------------------------------------
    tab1, tab2, tab3 = st.tabs(["Evolución temporal", "Análisis estadístico", "Patrones y distribución"])
    
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
        tab2_1, tab2_2, tab2_3 = st.tabs(["Matriz de Correlación", "Matriz de Dispersión", "Perfil Radar"])
        
        with tab2_1:
            st.markdown("<div class='title-md'>Análisis de Correlación</div>", unsafe_allow_html=True)
            st.write("""
            <div class='soft'>
            <b>Interpretación:</b><br>
            • <span style='color:#56B1F2'>Correlación positiva (+)</span>: Las variables aumentan juntas<br>
            • <span style='color:#E96A97'>Correlación negativa (-)</span>: Una aumenta cuando la otra disminuye<br>
            • <span style='color:#8F9BAA'>Cercano a 0</span>: Poca o ninguna relación
            </div>
            """, unsafe_allow_html=True)
            
            st.plotly_chart(plot_correlation_matrix(df_sel), width='stretch')
            
            # Estadísticas de correlación
            col1, col2, col3 = st.columns(3)
            with col1:
                corr_pm10_pm25 = df_sel['pm10'].corr(df_sel['pm2_5'])
                st.metric("PM10 vs PM2.5", f"{corr_pm10_pm25:.3f}", 
                         "Alta correlación" if abs(corr_pm10_pm25) > 0.7 else "Correlación moderada")
            with col2:
                corr_pm10_dust = df_sel['pm10'].corr(df_sel['dust'])
                st.metric("PM10 vs Polvo", f"{corr_pm10_dust:.3f}",
                         "Fuertemente relacionado" if abs(corr_pm10_dust) > 0.8 else "Relación media")
            with col3:
                corr_pm25_dust = df_sel['pm2_5'].corr(df_sel['dust'])
                st.metric("PM2.5 vs Polvo", f"{corr_pm25_dust:.3f}",
                         "Relación fuerte" if abs(corr_pm25_dust) > 0.7 else "Relación débil")
        
        with tab2_2:
            st.markdown("<div class='title-md'>Matriz de Dispersión</div>", unsafe_allow_html=True)
            st.write("""
            <div class='soft'>
            <b>Visualización de relaciones:</b> Cada punto representa una medición. 
            La línea discontinua muestra la tendencia lineal. El color indica el valor de PM10.
            </div>
            """, unsafe_allow_html=True)
            
            st.plotly_chart(plot_scatter_matrix(df_sel), width='stretch')
            
            # Insights automáticos
            st.markdown("<div class='title-sm'>📌 Insights detectados:</div>", unsafe_allow_html=True)
            
            # Calcular algunas relaciones clave
            if len(df_sel) > 10:
                ratio_pm25_pm10 = (df_sel['pm2_5'] / df_sel['pm10']).mean()
                dust_contribution = (df_sel['dust'] / (df_sel['pm10'] + df_sel['pm2_5'])).mean() * 100
                
                col_ins1, col_ins2 = st.columns(2)
                with col_ins1:
                    st.info(f"**Ratio PM2.5/PM10:** {ratio_pm25_pm10:.2%}\n\n"
                           f"Un ratio alto indica predominio de partículas finas (más peligrosas).")
                with col_ins2:
                    st.info(f"**Contribución del polvo:** {dust_contribution:.1f}%\n\n"
                           f"Porcentaje que representa el polvo en la contaminación total.")
        
        with tab2_3:
            st.markdown("<div class='title-md'>🎯 Perfil Radar</div>", unsafe_allow_html=True)
            st.write("""
            <div class='soft'>
            <b>Comparativa normalizada:</b> Muestra el perfil relativo de cada contaminante.
            Valores más cercanos al borde exterior indican concentraciones más altas.
            </div>
            """, unsafe_allow_html=True)
            
            st.plotly_chart(plot_radar_chart(df_sel), width='stretch')
            
            # Datos adicionales
            col_rad1, col_rad2, col_rad3 = st.columns(3)
            with col_rad1:
                max_pm10 = df_sel['pm10'].max()
                st.metric("PM10 Máx", f"{max_pm10:.1f} µg/m³")
            with col_rad2:
                max_pm25 = df_sel['pm2_5'].max()
                st.metric("PM2.5 Máx", f"{max_pm25:.1f} µg/m³")
            with col_rad3:
                max_dust = df_sel['dust'].max()
                st.metric("Polvo Máx", f"{max_dust:.1f} µg/m³")
    
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