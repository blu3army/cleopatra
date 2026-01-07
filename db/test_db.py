from sqlalchemy import text
from db.engine import engine

# ajustá import según tu estructura

def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a PostgreSQL")
    except Exception as e:
        print("❌ Error al conectar a PostgreSQL:")
        print(e)


test_connection()