from app.database.conexion import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float
class Medicamento(Base):
    __tablename__ = "Medicamentos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)
    laboratorio: Mapped[str] = mapped_column(String(50), nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=1)

    recetas: Mapped[list["Receta"]] = relationship(back_populates="medicamento")