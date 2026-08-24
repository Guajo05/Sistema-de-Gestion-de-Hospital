from app.database.conexion import SeccionLocal
from app.models.medicamento import Medicamento
from app.models.receta import Receta
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError


class RecetaRepository:
    def registrar_receta(self, datos: Receta) -> bool:
        with SeccionLocal() as Seccion:
            medicamento = Seccion.get(Medicamento, datos.medicamento_id)

            if not medicamento:
                return False

            if medicamento.stock < datos.cantidad:
                return False

            try:
                Seccion.add(datos)
                medicamento.stock = medicamento.stock - datos.cantidad
                Seccion.commit()
                return True
            except SQLAlchemyError:
                Seccion.rollback()
                return False

    def mostrar_recetas(self) -> list[Receta]:
        with SeccionLocal() as Seccion:
            stmt = (
                select(Receta)
                .options(
                    joinedload(Receta.medicamento),
                    joinedload(Receta.consulta),
                )
            )
            return Seccion.execute(stmt).scalars().all()