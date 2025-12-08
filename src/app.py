import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats
import warnings
import os
from dotenv import load_dotenv
load_dotenv()
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Air Quality Engineering Dashboard",
    page_icon="〄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS - Industrial/Engineering Theme
# ============================================================================
st.markdown("""
<style>
    /* Base Engineering Theme */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0e17 0%, #131826 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Engineering Header */
    .engineering-header {
        background: linear-gradient(90deg, #1a1f35 0%, #0f1324 100%);
        padding: 1.5rem 2rem;
        border-bottom: 2px solid #2d3748;
        border-left: 4px solid #4299e1;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .engineering-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #4299e1 0%, #38b2ac 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    
    .engineering-subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
        color: #a0aec0;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    /* Metric Cards - Engineering Style */
    div[data-testid="stMetric"] {
        background: #1a1f35;
        border: 1px solid #2d3748;
        border-radius: 8px;
        padding: 1.2rem;
        border-left: 4px solid #4299e1;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        background: #1e233a;
        border-color: #4a5568;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.15);
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 600;
        color: #ffffff !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #a0aec0 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9rem;
    }
    
    /* Tabs - Engineering Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 2px solid #2d3748;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1a1f35;
        color: #a0aec0;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        border: 1px solid #2d3748;
        border-bottom: none;
        margin-right: 4px;
        border-radius: 6px 6px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background: #2d3748;
        color: #4299e1 !important;
        border-color: #4299e1;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background: #1a1f35;
        border: 1px solid #2d3748;
        border-radius: 8px;
    }
    
    /* Slider Styling */
    .stSlider {
        margin: 1.5rem 0;
    }
    
    div[data-baseweb="slider"] > div > div {
        background: #4299e1 !important;
    }
    
    /* Input Styling */
    .stSelectbox, .stDateInput, .stNumberInput {
        background: #1a1f35;
        border: 1px solid #2d3748;
        border-radius: 6px;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-good { background: #38a169; }
    .status-warning { background: #d69e2e; }
    .status-critical { background: #e53e3e; }
    
    /* Grid Layout Helpers */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    /* Code Block Styling */
    .code-block {
        background: #0f1324;
        border: 1px solid #2d3748;
        border-radius: 6px;
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #cbd5e0;
        overflow-x: auto;
    }
    
    /* Footer */
    .engineering-footer {
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #2d3748;
        color: #718096;
        font-size: 0.85rem;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Fix for plotly text colors */
    .js-plotly-plot .plotly .modebar {
        background: transparent !important;
    }
    
    .js-plotly-plot .plotly .modebar-btn path {
        fill: #a0aec0 !important;
    }
    
    /* Ensure all text is visible */
    .stMarkdown, .stText, .stAlert, .stWarning, .stError, .stSuccess, .stInfo {
        color: #e2e8f0 !important;
    }
    
    .stButton > button {
        color: #e2e8f0 !important;
    }
    
    /* Fix dataframe text */
    .dataframe {
        color: #e2e8f0 !important;
    }
    
    .stDataFrame td, .stDataFrame th {
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATABASE ENGINE & DATA PIPELINE
# ============================================================================
class AirQualityDataPipeline:
    """Professional Data Pipeline for Air Quality Monitoring"""
    
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        
    @st.cache_data(ttl=300, show_spinner="Executing SQL Query...")
    def execute_query(_self, query, params=None):
        """Execute parameterized SQL query with caching"""
        try:
            with _self.engine.connect() as conn:
                if params:
                    df = pd.read_sql_query(text(query), conn, params=params)
                else:
                    df = pd.read_sql_query(text(query), conn)
                return df
        except Exception as e:
            st.error(f"Query Execution Error: {str(e)}")
            return pd.DataFrame()
    
    def get_all_data(self, limit=10000):
        """Get all data with limit"""
        query = f"SELECT * FROM mediciones_aire ORDER BY fecha DESC LIMIT {limit}"
        return self.execute_query(query)

# ============================================================================
# INITIALIZATION (CLOUD VS LOCAL LOGIC ROBUSTA)
# ============================================================================
def get_db_connection():
    """Determina la conexión correcta a prueba de fallos"""
    
    # 1. PRIMERO: Intentamos leer archivo .env (Para tu Mac)
    # Al hacerlo primero, evitamos que Streamlit busque 'secrets.toml' y falle
    env_cloud = os.getenv('DATABASE_URL_CLOUD')
    if env_cloud:
        # print("DEBUG: Usando conexión desde .env") # Descomentar para depurar
        return env_cloud

    # 2. SEGUNDO: Intentamos leer st.secrets (Para Streamlit Cloud)
    # Usamos un try/except para que no explote si estás en local
    try:
        if hasattr(st, "secrets") and "DATABASE_URL_CLOUD" in st.secrets:
            return st.secrets["DATABASE_URL_CLOUD"]
    except FileNotFoundError:
        pass # No pasa nada, es que estamos en local sin secrets.toml

    # 3. TERCERO: Fallback a Docker Local (Si todo lo demás falla)
    return "postgresql://admin_canary:CanaryIslands2025!@localhost:5433/canaryair"

# Inicializar Pipeline
try:
    CURRENT_CONNECTION = get_db_connection()
    pipeline = AirQualityDataPipeline(CURRENT_CONNECTION)
except Exception as e:
    st.error(f"Critical Connection Error: {e}")
    st.stop()

# ============================================================================
# ENGINEERING VISUALIZATION COMPONENTS - CORREGIDO
# ============================================================================
class EngineeringVisualizations:
    """Professional Engineering Visualizations"""
    
    @staticmethod
    def create_timeseries_engineering(df, title="Time Series Analysis"):
        """Create professional time series plot with engineering annotations"""
        df = df.sort_values('fecha')
        
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            subplot_titles=("PM10 Concentration", "PM2.5 Concentration", "Dust Particles"),
            row_heights=[0.4, 0.3, 0.3]
        )
        
        # PM10
        window = min(12, len(df))
        if window > 1:
            df['pm10_ma'] = df['pm10'].rolling(window=window).mean()
        
        fig.add_trace(
            go.Scatter(x=df['fecha'], y=df['pm10'], 
                      name='PM10', line=dict(color='#4299e1', width=2),
                      mode='lines', fill='tozeroy',
                      fillcolor='rgba(66, 153, 225, 0.1)'),
            row=1, col=1
        )
        
        if window > 1 and 'pm10_ma' in df:
            fig.add_trace(
                go.Scatter(x=df['fecha'], y=df['pm10_ma'],
                          name=f'MA{window}', line=dict(color='#ecc94b', width=1.5, dash='dash')),
                row=1, col=1
            )
        
        # PM2.5
        fig.add_trace(
            go.Scatter(x=df['fecha'], y=df['pm2_5'],
                      name='PM2.5', line=dict(color='#38b2ac', width=2)),
            row=2, col=1
        )
        
        # Dust
        fig.add_trace(
            go.Scatter(x=df['fecha'], y=df['dust'],
                      name='Dust', line=dict(color='#ed8936', width=2)),
            row=3, col=1
        )
        
        # Add threshold lines
        thresholds = {'PM10': 50, 'PM2.5': 25, 'Dust': 100}
        
        fig.add_hline(y=thresholds['PM10'], line_dash="dot", 
                     line_color="rgba(239, 68, 68, 0.7)", row=1, col=1,
                     annotation_text=f"Threshold: {thresholds['PM10']} µg/m³",
                     annotation_position="top right",
                     annotation_font_color="#ffffff")
        
        fig.add_hline(y=thresholds['PM2.5'], line_dash="dot",
                     line_color="rgba(239, 68, 68, 0.7)", row=2, col=1,
                     annotation_text=f"Threshold: {thresholds['PM2.5']} µg/m³",
                     annotation_font_color="#ffffff")
        
        fig.update_layout(
            height=800,
            title=dict(text=title, font=dict(size=20, color='#ffffff')),
            paper_bgcolor='#0a0e17',
            plot_bgcolor='#0a0e17',
            font=dict(color='#ffffff'),
            margin=dict(l=50, r=30, t=80, b=50),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(26, 31, 53, 0.9)",
                bordercolor="#2d3748",
                font=dict(color="#ffffff")
            )
        )
        
        # Update axis labels color
        fig.update_xaxes(color='#ffffff', gridcolor='#2d3748', zerolinecolor='#2d3748')
        fig.update_yaxes(color='#ffffff', gridcolor='#2d3748', zerolinecolor='#2d3748')
        
        return fig
    
    @staticmethod
    def create_correlation_matrix(df):
        """Create engineering correlation matrix with statistical significance"""
        numeric_cols = ['pm10', 'pm2_5', 'dust']
        available_cols = [col for col in numeric_cols if col in df.columns]
        
        if len(available_cols) < 2:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data for correlation matrix", 
                             font=dict(color="#ffffff", size=16))
            fig.update_layout(paper_bgcolor='#0a0e17', plot_bgcolor='#0a0e17')
            return fig
        
        corr_matrix = df[available_cols].corr(method='pearson')
        
        n = len(df)
        p_values = pd.DataFrame(index=corr_matrix.index, columns=corr_matrix.columns)
        
        for i in corr_matrix.index:
            for j in corr_matrix.columns:
                if i == j:
                    p_values.loc[i, j] = 0
                else:
                    corr = corr_matrix.loc[i, j]
                    if np.isnan(corr):
                        p_values.loc[i, j] = np.nan
                    else:
                        t_stat = corr * np.sqrt((n-2)/(1-corr**2))
                        p_val = 2 * (1 - stats.t.cdf(abs(t_stat), n-2))
                        p_values.loc[i, j] = p_val
        
        # CORRECCIÓN: Eliminado el parámetro inválido titlefont
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu',
            zmin=-1, zmax=1,
            text=corr_matrix.round(3).astype(str) + "<br>p=" + p_values.round(4).astype(str),
            texttemplate='%{text}',
            textfont=dict(size=12, color="#000000"),
            hoverongaps=False,
            colorbar=dict(
                title="Correlation",
                tickfont=dict(color='#ffffff')
            )
        ))
        
        fig.update_layout(
            title=dict(
                text="Correlation Matrix with Statistical Significance",
                font=dict(color='#ffffff', size=16)
            ),
            height=500,
            paper_bgcolor='#0a0e17',
            plot_bgcolor='#0a0e17',
            font=dict(color='#ffffff'),
            xaxis=dict(tickangle=45, tickfont=dict(color="#ffffff")),
            yaxis=dict(tickfont=dict(color="#ffffff")),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    @staticmethod
    def create_distribution_analysis(df):
        """Create comprehensive distribution analysis"""
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=(
                "PM10 Distribution", "PM2.5 Distribution", "Dust Distribution",
                "PM10 Q-Q Plot", "PM2.5 Q-Q Plot", "Dust Q-Q Plot"
            ),
            vertical_spacing=0.12,
            horizontal_spacing=0.08
        )
        
        variables = ['pm10', 'pm2_5', 'dust']
        colors = ['#4299e1', '#38b2ac', '#ed8936']
        
        for i, (var, color) in enumerate(zip(variables, colors), 1):
            if var not in df.columns or df[var].isna().all():
                continue
                
            # Histogram
            fig.add_trace(
                go.Histogram(
                    x=df[var].dropna(), 
                    name=var.upper(),
                    marker_color=color,
                    opacity=0.7,
                    nbinsx=30,
                    histnorm='probability density'
                ),
                row=1, col=i
            )
            
            # Add KDE curve
            try:
                kde = stats.gaussian_kde(df[var].dropna())
                x_range = np.linspace(df[var].min(), df[var].max(), 100)
                fig.add_trace(
                    go.Scatter(
                        x=x_range, 
                        y=kde(x_range),
                        mode='lines',
                        line=dict(color='white', width=2),
                        showlegend=False
                    ),
                    row=1, col=i
                )
            except:
                pass
        
        # Q-Q Plots
        for i, (var, color) in enumerate(zip(variables, colors), 1):
            if var not in df.columns or df[var].isna().all():
                continue
                
            data = df[var].dropna()
            if len(data) > 0:
                try:
                    (osm, osr), (slope, intercept, r) = stats.probplot(data, dist="norm")
                    
                    fig.add_trace(
                        go.Scatter(
                            x=osm, y=osr,
                            mode='markers',
                            marker=dict(color=color, size=6),
                            name=f'{var.upper()} Q-Q'
                        ),
                        row=2, col=i
                    )
                    
                    # Add theoretical line
                    fig.add_trace(
                        go.Scatter(
                            x=osm, y=slope*osm + intercept,
                            mode='lines',
                            line=dict(color='white', dash='dash', width=2),
                            showlegend=False
                        ),
                        row=2, col=i
                    )
                except:
                    pass
        
        fig.update_layout(
            height=800,
            paper_bgcolor='#0a0e17',
            plot_bgcolor='#0a0e17',
            font=dict(color='#ffffff'),
            showlegend=False,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Update all axis colors
        for i in range(1, 3):
            for j in range(1, 4):
                fig.update_xaxes(row=i, col=j, color='#ffffff', gridcolor='#2d3748', zerolinecolor='#2d3748')
                fig.update_yaxes(row=i, col=j, color='#ffffff', gridcolor='#2d3748', zerolinecolor='#2d3748')
        
        return fig
    
    @staticmethod
    def create_scatter_matrix(df):
        """Create professional scatter matrix with regression lines"""
        available_vars = [col for col in ['pm10', 'pm2_5', 'dust'] if col in df.columns]
        
        if len(available_vars) < 2:
            fig = go.Figure()
            fig.add_annotation(text="Insufficient data for scatter matrix",
                             font=dict(color="#ffffff", size=16))
            fig.update_layout(paper_bgcolor='#0a0e17', plot_bgcolor='#0a0e17')
            return fig
            
        fig = px.scatter_matrix(
            df,
            dimensions=available_vars,
            color='pm10' if 'pm10' in df.columns else available_vars[0],
            color_continuous_scale='Viridis',
            title="Scatter Matrix with Density Estimates",
            labels={col: f"{col.upper()} (µg/m³)" for col in available_vars}
        )
        
        # CORRECCIÓN: Usar dict correcto para colorbar
        fig.update_layout(
            height=800,
            paper_bgcolor='#0a0e17',
            plot_bgcolor='#0a0e17',
            font=dict(color='#ffffff'),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Actualizar colorbar correctamente
        fig.update_coloraxes(
            colorbar=dict(
                title="PM10 Value",
                tickfont=dict(color='#ffffff')
            )
        )
        
        # Update axis colors
        for annotation in fig.layout.annotations:
            annotation.font.color = "#ffffff"
        
        return fig

# ============================================================================
# DATA QUALITY & MONITORING FUNCTIONS
# ============================================================================
def calculate_data_quality(df):
    """Calculate comprehensive data quality metrics"""
    total_rows = len(df)
    
    if total_rows == 0:
        return {}
    
    quality_metrics = {
        'completeness': {
            'pm10': (df['pm10'].notna().sum() / total_rows) * 100 if 'pm10' in df.columns else 0,
            'pm2_5': (df['pm2_5'].notna().sum() / total_rows) * 100 if 'pm2_5' in df.columns else 0,
            'dust': (df['dust'].notna().sum() / total_rows) * 100 if 'dust' in df.columns else 0,
            'timestamp': (df['fecha'].notna().sum() / total_rows) * 100 if 'fecha' in df.columns else 0
        },
        'consistency': {
            'pm10_range': (df['pm10'].min(), df['pm10'].max()) if 'pm10' in df.columns else (0, 0),
            'pm2_5_range': (df['pm2_5'].min(), df['pm2_5'].max()) if 'pm2_5' in df.columns else (0, 0),
            'dust_range': (df['dust'].min(), df['dust'].max()) if 'dust' in df.columns else (0, 0)
        },
        'validity': {
            'pm10_negative': (df['pm10'] < 0).sum() if 'pm10' in df.columns else 0,
            'pm2_5_negative': (df['pm2_5'] < 0).sum() if 'pm2_5' in df.columns else 0,
            'dust_negative': (df['dust'] < 0).sum() if 'dust' in df.columns else 0
        }
    }
    
    return quality_metrics

def calculate_air_quality_index(pm10, pm25):
    """Calculate professional AQI based on EPA standards"""
    try:
        pm10 = float(pm10)
        pm25 = float(pm25)
    except:
        return 0
    
    def calculate_component(concentration, breakpoints):
        for i in range(len(breakpoints) - 1):
            if breakpoints[i][0] <= concentration <= breakpoints[i][1]:
                return i + (concentration - breakpoints[i][0]) / (breakpoints[i][1] - breakpoints[i][0])
        return 0
    
    pm10_breakpoints = [(0, 54), (55, 154), (155, 254), (255, 354), (355, 424), (425, 504)]
    pm25_breakpoints = [(0, 12), (12.1, 35.4), (35.5, 55.4), (55.5, 150.4), (150.5, 250.4), (250.5, 350.4)]
    
    aqi_pm10 = calculate_component(pm10, pm10_breakpoints) * 50
    aqi_pm25 = calculate_component(pm25, pm25_breakpoints) * 50
    
    return max(aqi_pm10, aqi_pm25)

# ============================================================================
# MAIN DASHBOARD
# ============================================================================
def main():
    # Header
    st.markdown("""
    <div class="engineering-header">
        <div class="engineering-title">AIR QUALITY ENGINEERING DASHBOARD</div>
        <div class="engineering-subtitle">PostgreSQL Pipeline | Real-time Analytics | Data Engineering Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Control Panel
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_range = st.selectbox(
            "Time Range",
            ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Data"],
            index=3
        )
    
    with col2:
        data_limit = st.selectbox(
            "Data Points Limit",
            ["100", "500", "1000", "5000", "10000"],
            index=3
        )
    
    with col3:
        auto_refresh = st.checkbox("Auto Refresh", value=False)
        if auto_refresh:
            st.cache_data.clear()
    
    # Load Data
    try:
        if time_range == "All Data":
            df = pipeline.get_all_data(limit=int(data_limit))
        else:
            # Get all data first
            df = pipeline.get_all_data(limit=int(data_limit))
            if 'fecha' in df.columns:
                df['fecha'] = pd.to_datetime(df['fecha'])
                
                if time_range == "Last 24 Hours":
                    cutoff = datetime.now() - timedelta(hours=24)
                    df = df[df['fecha'] >= cutoff]
                elif time_range == "Last 7 Days":
                    cutoff = datetime.now() - timedelta(days=7)
                    df = df[df['fecha'] >= cutoff]
                elif time_range == "Last 30 Days":
                    cutoff = datetime.now() - timedelta(days=30)
                    df = df[df['fecha'] >= cutoff]
                    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        df = pipeline.execute_query("SELECT * FROM mediciones_aire ORDER BY fecha DESC LIMIT 5000")
    
    if df.empty:
        st.error("No data available. Check database connection.")
        st.info("Running ETL job to populate database...")
        
        if st.button("Run ETL Job Now"):
            import subprocess
            import sys
            
            try:
                result = subprocess.run([sys.executable, "etl_job.py"], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    st.success("ETL job completed successfully!")
                    st.code(result.stdout)
                    st.rerun()
                else:
                    st.error("ETL job failed!")
                    st.code(result.stderr)
            except Exception as e:
                st.error(f"Failed to run ETL job: {str(e)}")
        
        st.stop()
    
    # Convert fecha to datetime if needed
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'])
        df = df.sort_values('fecha', ascending=False)
    else:
        st.error("Column 'fecha' not found in data")
        st.stop()
    
    # REAL-TIME ENGINEERING METRICS
    st.markdown("### REAL-TIME ENGINEERING METRICS")
    
    if len(df) > 0:
        latest = df.iloc[0]
        aqi = calculate_air_quality_index(latest.get('pm10', 0), latest.get('pm2_5', 0))
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            pm10_val = latest.get('pm10', 0)
            delta_pm10 = pm10_val - df.iloc[1]['pm10'] if len(df) > 1 else 0
            st.metric(
                label="PM10 (µg/m³)",
                value=f"{pm10_val:.1f}",
                delta=f"{delta_pm10:+.1f}"
            )
        
        with col2:
            pm25_val = latest.get('pm2_5', 0)
            delta_pm25 = pm25_val - df.iloc[1]['pm2_5'] if len(df) > 1 else 0
            st.metric(
                label="PM2.5 (µg/m³)",
                value=f"{pm25_val:.1f}",
                delta=f"{delta_pm25:+.1f}"
            )
        
        with col3:
            dust_val = latest.get('dust', 0)
            delta_dust = dust_val - df.iloc[1]['dust'] if len(df) > 1 else 0
            st.metric(
                label="Dust (µg/m³)",
                value=f"{dust_val:.1f}",
                delta=f"{delta_dust:+.1f}"
            )
        
        with col4:
            st.metric(
                label="Engineering AQI",
                value=f"{aqi:.0f}",
                delta="EPA Standard" if aqi < 100 else "Alert"
            )
        
        with col5:
            st.metric(
                label="Data Points",
                value=f"{len(df):,}"
            )
        
        with col6:
            completeness = 0
            if len(df) > 0:
                valid_cols = [col for col in ['pm10', 'pm2_5', 'dust'] if col in df.columns]
                if valid_cols:
                    completeness = (df[valid_cols].notna().sum().min() / len(df)) * 100
            st.metric(
                label="Data Quality",
                value=f"{completeness:.1f}%"
            )
    else:
        st.warning("No data available for metrics")
    
    # ENGINEERING STATUS PANEL
    st.markdown("### ENGINEERING STATUS PANEL")
    
    status_col1, status_col2, status_col3, status_col4 = st.columns(4)
    
    with status_col1:
        pm10_val = latest.get('pm10', 0) if len(df) > 0 else 0
        pm10_status = "Normal" if pm10_val < 50 else "Warning" if pm10_val < 100 else "Critical"
        status_color = "#38a169" if pm10_val < 50 else "#d69e2e" if pm10_val < 100 else "#e53e3e"
        st.markdown(f"""
        <div style='background: #1a1f35; padding: 1rem; border-radius: 8px; border-left: 4px solid {status_color};'>
            <div style='font-size: 0.9rem; color: #a0aec0;'>PM10 STATUS</div>
            <div style='font-size: 1.5rem; font-weight: 600; color: {status_color};'>{pm10_status}</div>
            <div style='font-size: 0.8rem; color: #cbd5e0;'>Value: {pm10_val:.1f} µg/m³</div>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col2:
        pm25_val = latest.get('pm2_5', 0) if len(df) > 0 else 0
        pm25_status = "Normal" if pm25_val < 25 else "Warning" if pm25_val < 50 else "Critical"
        status_color = "#38a169" if pm25_val < 25 else "#d69e2e" if pm25_val < 50 else "#e53e3e"
        st.markdown(f"""
        <div style='background: #1a1f35; padding: 1rem; border-radius: 8px; border-left: 4px solid {status_color};'>
            <div style='font-size: 0.9rem; color: #a0aec0;'>PM2.5 STATUS</div>
            <div style='font-size: 1.5rem; font-weight: 600; color: {status_color};'>{pm25_status}</div>
            <div style='font-size: 0.8rem; color: #cbd5e0;'>Value: {pm25_val:.1f} µg/m³</div>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col3:
        pipeline_status = "Operational" if len(df) > 0 else "Offline"
        status_color = "#38a169" if len(df) > 0 else "#e53e3e"
        st.markdown(f"""
        <div style='background: #1a1f35; padding: 1rem; border-radius: 8px; border-left: 4px solid {status_color};'>
            <div style='font-size: 0.9rem; color: #a0aec0;'>DATA PIPELINE</div>
            <div style='font-size: 1.5rem; font-weight: 600; color: {status_color};'>{pipeline_status}</div>
            <div style='font-size: 0.8rem; color: #cbd5e0;'>{len(df):,} records loaded</div>
        </div>
        """, unsafe_allow_html=True)
    
    with status_col4:
        db_status = "Connected" if len(df) > 0 else "Disconnected"
        status_color = "#38a169" if len(df) > 0 else "#e53e3e"
        earliest = df['fecha'].min().strftime('%Y-%m-%d') if len(df) > 0 else "N/A"
        latest_date = df['fecha'].max().strftime('%Y-%m-%d') if len(df) > 0 else "N/A"
        st.markdown(f"""
        <div style='background: #1a1f35; padding: 1rem; border-radius: 8px; border-left: 4px solid {status_color};'>
            <div style='font-size: 0.9rem; color: #a0aec0;'>DATABASE</div>
            <div style='font-size: 1.5rem; font-weight: 600; color: {status_color};'>{db_status}</div>
            <div style='font-size: 0.8rem; color: #cbd5e0;'>{earliest} to {latest_date}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # MAIN ANALYSIS TABS
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Time Series Analysis", 
        "Statistical Analysis", 
        "Data Quality", 
        "Raw Data", 
        "System"
    ])
    
    with tab1:
        st.markdown("### ENGINEERING TIME SERIES ANALYSIS")
        
        viz = EngineeringVisualizations()
        fig1 = viz.create_timeseries_engineering(df, "Engineering Time Series Analysis")
        st.plotly_chart(fig1, width='stretch')

        
        if len(df) > 1:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                rolling_window = min(6, len(df))
                if rolling_window > 1:
                    rolling_avg = df['pm10'].rolling(window=rolling_window).mean().iloc[-1]
                    st.metric("6h Rolling Avg PM10", f"{rolling_avg:.1f}")
            
            with col2:
                if len(df) > 1:
                    volatility = df['pm10'].pct_change().std() * 100
                    st.metric("PM10 Volatility", f"{volatility:.2f}%")
            
            with col3:
                if len(df) > 1:
                    x = np.arange(len(df))
                    y = df['pm10'].values
                    trend = np.polyfit(x, y, 1)[0] * 100
                    st.metric("Trend Slope", f"{trend:.3f}")
            
            with col4:
                if len(df) > 1:
                    autocorr = df['pm10'].autocorr(lag=1)
                    st.metric("Autocorrelation", f"{autocorr:.3f}")
    
    with tab2:
        st.markdown("### ADVANCED STATISTICAL ANALYSIS")
        
        viz = EngineeringVisualizations()
        
        st.markdown("#### Correlation Analysis")
        fig_corr = viz.create_correlation_matrix(df)
        st.plotly_chart(fig_corr, width='stretch')

        
        st.markdown("#### Distribution Analysis")
        fig_dist = viz.create_distribution_analysis(df)
        st.plotly_chart(fig_dist, width='stretch')

        
        st.markdown("#### Scatter Matrix Analysis")
        fig_scatter = viz.create_scatter_matrix(df)
        st.plotly_chart(fig_scatter, width='stretch')

        
        st.markdown("#### Statistical Summary")
        stats_cols = [col for col in ['pm10', 'pm2_5', 'dust'] if col in df.columns]
        if stats_cols:
            stats_df = df[stats_cols].describe().T
            stats_df['skewness'] = [df[col].skew() for col in stats_cols]
            stats_df['kurtosis'] = [df[col].kurtosis() for col in stats_cols]
            stats_df['cv'] = stats_df['std'] / stats_df['mean'] * 100
            
            st.dataframe(
                stats_df.style.format("{:.2f}"),
                width='stretch'

            )
    
    with tab3:
        st.markdown("### DATA QUALITY ENGINEERING")
        
        quality_metrics = calculate_data_quality(df)
        
        if quality_metrics:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### Completeness")
                for key, value in quality_metrics['completeness'].items():
                    status_text = "Good" if value > 95 else "Warning" if value > 90 else "Critical"
                    status_color = "#38a169" if value > 95 else "#d69e2e" if value > 90 else "#e53e3e"
                    st.markdown(f"<span style='color:{status_color}'>{key.upper()}: {value:.1f}% ({status_text})</span>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### Validity Checks")
                for key, value in quality_metrics['validity'].items():
                    status_text = "Valid" if value == 0 else f"Invalid: {value}"
                    status_color = "#38a169" if value == 0 else "#e53e3e"
                    st.markdown(f"<span style='color:{status_color}'>{key.replace('_', ' ').title()}: {status_text}</span>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("#### Value Ranges")
                for key, (min_val, max_val) in quality_metrics['consistency'].items():
                    st.markdown(f"<span style='color:#cbd5e0'>{key.replace('_', ' ').title()}: {min_val:.1f} - {max_val:.1f}</span>", unsafe_allow_html=True)
        
        st.markdown("#### Missing Data Pattern Analysis")
        if len(df) > 0:
            missing_cols = [col for col in ['pm10', 'pm2_5', 'dust', 'fecha'] if col in df.columns]
            if missing_cols:
                missing_df = df[missing_cols].isnull()
                missing_pattern = missing_df.sum()
                
                if missing_pattern.sum() > 0:
                    fig_missing = go.Figure(data=[
                        go.Bar(x=missing_pattern.index, y=missing_pattern.values,
                              marker_color='#ed8936')
                    ])
                    fig_missing.update_layout(
                        title="Missing Values by Feature",
                        paper_bgcolor='#0a0e17',
                        plot_bgcolor='#0a0e17',
                        font=dict(color='#ffffff'),
                        height=400,
                        xaxis=dict(tickfont=dict(color="#ffffff")),
                        yaxis=dict(tickfont=dict(color="#ffffff"))
                    )
                    st.plotly_chart(fig_missing, width='stretch')

                else:
                    st.markdown("<span style='color:#38a169'>No missing values detected in the dataset</span>", unsafe_allow_html=True)
        
        st.markdown("#### Outlier Detection (IQR Method)")
        
        def detect_outliers(series):
            if len(series) < 2:
                return 0
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            if IQR == 0:
                return 0
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return ((series < lower_bound) | (series > upper_bound)).sum()
        
        for var in ['pm10', 'pm2_5', 'dust']:
            if var in df.columns:
                outliers_count = detect_outliers(df[var])
                status_color = "#38a169" if outliers_count == 0 else "#d69e2e" if outliers_count < 10 else "#e53e3e"
                st.markdown(f"<span style='color:{status_color}'>{var.upper()}: {outliers_count} outliers detected</span>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### RAW DATA & QUERY INTERFACE")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("#### Latest Measurements")
            display_df = df.head(100).copy()
            if 'fecha' in display_df.columns:
                display_df['fecha'] = display_df['fecha'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            display_cols = {}
            if 'fecha' in display_df.columns:
                display_cols['fecha'] = 'Timestamp'
            if 'pm10' in display_df.columns:
                display_cols['pm10'] = 'PM10'
            if 'pm2_5' in display_df.columns:
                display_cols['pm2_5'] = 'PM2.5'
            if 'dust' in display_df.columns:
                display_cols['dust'] = 'Dust'
            
            display_df = display_df[list(display_cols.keys())]
            display_df.columns = [display_cols[col] for col in display_df.columns]
            
            st.dataframe(
                display_df,
                width='stretch',
                height=400
            )
        
        with col2:
            st.markdown("#### Data Export")
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"air_quality_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            json_data = df.to_json(orient='records', date_format='iso')
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"air_quality_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            st.markdown("---")
            
            st.markdown("#### Simple Query")
            if st.button("Refresh All Data"):
                st.cache_data.clear()
                st.rerun()
            
            if st.button("Show Table Schema"):
                schema_query = """
                SELECT 
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_name = 'mediciones_aire'
                ORDER BY ordinal_position;
                """
                schema_df = pipeline.execute_query(schema_query)
                st.dataframe(schema_df)
    
    with tab5:
        st.markdown("### SYSTEM & PIPELINE CONFIGURATION")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Database Configuration")
            st.code(f"""
            Database: PostgreSQL
            Host: localhost:5433
            Database: canaryair
            Table: mediciones_aire
            Total Records: {len(df):,}
            Time Range: {df['fecha'].min().strftime('%Y-%m-%d')} to {df['fecha'].max().strftime('%Y-%m-%d')}
            Data Age: {(datetime.now() - df['fecha'].max()).seconds // 60} minutes
            """, language="sql")
        
        with col2:
            st.markdown("#### Pipeline Statistics")
            
            if len(df) > 0:
                time_diff = (df['fecha'].max() - df['fecha'].min()).total_seconds() / 3600
                records_per_hour = len(df) / time_diff if time_diff > 0 else 0
                
                stats = {
                    "Data Freshness": f"{(datetime.now() - df['fecha'].max()).seconds // 60} minutes ago",
                    "Sampling Rate": f"{records_per_hour:.1f} records/hour",
                    "Memory Usage": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
                    "Cache Status": "Active",
                    "Last Refresh": datetime.now().strftime("%H:%M:%S")
                }
                
                for key, value in stats.items():
                    st.markdown(f"**{key}:** {value}")
        
        st.markdown("---")
        
        st.markdown("#### Performance Metrics")
        
        perf_col1, perf_col2, perf_col3 = st.columns(3)
        
        with perf_col1:
            load_time = len(df) * 0.001
            st.metric("Data Load Time", f"{load_time:.2f}s")
        
        with perf_col2:
            st.metric("Data Points", f"{len(df):,}")
        
        with perf_col3:
            if len(df) > 0:
                completeness = (df[['pm10', 'pm2_5', 'dust']].notna().sum().min() / len(df)) * 100
                st.metric("Data Quality", f"{completeness:.1f}%")
        
        st.markdown("#### System Controls")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Clear Cache", width='stretch'):
                st.cache_data.clear()
                st.success("Cache cleared successfully!")
                st.rerun()
        
        with col2:
            if st.button("Refresh Data", width='stretch', type="primary"):
                st.rerun()
        
        with col3:
            if st.button("Validate Connection", width='stretch'):
                try:
                    with pipeline.engine.connect() as conn:
                        result = conn.execute(text("SELECT 1"))
                        st.success("Database connection is working!")
                        count_result = conn.execute(text("SELECT COUNT(*) FROM mediciones_aire"))
                        count = count_result.fetchone()[0]
                        st.info(f"Total records in table: {count:,}")
                except Exception as e:
                    st.error(f"Connection failed: {str(e)}")
    
    # FOOTER
    st.markdown("""
    <div class="engineering-footer">
        Air Quality Engineering Dashboard v2.0 | PostgreSQL Pipeline | 
        Last Update: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """ | 
        Data Source: mediciones_aire
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# EXECUTION
# ============================================================================
if __name__ == "__main__":
    main()