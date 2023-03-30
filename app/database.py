from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Esta clase BASE de sqlAlchemy permite crear las tablas en la base de datos
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#este código usa la librería psycopg2 para conectar a la base de datos, pero nosotros
#finalmente escogimos sqlalquemy para esta conexión. Lo dejamos aquí (traído desde main.py) para conservar 
#este código por si alguna vez lo necesitamos

# while True: #    rating: Optional[int] = None
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres',
#         password= '1postgresLocal', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull")
#         break #salimos del bucle si hay conexión exitosa
#     except Exception as error: 
#         print ("Connecting to database failed")
#         print ("The error was:", error)
#         time.sleep(2) #esperará dos segundos antes de continuar con otro intento

