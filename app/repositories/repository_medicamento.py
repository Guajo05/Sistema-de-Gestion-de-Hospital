from app.database.conexion import SeccionLocal
from app.models.medicamento import Medicamento
from sqlalchemy import select
class MedicamentoRepository:
    def registrar_medicamento(self, datos):
        with SeccionLocal() as Seccion:
            Seccion.add(datos)
            Seccion.commit()
            return True

    def mostrar_medicamentos(self):
        with SeccionLocal() as Seccion:
           stmt = select(Medicamento)
           medicamentos = Seccion.execute(stmt).scalars().all()
           return medicamentos
