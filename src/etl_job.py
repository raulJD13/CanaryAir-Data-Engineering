import requests
import pandas as pd
from sqlalchemy import create_engine, text
import os
# --- CONFIGURACIÓN ---
# Usamos el puerto 5433 que configuramos antes

if os.getenv('AM_I_IN_DOCKER'):
    # Configuración interna (Docker a Docker)
    DB_HOST = "db"
    DB_PORT = "5432"
else:
    # Configuración externa (Tu Mac a Docker)
    DB_HOST = "localhost"
    DB_PORT = "5433"

DB_CONNECTION = f"postgresql://admin_canary:CanaryIslands2025!@{DB_HOST}:{DB_PORT}/canaryair"

LAT = 27.9576
LON = -15.5995

def run_etl():
    print(" Iniciando proceso ETL (Extract-Transform-Load)...")
    
    # 1. EXTRACT
    print(" Descargando datos de Open-Meteo...")
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
        print(f" Datos transformados: {len(df)} registros listos.")

        # 3. LOAD
        print(" Conectando a Base de Datos...")
        engine = create_engine(DB_CONNECTION)
        
        registros_nuevos = 0
        
        with engine.connect() as conn:
            for index, row in df.iterrows():
                # Usamos la función text() y parámetros con nombre (:fecha) para seguridad
                sql = text("""
                    INSERT INTO mediciones_aire (fecha, pm10, pm2_5, dust)
                    VALUES (:fecha, :pm10, :pm2_5, :dust)
                    ON CONFLICT (fecha) DO NOTHING;
                """)
                
                # Pasamos los datos como diccionario
                parametros = {
                    "fecha": row['fecha'],
                    "pm10": row['pm10'],
                    "pm2_5": row['pm2_5'],
                    "dust": row['dust']
                }
                
                result = conn.execute(sql, parametros)
                if result.rowcount > 0:
                    registros_nuevos += 1
            
            # ¡IMPORTANTE! Confirmar los cambios
            conn.commit()
                    
        print(f" ÉXITO: Se han guardado {registros_nuevos} registros nuevos en la base de datos.")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    run_etl()