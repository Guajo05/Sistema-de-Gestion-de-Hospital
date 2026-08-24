from app.repositories.repository_estadisticas import EstadisticasRepository

class EstadisticasService:
    def __init__(self):
        self.repository = EstadisticasRepository()

    def ejecutar_estadisticas_ciudad(self) -> tuple:
        datos = self.repository.contar_pacientes_por_ciudad()
        if not datos:
            return None, 'NO HAY DATOS DE PACIENTES POR CIUDAD.❎'
        etiquetas = [ciudad for ciudad, _ in datos]
        valores = [total for _, total in datos]
        return {'etiquetas': etiquetas, 'valores': valores}, None

    def ejecutar_estadisticas_tipo_sangre(self) -> tuple:
        datos = self.repository.contar_pacientes_por_tipo_sangre()
        if not datos:
            return None, 'NO HAY DATOS DE TIPOS DE SANGRE.❎'
        etiquetas = [sangre for sangre, _ in datos]
        valores = [total for _, total in datos]
        return {'etiquetas': etiquetas, 'valores': valores}, None

    def ejecutar_estadisticas_activos_inactivos(self) -> tuple:
        datos = self.repository.contar_pacientes_activos_vs_inactivos()
        if datos['activos'] == 0 and datos['inactivos'] == 0:
            return None, 'NO HAY PACIENTES REGISTRADOS.❎'
        return {
            'etiquetas': ['Activos', 'Inactivos'],
            'valores': [datos['activos'], datos['inactivos']]
        }, None

    def ejecutar_estadisticas_consultas_por_mes(self) -> tuple:
        datos = self.repository.contar_consultas_por_mes()
        if not datos:
            return None, 'NO HAY CONSULTAS REGISTRADAS.❎'
        etiquetas = [mes for mes, _ in datos]
        valores = [total for _, total in datos]
        return {'etiquetas': etiquetas, 'valores': valores}, None

    def ejecutar_estadisticas_con_sin_consultas(self) -> tuple:
        datos = self.repository.contar_pacientes_con_y_sin_consultas()
        if datos['con_consultas'] == 0 and datos['sin_consultas'] == 0:
            return None, 'NO HAY PACIENTES REGISTRADOS.❎'
        return {
            'etiquetas': ['Con consultas', 'Sin consultas'],
            'valores': [datos['con_consultas'], datos['sin_consultas']]
        }, None

    def ejecutar_top_5_medicamentos(self) -> tuple:
        datos = self.repository.top_5_medicamentos_recetados()
        if not datos:
            return None, 'NO HAY RECETAS REGISTRADAS.❎'
        etiquetas = [nombre for nombre, _ in datos]
        valores = [total for _, total in datos]
        return {'etiquetas': etiquetas, 'valores': valores}, None

    def ejecutar_consulta_mas_cara(self) -> tuple:
        consulta = self.repository.consulta_mas_cara()
        if consulta is None:
            return None, 'NO HAY CONSULTAS REGISTRADAS.❎'
        try:
            resultado = {
                'id': consulta.id,
                'paciente': consulta.paciente.nombre if consulta.paciente else 'N/A',
                'medico': consulta.medico.nombre if consulta.medico else 'N/A',
                'diagnostico': consulta.diagnostico,
                'costo': consulta.costo,
                'fecha': consulta.fecha
            }
        except AttributeError:
            return None, 'ERROR AL PROCESAR LA CONSULTA MÁS CARA.❎'
        return resultado, None

    def contar_pacientes_activos_recientes(self, dias: int = 30) -> int:
        """Retorna la cantidad de pacientes con consultas en los últimos 'dias' días."""
        return self.repository.contar_pacientes_con_consultas_recientes(dias)

    def obtener_kpis(self) -> dict:
        return {
            'citas_hoy': self.repository.contar_citas_hoy(),
            'pacientes_activos_mes': self.contar_pacientes_activos_recientes(30),
            'medicos_activos': self.repository.contar_medicos_activos(),
            'ingresos_dia': self.repository.ingresos_dia()
        }

    def obtener_proximas_citas(self, limite: int = 5) -> list:
        """Retorna una lista de las próximas citas (hoy o las siguientes)."""
        return self.repository.obtener_proximas_citas(limite)