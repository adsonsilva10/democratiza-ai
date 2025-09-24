from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    contract_type = Column(String)
    content = Column(String)

DATABASE_URL = "postgresql+psycopg2://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)