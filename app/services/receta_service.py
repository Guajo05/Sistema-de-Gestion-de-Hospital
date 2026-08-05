from app.models.receta import Receta
from app.repositories.repository_receta import RecetaRepository
from app.repositories.repository_consulta import ConsultaRepository
from app.repositories.repository_medicamento import MedicamentoRepository
from app.utils.validar_datos import Validar_Datos_Existente

class RecetaService:
    def __init__(self):
        self.r_repository = RecetaRepository()
        self.c_repository = ConsultaRepository()
        self.m_repository = MedicamentoRepository()

    def ejecutar_registrar_receta(self, datos: dict) -> tuple[Receta]:
        if 'consulta' not in datos:
            return None, 'EL ID DE LA CONSULTA DEBE SER REQUERIDO.❎'

        try:
            consulta = int(datos['consulta'])

        except(TypeError, ValueError):
            return None, 'ID INVALIDO.❎'

        if 'medicamento' not in datos:
            return None, 'EL EL DEL MEDICAMENTO DEBE SER REQUERIDO.❎'

        try:
            medicamento = int(datos['medicamento'])
        
        except(TypeError, ValueError):
            return None, 'ID INVALIDO.❎'

        try:
            cantidad = int(datos.get('cantidad'))

        except(TypeError, ValueError):
            return None, 'LA CANTIDAD DEBE SER UN NUMERO.❎'

        
        if not Validar_Datos_Existente(consulta, self.c_repository.mostrar_consultas(), posicion_id=0):
            return None, 'ESA CONSULTA NO ESTA REGISTRADA.❎'
        
        if not Validar_Datos_Existente(medicamento, self.m_repository.mostrar_medicamentos(), posicion_id=0):
            return None, 'ESE MEDICAMENTO NO ESTA REGISTRADO.❎'
        
        self.r_repository.registrar_receta(receta)
        return True, 'RECETA EMITIDA CORRECTAMENTE.✅'