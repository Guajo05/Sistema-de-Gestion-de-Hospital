from app.models.medicamento import Medicamento
from app.repositories.medicamento_repository import MedicamentoRepository

class MedicamentoService:
    def __init__(self):
        self.repository = MedicamentoRepository()

    def ejecutar_registrar_medicamento(self, datos):
        if datos['precio'] < 0:
            return None, 'EL PRECIO INGRESADO ES INVALIDO.❎'
        
        if datos['stock'] < 0:
            return None, 'EL STOCK INGRESADO ES INVALIDO.❎'
        
        medicamento = Medicamento(
            datos['nombre'],
            datos['laboratorio'],
            datos['precio'],
            datos['stock']
        )
        self.repository.registrar_medicamento(medicamento)
        return True, 'EL MEDICAMENTO SE REGISTRO CORRECTAMENTE.✅'
    
    def ejecutar_mostrar_medicamento(self):
        medicamentos = self.repository.mostrar_medicamentos()

        if len(medicamentos) == 0:
            return None, 'NO HAY MEDICAMENTOS REGISTRADOS.❎'
        
        return medicamentos, None
    
    def ejecutar_top_medicamentos(self):
        medicamentos = self.repository.mostrar_medicamentos()
        
        if len(medicamentos) > 0:
            top_medicamentos = self.repository.top_medicamentos()
            if len(top_medicamentos) == 0:
                return None, 'NO ES POSIBLE HACER EL TOP.❎'
            
            return medicamentos, None
        
        else:
            return None, 'NO HAY MEDICAMENTOS REGISTRADOS.❎'