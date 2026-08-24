from app.services.estadisticas_service import EstadisticasService
from app.charts.chart_builder import ChartBuilder
from app.reports.informe_pdf_generator import InformePDFGenerator

class EstadisticasController:
    def __init__(self):
        self.service = EstadisticasService()
        self.chart_builder = ChartBuilder()

    def grafica_pastel_ciudad(self):
        datos, error = self.service.ejecutar_estadisticas_ciudad()
        if error:
            return None, error
        return self.chart_builder.grafica_pastel(datos, 'Pacientes por Ciudad'), None

    def grafica_barras_tipo_sangre(self):
        datos, error = self.service.ejecutar_estadisticas_tipo_sangre()
        if error:
            return None, error
        return self.chart_builder.grafica_barras(datos, 'Pacientes por Tipo de Sangre'), None

    def grafica_pastel_con_sin_consultas(self):
        datos, error = self.service.ejecutar_estadisticas_con_sin_consultas()
        if error:
            return None, error
        return self.chart_builder.grafica_pastel(datos, 'Pacientes con vs sin Consultas'), None

    def grafica_barras_top_medicamentos(self):
        datos, error = self.service.ejecutar_top_5_medicamentos()
        if error:
            return None, error
        return self.chart_builder.grafica_barras(
            datos, 'Top 5 Medicamentos Más Recetados', color='#C44E52'
        ), None

    def grafica_pastel_activos_inactivos(self):
        datos, error = self.service.ejecutar_estadisticas_activos_inactivos()
        if error:
            return None, error
        return self.chart_builder.grafica_pastel(
            datos, 'Pacientes Activos vs Inactivos'
        ), None

    def grafica_barras_consultas_por_mes(self):
        datos, error = self.service.ejecutar_estadisticas_consultas_por_mes()
        if error:
            return None, error
        return self.chart_builder.grafica_barras(
            datos, 'Consultas por Mes', color='#55A868'
        ), None

    def obtener_consulta_mas_cara(self):
        return self.service.ejecutar_consulta_mas_cara()

    def obtener_kpis(self):
        return self.service.obtener_kpis()

    def obtener_proximas_citas(self, limite: int = 5):
        return self.service.obtener_proximas_citas(limite)

    def obtener_pacientes_activos_recientes(self, dias: int = 30):
        return self.service.contar_pacientes_activos_recientes(dias)

    def generar_informe_pdf(self, ruta_destino: str) -> tuple[bool, str]:
        figuras = []
        metodos_graficas = [
            self.grafica_barras_consultas_por_mes,
            self.grafica_pastel_activos_inactivos,
            self.grafica_pastel_ciudad,
            self.grafica_barras_tipo_sangre,
            self.grafica_pastel_con_sin_consultas,
            self.grafica_barras_top_medicamentos,
        ]

        for metodo in metodos_graficas:
            figura, error = metodo()
            if figura is not None and error is None:
                figuras.append(figura)

        if not figuras:
            return False, "No hay gráficas disponibles para generar el informe."

        try:
            return InformePDFGenerator.generar(
                figuras, ruta_destino, titulo="Informe Estadístico - Modern Care Clinic"
            )
        except Exception as e:
            return False, f"Error al generar el informe PDF: {e}"