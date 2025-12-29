from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root@localhost:3306/cleopatra"

engine = create_engine(DATABASE_URL, echo=False, future=True)