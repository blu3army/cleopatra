from sqlalchemy import text
from db.engine import engine

# ajustá import según tu estructura

def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a MariaDB")
    except Exception as e:
        print("❌ Error al conectar a MariaDB:")
        print(e)


test_connection()