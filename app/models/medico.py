from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Float
from app.database.conexion import Base
class Medico(Base):
    __tablename__ = 'Medicos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    especialidad: Mapped[str] = mapped_column(String(30), nullable=False)
    salario: Mapped[float] = mapped_column(Float, nullable=False)
    turno: Mapped[str] = mapped_column(String(10), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, default=True)

    consultas: Mapped[list["Consulta"]] = relationship(back_populates="medico")