from app.models.paciente import Paciente
from app.repositories.paciente_repository import PacienteRepository
from app.utils.validar_datos import Validar_Datos_Existente

class PacienteService:
    def __init__(self):
        self.repository = PacienteRepository()

    def ejecutar_registrar_paciente(self, datos):
        tipos_de_Sangre = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

        if datos['nombre'] == '':
            return None, 'EL NOMBRE DEBER SER OBLIGATORIO.❎'
        
        if datos['edad'] < 0:
            return None, 'LA EDAD DEBE SER POSITIVA.❎'
        
        if datos['sangre'] not in tipos_de_Sangre:
            return None, 'ESTE TIPO DE SANGRE NO EXISTE.❎'
        
        paciente = Paciente(
            nombre = datos['nombre'], 
            edad = datos['edad'],
            sangre = datos['sangre'],
            ciudad = datos['ciudad'],
            estado = None
        )
        self.repository.registrar_paciente(paciente)
        return paciente, 'PACIENTE REGISTRADO CORRECTAMENTE.✅'
    
    def ejecutar_actualizar_paciente(self, datos):
        tipos_de_Sangre = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

        if datos['nombre'] == '':
            return None, 'EL NOMBRE DEBER SER OBLIGATORIO.❎'
        
        if datos['edad'] < 0:
            return None, 'LA EDAD DEBE SER POSITIVA.❎'
        
        if datos['sangre'] not in tipos_de_Sangre:
            return None, 'ESTE TIPO DE SANGRE NO EXISTE.❎'
        
        paciente = Paciente(
            id = datos['id'],
            nombre = datos['nombre'], 
            edad = datos['edad'],
            sangre = datos['sangre'],
            ciudad = datos['ciudad'],
            estado = None
        )

        resultado = self.repository.actualizar_paciente(paciente)

        if resultado is None:
            return None, 'NO SE PUDO ACTUALIZAR LOS DATOS.❎'
        
        return resultado, None
    
    def ejecutar_eliminar_paciente(self, id):
        pacientes = self.repository.mostrar_pacientes()

        if not Validar_Datos_Existente(id, pacientes, posicion_id = 0):
            return False, 'ID INVALIDO.❎'
        
        self.repository.eliminar_paciente(id)
        return True, 'PACIENTE ELIMINADO CORRECTAMENTE.✅'
    
    def ejecutar_mostrar_pacientes(self):
        pacientes = self.repository.mostrar_pacientes()
        if len(pacientes) == 0:
            return None, 'NO HAY PACIENTES REGISTRADOS.❎'
        return pacientes, None
    
    def ejecutar_mostrar_historial(self, paciente_id):
        pacientes = self.repository.mostrar_pacientes()
        
        if not Validar_Datos_Existente(paciente_id, pacientes, posicion_id=0):
            return None, 'ESE PACIENTE NO ESTA REGISTRADO.❎'
       
        historial = self.repository.mostrar_historial(paciente_id)
        
        if not historial: 
            return None, 'ESTE PACIENTE NO TIENE HISTORIAL DE CONSULTAS.❎'
        
        return historial, None

    def ejecutar_paciente_sin_consultas(self):
        pacientes = self.repository.pacientes_sin_consultas()
        if len(pacientes) == 0:
            return None, 'TODOS LOS PACIENTES TIENEN CONSULTAS.❎'
        return pacientes, None