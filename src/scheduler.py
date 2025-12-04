import schedule
import time
from etl_job import run_etl
from datetime import datetime

def job():
    print(f" [SCHEDULER] Iniciando tarea programada: {datetime.now()}")
    run_etl()
    print(f" [SCHEDULER] Tarea finalizada. Durmiendo hasta la próxima...")

# Configuración: Ejecutar cada 1 hora
# (Para probarlo ahora, puedes cambiarlo a .seconds.do(job) y poner 60 segundos)
schedule.every(1).hours.do(job)

print(" SCHEDULER INICIADO. Esperando a la siguiente ventana de ejecución...")

# Ejecutamos una vez al arrancar para no esperar 1 hora vacía
job()

while True:
    schedule.run_pending()
    time.sleep(1)