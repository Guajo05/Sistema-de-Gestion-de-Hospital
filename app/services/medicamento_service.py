from app.models.medicamento import Medicamento
from app.repositories.repository_medicamento import MedicamentoRepository
class MedicamentoService:
    def __init__(self):
        self.repository = MedicamentoRepository()

    def ejecutar_registrar_medicamento(self, datos: dict) -> tuple[Medicamento]:

        nombre = datos.get('nombre')

        if not isinstance(nombre, str):
            return None, 'EL NOMBRE DEBE SER OBLIGATORIO.❎'

        laboratorio = datos.get('laboratorio')

        if not isinstance(laboratorio, str):
            return None, 'EL NOMBRE DEL LABORATORIO DEBE SER OBLIGATORIO.❎'

        try:
            precio = float(datos.get("precio"))

        except(TypeError, ValueError):
            return None, 'EL PRECIO DEBE SER NUMERICO.❎'

        if precio < 0:
            return None, 'EL PRECIO DEBE SER POSITIVO.❎'

        try:
            stock = int(datos.get('cantidad'))

        except(TypeError, ValueError):
            return None, 'LA CANTIDAD DEBE SER UN NUMERO ENTERO.❎'

        medicamento = Medicamento(
            nombre = nombre.title(),
            laboratorio = laboratorio.title(),
            precio = precio,
            stock = stock
        )

        resultado = self.repository.registrar_medicamento(medicamento)
        if not resultado:
            return None, 'ERRO AL REGISTRAR EL MEDICAMENTO.❎'

        return medicamento, 'EL MEDICAMENTO SE REGISTRO CORRECTAMENTE.✅'
        
    
    def ejecutar_mostrar_medicamento(self):
        medicamentos = self.repository.mostrar_medicamentos()

        if not medicamentos:
            return None, 'NO HAY MEDICAMENTOS REGISTRADOS.❎'
        
        return medicamentos, None