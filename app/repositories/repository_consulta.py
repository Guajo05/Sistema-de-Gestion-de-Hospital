from app.models.consulta import Consulta
from app.models.medico import Medico
from app.models.paciente import Paciente
from app.models.receta import Receta
from app.models.medicamento import Medicamento
from app.database.conexion import SeccionLocal
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from app.dto.mostrar_consulta_dto import MostrarConsultaDto
class ConsultaRepository:
    def registrar_consulta(self, consulta) -> bool:
        with SeccionLocal() as Seccion:
            try:
                Seccion.add(consulta)
                Seccion.commit()
                return True
            except SQLAlchemyError:
                Seccion.rollback()
                return False

    def _a_dto(self, c: Consulta) -> MostrarConsultaDto:
        return MostrarConsultaDto(
            id=c.id,
            costo=c.costo,
            fecha=c.fecha,
            diagnostico=c.diagnostico,
            paciente=c.paciente.nombre if c.paciente else None,
            medico=c.medico.nombre if c.medico else None,
        )

    def mostrar_consultas(self):
        with SeccionLocal() as Seccion:
            stmt = select(Consulta).order_by(Consulta.fecha.asc())
            resultado = Seccion.execute(stmt).scalars().all()
            return [self._a_dto(c) for c in resultado]

    def buscar_consulta(self, fecha_inicio, fecha_final):
        with SeccionLocal() as Seccion:
            stmt = (
                select(Consulta)
                .where(Consulta.fecha >= fecha_inicio, Consulta.fecha <= fecha_final)
                .order_by(Consulta.fecha.desc())
            )
            resultado = Seccion.execute(stmt).scalars().all()
            return [self._a_dto(c) for c in resultado]

    def mostrar_historial(self, id):
        with SeccionLocal() as Seccion:
            historial = (Seccion.query(
                                        Consulta.costo,
                                        Consulta.diagnostico,
                                        Medico.nombre.label("medico"),
                                        Medicamento.nombre.label("medicamento"))
                                        .join(Paciente, Consulta.paciente_id == Paciente.id)
                                        .join(Medico, Consulta.medico_id == Medico.id)
                                        .outerjoin(Receta, Receta.consulta_id == Consulta.id)
                                        .outerjoin(Medicamento, Receta.medicamento_id == Medicamento.id)
                                        .filter(Paciente.id == id)
                                        .order_by(Consulta.fecha.desc())
                                        .all())
            return historial