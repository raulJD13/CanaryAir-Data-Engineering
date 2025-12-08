import requests
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv  # <--- IMPORTANTE: Para leer el archivo .env

# Cargar variables del archivo .env (si existe)
load_dotenv()

# --- CONFIGURACIÓN DE CONEXIÓN (Lógica de Prioridad) ---

# 1. Intentamos leer la URL de la Nube del archivo .env
CLOUD_URL = os.getenv('DATABASE_URL_CLOUD')
AM_I_IN_DOCKER = os.getenv('AM_I_IN_DOCKER')

if CLOUD_URL:
    print("☁️ MODO: NUBE (Neon.tech). Usando credenciales del .env")
    DB_CONNECTION = CLOUD_URL
elif AM_I_IN_DOCKER:
    print("🐳 MODO: DOCKER INTERNO. Conectando al contenedor 'db'...")
    DB_CONNECTION = "postgresql://admin_canary:CanaryIslands2025!@db:5432/canaryair"
else:
    print("💻 MODO: LOCALHOST (Mac). Conectando a Docker desde fuera...")
    DB_CONNECTION = "postgresql://admin_canary:CanaryIslands2025!@localhost:5433/canaryair"

# Coordenadas (Gran Canaria)
LAT = 27.9576
LON = -15.5995

def run_etl():
    print("🚀 Iniciando proceso ETL...")
    
    # 1. EXTRACT
    print("📡 Descargando datos de Open-Meteo...")
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "hourly": ["pm10", "pm2_5", "dust"],
        "timezone": "Europe/London",
        "past_days": 1
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Buena práctica: lanza error si la API falla (404/500)
        data = response.json()
        
        # 2. TRANSFORM
        hourly = data['hourly']
        df = pd.DataFrame({
            'fecha': hourly['time'],
            'pm10': hourly['pm10'],
            'pm2_5': hourly['pm2_5'],
            'dust': hourly['dust']
        })
        
        df['fecha'] = pd.to_datetime(df['fecha'])
        print(f"📊 Datos transformados: {len(df)} registros listos.")

        # 3. LOAD
        print(f"💾 Conectando a Base de Datos...")
        engine = create_engine(DB_CONNECTION)

        # --- AUTO-CREACIÓN DE TABLA (Idempotencia) ---
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS mediciones_aire (
                    id SERIAL PRIMARY KEY,
                    fecha TIMESTAMP NOT NULL,
                    pm10 FLOAT,
                    pm2_5 FLOAT,
                    dust FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_fecha UNIQUE (fecha)
                );
            """))
            conn.commit()
            # print("✅ Tabla verificada.") # Comentado para no ensuciar logs

        registros_nuevos = 0
        
        with engine.connect() as conn:
            for index, row in df.iterrows():
                sql = text("""
                    INSERT INTO mediciones_aire (fecha, pm10, pm2_5, dust)
                    VALUES (:fecha, :pm10, :pm2_5, :dust)
                    ON CONFLICT (fecha) DO NOTHING;
                """)
                
                parametros = {
                    "fecha": row['fecha'],
                    "pm10": row['pm10'],
                    "pm2_5": row['pm2_5'],
                    "dust": row['dust']
                }
                
                result = conn.execute(sql, parametros)
                if result.rowcount > 0:
                    registros_nuevos += 1
            
            conn.commit()
                    
        print(f"✅ ÉXITO: Se han guardado {registros_nuevos} registros nuevos.")
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO EN ETL: {e}")

if __name__ == "__main__":
    run_etl()