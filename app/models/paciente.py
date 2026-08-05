from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.conexion import Base
class Paciente(Base):
    __tablename__ = 'Pacientes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    sangre: Mapped[str] = mapped_column(String(10), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(30), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, default=True)

    consultas: Mapped[list["Consulta"]] = relationship(back_populates="paciente")