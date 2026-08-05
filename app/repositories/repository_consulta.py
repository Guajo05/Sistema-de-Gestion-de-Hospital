from app.models.consulta import Consulta
from app.models.medico import Medico
from app.models.paciente import Paciente
from app.models.receta import Receta
from app.models.medicamento import Medicamento
from app.database.conexion import SeccionLocal
from sqlalchemy import select, func
from app.dto.mostrar_consulta_dto import MostrarConsultaDto

class ConsultaRepository:
    def registrar_consulta(self, consulta):
        with SeccionLocal() as Seccion:
            Seccion.add(consulta)
            Seccion.commit()
            return True

    def mostrar_consultas(self):
        with SeccionLocal() as Seccion:
            stmt = select(Consulta)
            resultado = Seccion.execute(stmt).scalars().all()

            consultas = []

            for c in resultado:
                consulta = MostrarConsultaDto(
                    id = c.id,
                    costo = c.costo,
                    fecha = c.fecha
                )
                consultas.append(consulta)
            return consultas

    def consulta_mas_cara(self):
        with SeccionLocal() as Seccion:
            subq = select(func.max(Consulta.costo)).scalar_subquery()
            consulta = (Seccion.query(Consulta)
                        .join(Medico, Consulta.medico_id == Medico.id)
                        .join(Paciente, Consulta.paciente_id == Paciente.id)
                        .filter(Consulta.costo == subq).first())
            return consulta

    def mostral_historial(self, id):
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

    def estadisticas(self):
        with SeccionLocal() as Seccion:
            estadistica = (Seccion.query(
                                        func.min(Consulta.costo).label("barata"),
                                        func.max(Consulta.costo).label("cara"),
                                        func.sum(Consulta.costo).label("total"),
                                        func.avg(Consulta.costo).label("promedio"))
                                        .one())
            return estadistica