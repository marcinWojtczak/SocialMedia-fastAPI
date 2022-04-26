from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import psycopg2
from config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@" \
                          f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# function that constructs a base class for declarative class
Base = declarative_base()


# Dependency every time we get request we get a session with db and be able to send sql statement do db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         # Connect to database with psycopg2
#         conn = psycopg2.connect(host='127.0.0.1',
#                                 database='socialmedia2',
#                                 user='postgres',
#                                 password="342110",
#                                 cursor_factory=RealDictCursor)
#         #  Open a cursor to perform database operations
#         cursor = conn.cursor()
#         print('Database connection was successfully')
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error:", error)