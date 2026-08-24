from app.services.medico_service import MedicoService

class MedicoController:
    def __init__(self):
        self.service = MedicoService()

    def registrar_medico(self, datos):
        return self.service.ejecutar_registrar_medico(datos)
    
    def actualizar_medico(self, datos):
        return self.service.ejecutar_actualizar_medico(datos)
    
    def eliminar_medico(self, id):
        return self.service.ejecutar_eliminar_medico(id)
        
    def mostrar_medicos(self):
        return self.service.ejecutar_mostrar_medicos()
        
    def medicos_ocupados(self):
        return self.service.ejecutar_medicos_ocupados()