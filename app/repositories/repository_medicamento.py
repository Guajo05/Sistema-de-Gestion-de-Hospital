from app.database.conexion import SeccionLocal
from app.models.medicamento import Medicamento
from app.models.receta import Receta
from sqlalchemy import select, func

class MedicamentoRepository:
    def registrar_medicamento(self, datos):
        with SeccionLocal() as Seccion:
            Seccion.add(datos)
            Seccion.commit()

    def mostrar_medicamento(self):
        with SeccionLocal() as Seccion:
           stmt = select(Medicamento)
           medicamentos = Seccion.execute(stmt).scalars().all()
           return medicamentos

    def top_medicamentos(self):
        with SeccionLocal() as Seccion:
            medicamentos = (Seccion.query(
                                            Medicamento.nombre, 
                                            Medicamento.laboratorio,
                                            func.count(Receta.id).label("total")
                                          )
                            .join(Receta, Receta.medicamento_id == Medicamento.id)
                            .group_by(Medicamento.id)
                            .order_by(func.count(Receta.medicamento_id).desc()).limit(5)
                            .all()
                            )
            return medicamentos