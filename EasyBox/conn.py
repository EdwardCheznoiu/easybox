import psycopg2
DB_HOST = "localhost"
DB_NAME = "easybox"
DB_USER = "postgres"
DB_PASS = "dragondemort1"
DB_PORT = "5432"
 
try:
    conn = psycopg2.connect(
            host = DB_HOST,
            database = DB_NAME,
            user = DB_USER,
            password = DB_PASS,
            port = DB_PORT
        )
    print("Connected")
except:
    print("Something went wrong")
