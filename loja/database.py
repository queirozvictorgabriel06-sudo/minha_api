import psycopg
import dotenv
import os

dotenv.load_dotenv()


conexao = psycopg.connect(
    host=os.getenv('DB_HOST'),
    dbname=os.getenv('DB_DATABASE'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    sslmode='require'
)
cursor = conexao.cursor()