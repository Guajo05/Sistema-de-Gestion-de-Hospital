from app.models.receta import Receta
from app.repositories.receta_repository import RecetaRepository
from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.medicamento_repository import MedicamentoRepository
from app.utils.validar_datos import Validar_Datos_Existente

class RecetaService:
    def __init__(self):
        self.r_repository = RecetaRepository()
        self.c_repository = ConsultaRepository()
        self.m_repository = MedicamentoRepository()

    def ejecutar_registrar_receta(self, datos):
        if not Validar_Datos_Existente(datos['consulta'], self.c_repository.mostrar_consultas(), posicion_id=0):
            return None, 'ESA CONSULTA NO ESTA REGISTRADA.❎'
        
        if not Validar_Datos_Existente(datos['medicamento'], self.m_repository.mostrar_medicamentos(), posicion_id=0):
            return None, 'ESE MEDICAMENTO NO ESTA REGISTRADO.❎'
        
        receta = Receta(
            dosis = datos['dosis'],
            dias = datos['dias'],
            consulta = datos['consulta'],
            medicamento = datos['medicamento'],
            cantidad = None
        )

        self.r_repository.registrar_receta(receta)
        return True, 'RECETA EMITIDA CORRECTAMENTE.✅'