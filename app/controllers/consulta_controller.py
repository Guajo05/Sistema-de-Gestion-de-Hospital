from app.services.consulta_service import ConsultaService
class ConsultaController:
    def __init__(self):
        self.service = ConsultaService()

    def registrar_consulta(self, datos):
        return self.service.ejecutar_registrar_consulta(datos)
    
    def mostrar_consultas(self):
        return self.service.ejecutar_mostrar_consultas()
    
    def buscar_consultas(self, fechas):
        return self.service.ejecutar_buscar_consulta(fechas)