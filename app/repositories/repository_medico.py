from app.database.conexion import SeccionLocal
from app.models.medico import Medico
from app.models.consulta import Consulta
from sqlalchemy import (select, func)
from sqlalchemy.exc import SQLAlchemyError
class MedicoRepository:
    def registrar_medico(self, medico) -> bool:
        with SeccionLocal() as Seccion:
            try:
                Seccion.add(medico)
                Seccion.commit()
                return True
            except SQLAlchemyError:
                Seccion.rollback()
                return False

    def mostrar_medicos(self):
        with SeccionLocal() as Seccion:
            stmt = select(Medico).where(Medico.estado == True)
            medicos = Seccion.execute(stmt).scalars().all()
            return medicos
        
    def actualizar_medico(self, datos):
        with SeccionLocal() as Seccion:
            medico = Seccion.get(Medico, datos.id)

            if medico is None:
                return None

            medico.nombre = datos.nombre
            medico.especialidad = datos.especialidad
            medico.salario = datos.salario
            medico.turno = datos.turno

            try:
                Seccion.commit()
                return medico
            
            except SQLAlchemyError:
                Seccion.rollback()
                return None

    def eliminar_medico(self, id) -> bool:
        with SeccionLocal() as Seccion:
            medico = Seccion.get(Medico, id)

            if medico is None:
                return False

            medico.estado = False

            try:
                Seccion.commit()
                return True
            except SQLAlchemyError:
                Seccion.rollback()
                return False

    def medicos_ocupados(self):
        with SeccionLocal() as Seccion:
            medicos = (Seccion.query(
                                    Medico.nombre, 
                                    Medico.especialidad,
                                    func.count(Consulta.id).label("total"))
                                    .join(Consulta, Consulta.medico_id == Medico.id)
                                    .filter(Medico.estado == True)
                                    .group_by(Medico.id)
                                    .having(func.count(Consulta.id) > 2)
                                    .order_by(func.count(Consulta.id).desc())
                                    .all()
                                    )
            return medicos
    
    def consultas_medicos(self):
        with SeccionLocal() as Seccion:
            consultas = (Seccion.query(
                                        Medico.nombre, 
                                        Medico.especialidad, 
                                        func.count(Consulta.id).label("total"))
                                        .outerjoin(Consulta, Consulta.medico_id == Medico.id)
                                        .filter(Medico.estado == True)
                                        .group_by(Medico.id)
                                        .order_by(func.count(Consulta.id).desc())
                                        .all()
                                        )
            return consultas