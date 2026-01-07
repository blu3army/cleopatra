from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:2566@localhost:5432/cleopatra"

engine = create_engine(DATABASE_URL, echo=False, future=True)