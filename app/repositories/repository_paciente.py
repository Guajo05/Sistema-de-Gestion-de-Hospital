from app.models.paciente import Paciente
from app.models.consulta import Consulta
from app.database.conexion import SeccionLocal
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

class PacienteRepository:
    def registrar_paciente(self, paciente: Paciente) -> bool:
        with SeccionLocal() as Seccion:
            try:
                Seccion.add(paciente)
                Seccion.commit()
                return True
            except SQLAlchemyError:
                Seccion.rollback()
                return False

    def mostrar_pacientes(self) -> list[Paciente]:
        with SeccionLocal() as Seccion:
            stmt = select(Paciente)
            pacientes = Seccion.execute(stmt).scalars().all()
            return pacientes

    def actualizar_paciente(self, datos):
        with SeccionLocal() as Seccion:
            paciente = Seccion.get(Paciente, datos.id)

            if paciente is None:
                return None

            paciente.nombre = datos.nombre
            paciente.edad = datos.edad
            paciente.ciudad = datos.ciudad
            paciente.sangre = datos.sangre
            paciente.estado = datos.estado

            try:
                Seccion.commit()
                return paciente
            
            except SQLAlchemyError:
                Seccion.rollback()
                return None

    def eliminar_paciente(self, id: int) -> bool:
        with SeccionLocal() as Seccion:
            paciente = Seccion.get(Paciente, id)

            if paciente is None:
                return False

            paciente.estado = False

            try:
                Seccion.commit()
                return True
            
            except SQLAlchemyError:
                Seccion.rollback()
                return False
            
    def mostrar_historial(self, id: int):
        with SeccionLocal() as Seccion:
            paciente = Seccion.get(Paciente, id)

            if paciente is None:
                return None
            
            consultas = (
                Seccion.query(Consulta)
                .filter(Consulta.paciente_id == id)
                .order_by(Consulta.fecha.desc())
                .all())
            
            return consultas

    def pacientes_sin_consultas(self):
        with SeccionLocal() as Seccion:
            subq = select(Consulta.paciente_id).distinct().scalar_subquery()
            
            pacientes = (Seccion.query(Paciente)
                         .filter(Paciente.id.not_in(subq))
                         .all())
            return pacientes