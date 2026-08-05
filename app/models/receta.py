from app.database.conexion import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

class Receta(Base):
    __tablename__ = 'Recetas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dosis: Mapped[str] = mapped_column(String(50), nullable=False)
    dias: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, default=1)

    medicamento_id: Mapped[int] = mapped_column(ForeignKey("Medicamentos.id"))
    consulta_id: Mapped[int] = mapped_column(ForeignKey("Consultas.id"))

    medicamento: Mapped["Medicamento"] = relationship(back_populates='recetas')
    consulta: Mapped["Consulta"] = relationship(back_populates='recetas')