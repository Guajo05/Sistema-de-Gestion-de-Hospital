from app.database.conexion import engine, Base
from app.models import *

def init_db():
    Base.metadata.create_all(engine)