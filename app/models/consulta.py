from app.database.conexion import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Float, ForeignKey
from datetime import datetime

class Consulta(Base):
    __tablename__ = 'Consultas'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    diagnostico: Mapped[str] = mapped_column(String(30), nullable=False)
    costo: Mapped[float] = mapped_column(Float, nullable=False)

    paciente_id: Mapped[int] = mapped_column(ForeignKey("Pacientes.id"))
    medico_id: Mapped[int] = mapped_column(ForeignKey("Medicos.id"))

    paciente: Mapped["Paciente"] = relationship(back_populates="consultas")
    medico: Mapped["Medico"] = relationship(back_populates="consultas")
    recetas: Mapped[list["Receta"]] = relationship(back_populates="consulta")