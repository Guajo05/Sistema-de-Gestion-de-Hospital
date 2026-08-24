from app.models.paciente import Paciente
from app.models.consulta import Consulta
from app.database.conexion import SeccionLocal
from sqlalchemy import select, func
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
            stmt = select(Paciente).where(Paciente.estado == True)
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