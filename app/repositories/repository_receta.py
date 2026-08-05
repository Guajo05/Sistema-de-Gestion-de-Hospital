from app.database.conexion import SeccionLocal
from app.models.medicamento import Medicamento

class RecetaRepository:
    def registrar_receta(self, datos):
        with SeccionLocal() as Seccion:
            medicamento = Seccion.get(Medicamento, datos.medicamento_id)

            if not medicamento:
                return False

            Seccion.add(datos)

            medicamento.stock = (medicamento.stock - datos.cantidad)
            Seccion.commit()
            return True