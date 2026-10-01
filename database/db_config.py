from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base , sessionmaker
from config.settings import settings


DB_URL = settings.DB_URL

Base = declarative_base()

engine = create_engine(DB_URL)

session = sessionmaker(bind=engine,autoflush=False)


def get_session():
    try:
        db = session()
        yield db
    finally:
        db.close()




