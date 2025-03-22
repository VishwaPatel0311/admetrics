from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DB_CONNECTION


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://{}".format(DB_CONNECTION)


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=30, pool_pre_ping=True)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
