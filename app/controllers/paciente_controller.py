from app.services.paciente_service import PacienteService
class PacienteController:
    def __init__(self):
        self.service = PacienteService()

    def registrar_paciente(self, datos):
        return self.service.ejecutar_registrar_paciente(datos)
    
    def actualizar_paciente(self, datos):
        return self.service.ejecutar_actualizar_paciente(datos)
    
    def eliminar_paciente(self, id):
        return self.service.ejecutar_eliminar_paciente(id)
        
    def mostrar_pacientes(self):
        return self.service.ejecutar_mostrar_pacientes()
    
    def mostrar_historial(self, paciente_id):
        return self.service.ejecutar_mostrar_historial(paciente_id)