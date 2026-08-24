from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config.setting import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)

class Base(DeclarativeBase):
    pass

SeccionLocal = sessionmaker(bind=engine)