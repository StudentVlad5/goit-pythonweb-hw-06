from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://postgres:mysecretpassword@localhost:5432/postgres'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()