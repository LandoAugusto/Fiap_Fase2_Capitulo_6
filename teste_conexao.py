from dotenv import load_dotenv
import oracledb
import os

# Carregar variáveis do .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SID = os.getenv("DB_SID")

# Montar o DSN
dsn = f"{DB_HOST}:{DB_PORT}/{DB_SID}"

try:
    print("Tentando conectar ao Oracle...")
    conn = oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=dsn
    )
    print("✅ Conexão bem-sucedida com o banco Oracle!")
    conn.close()
except oracledb.Error as e:
    print("❌ Erro ao conectar ao Oracle:")
    print(e)