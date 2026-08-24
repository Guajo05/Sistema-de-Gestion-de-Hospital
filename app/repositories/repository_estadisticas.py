from app.models.paciente import Paciente
from app.models.consulta import Consulta
from app.models.receta import Receta
from app.models.medicamento import Medicamento
from app.models.medico import Medico
from app.database.conexion import SeccionLocal
from sqlalchemy import select, func, desc
from datetime import datetime, timedelta, date

class EstadisticasRepository:
    def contar_pacientes_por_ciudad(self) -> list[tuple[str, int]]:
        with SeccionLocal() as Seccion:
            stmt = (
                select(Paciente.ciudad, func.count(Paciente.id))
                .where(Paciente.estado == True)
                .group_by(Paciente.ciudad)
            )
            return Seccion.execute(stmt).all()

    def contar_pacientes_por_tipo_sangre(self) -> list[tuple[str, int]]:
        with SeccionLocal() as Seccion:
            stmt = (
                select(Paciente.sangre, func.count(Paciente.id))
                .where(Paciente.estado == True)
                .group_by(Paciente.sangre)
            )
            return Seccion.execute(stmt).all()

    def contar_pacientes_activos_vs_inactivos(self) -> dict:
        with SeccionLocal() as Seccion:
            activos = Seccion.query(Paciente).filter(Paciente.estado == True).count()
            inactivos = Seccion.query(Paciente).filter(Paciente.estado == False).count()
            return {'activos': activos, 'inactivos': inactivos}

    def contar_consultas_por_mes(self) -> list[tuple[str, int]]:
        with SeccionLocal() as Seccion:
            stmt = (
                select(func.strftime('%Y-%m', Consulta.fecha), func.count(Consulta.id))
                .group_by(func.strftime('%Y-%m', Consulta.fecha))
                .order_by(func.strftime('%Y-%m', Consulta.fecha))
            )
            return Seccion.execute(stmt).all()

    def contar_pacientes_con_y_sin_consultas(self) -> dict:
        with SeccionLocal() as Seccion:
            subq = select(Consulta.paciente_id).distinct().scalar_subquery()

            con_consultas = (
                Seccion.query(Paciente)
                .filter(Paciente.id.in_(subq))
                .count()
            )
            sin_consultas = (
                Seccion.query(Paciente)
                .filter(Paciente.id.not_in(subq))
                .count()
            )
            return {'con_consultas': con_consultas, 'sin_consultas': sin_consultas}

    def top_5_medicamentos_recetados(self) -> list[tuple[str, int]]:
        with SeccionLocal() as Seccion:
            stmt = (
                select(Medicamento.nombre, func.sum(Receta.cantidad).label('total'))
                .join(Receta, Receta.medicamento_id == Medicamento.id)
                .group_by(Medicamento.nombre)
                .order_by(desc('total'))
                .limit(5))
            return Seccion.execute(stmt).all()

    def consulta_mas_cara(self) -> Consulta | None:
        with SeccionLocal() as Seccion:
            stmt = (
                select(Consulta)
                .order_by(Consulta.costo.desc())
                .limit(1)
            )
            return Seccion.execute(stmt).scalar_one_or_none()

    def contar_pacientes_con_consultas_recientes(self, dias: int = 30) -> int:
        with SeccionLocal() as session:
            fecha_limite = datetime.now() - timedelta(days=dias)
            subq = select(Consulta.paciente_id).where(Consulta.fecha >= fecha_limite).distinct().subquery()
            stmt = select(func.count()).select_from(subq)
            return session.execute(stmt).scalar() or 0

    def contar_medicos_activos(self) -> int:
        with SeccionLocal() as session:
            stmt = select(func.count(Medico.id)).where(Medico.estado == True)
            return session.execute(stmt).scalar() or 0

    def ingresos_dia(self) -> float:
        with SeccionLocal() as session:
            hoy = datetime.now().date()
            stmt = select(func.sum(Consulta.costo)).where(func.date(Consulta.fecha) == hoy)
            return session.execute(stmt).scalar() or 0.0

    def contar_citas_hoy(self) -> int:
            with SeccionLocal() as session:
                hoy = date.today()
                stmt = select(func.count(Consulta.id)).where(func.date(Consulta.fecha) == hoy)
                return session.execute(stmt).scalar() or 0
    
    def obtener_proximas_citas(self, limite: int = 5) -> list:
        with SeccionLocal() as session:
            hoy = date.today()
            stmt = (
                    select(Consulta)
                    .where(func.date(Consulta.fecha) == hoy)
                    .order_by(Consulta.fecha.asc())
                    .limit(limite))
            citas = session.execute(stmt).scalars().all()
            
            if not citas:
                stmt = (
                    select(Consulta)
                    .where(Consulta.fecha >= hoy)
                    .order_by(Consulta.fecha.asc())
                    .limit(limite))
                citas = session.execute(stmt).scalars().all()
            
            resultado = []

            for c in citas:
                estado = getattr(c, 'estado', 'Pendiente')

                if estado.lower() == 'confirmado':
                    bg_color = "#D4EDDA"
                    text_color = "#155724"

                elif estado.lower() == 'pendiente':
                    bg_color = "#FFF3CD"
                    text_color = "#856404"

                else:
                    bg_color = "#E2E3E5"
                    text_color = "#383D41"
                
                resultado.append({
                    'hora': c.fecha.strftime("%I:%M %p") if hasattr(c, 'hora') else c.fecha.strftime("%d/%m/%Y"),
                    'paciente': c.paciente.nombre if c.paciente else "Desconocido",
                    'medico': c.medico.nombre if c.medico else "Desconocido",
                    'estado': estado,
                    'bg_color': bg_color,
                    'text_color': text_color
                    })
                
        return resultado

    def estadisticas_costo(self):
        with SeccionLocal() as Seccion:
            estadistica = (Seccion.query(
                                        func.min(Consulta.costo).label("barata"),
                                        func.max(Consulta.costo).label("cara"),
                                        func.sum(Consulta.costo).label("total"),
                                        func.avg(Consulta.costo).label("promedio"))
                                        .one())
            return estadistica