from app.models.paciente import Paciente
from app.repositories.repository_paciente import PacienteRepository
from app.utils.validar_datos import Validar_Datos_Existente
class PacienteService:
    def __init__(self):
        self.repository = PacienteRepository()
        self._tipos_de_sangre = {'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'}

    def ejecutar_registrar_paciente(self, datos: dict) -> tuple[Paciente]:
        nombre = datos.get('nombre')

        if not isinstance(nombre, str):
            return None, 'EL NOMBRE ES OBLIGATORIO.❎'
        
        try:
            edad = int(datos.get('edad', -1))

        except (TypeError, ValueError):
            return None, 'LA EDAD DEBE SER UN NUMERO ENTERO.❎'

        if edad < 0:
            return None, 'LA EDAD DEBE SER POSITIVA.❎'

        sangre = str(datos.get('sangre', '')).upper()

        if sangre not in self._tipos_de_sangre:
            return None, 'ESTE TIPO DE SANGRE NO EXISTE.❎'

        ciudad = str(datos.get('ciudad', '')).strip()

        if ciudad == '':
            return None, 'LA CIUDAD DEBE SER OBLIGATORIA.❎'

        paciente = Paciente(
            nombre = nombre,
            edad = edad,
            sangre = sangre,
            ciudad = ciudad
        )

        registrado = self.repository.registrar_paciente(paciente)

        if not registrado:
            return None, 'ERROR AL REGISTRAR PACIENTE.❎'

        return paciente, 'PACIENTE REGISTRADO CORRECTAMENTE.✅'
    
    def ejecutar_actualizar_paciente(self, datos: dict) -> tuple[Paciente]:
        if 'id' not in datos:
            return None, 'ID DEL PACIENTE REQUERIDO.❎'

        try:
            paciente_id = int(datos['id'])

        except (TypeError, ValueError):
            return None, 'ID INVALIDO.❎'

        nombre = datos.get('nombre', '')

        if not isinstance(nombre, str):
            return None, 'EL NOMBRE DEBE SER OBLIGATORIO.❎'

        try:
            edad = int(datos.get('edad', -1))
        except (TypeError, ValueError):
            return None, 'LA EDAD DEBE SER UN NÚMERO ENTERO.❎'

        if edad < 0:
            return None, 'LA EDAD DEBE SER POSITIVA.❎'

        sangre = str(datos.get('sangre', '')).upper()
        if sangre not in self._tipos_de_sangre:
            return None, 'ESTE TIPO DE SANGRE NO EXISTE.❎'

        ciudad = datos.get('ciudad', '').strip()
        if ciudad == '':
            return None, 'LA CIUDAD ES OBLIGATORIA.❎'

        paciente = Paciente(
            id = paciente_id,
            nombre = nombre,
            edad = edad,
            sangre = sangre,
            ciudad = ciudad
        )

        resultado = self.repository.actualizar_paciente(paciente)
        if resultado is None:
            return None, 'NO SE PUDO ACTUALIZAR LOS DATOS.❎'
        return resultado, 'PACIENTE ACTUALIZADO CORRECTAMENTE.✅'
    
    def ejecutar_eliminar_paciente(self, id) -> bool:
        pacientes = self.repository.mostrar_pacientes()

        if not Validar_Datos_Existente(id, pacientes, posicion_id = 0):
            return False, 'ID INVALIDO.❎'
        
        eliminado = self.repository.eliminar_paciente(id)

        if not eliminado:
            return False, 'NO SE PUDO ELIMINAR EL PACIENTE.❎'
        return True, 'PACIENTE ELIMINADO CORRECTAMENTE.✅'
    
    def ejecutar_mostrar_pacientes(self):
        pacientes = self.repository.mostrar_pacientes()

        if not pacientes:
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

    def ejecutar_pacientes_sin_consultas(self):
        pacientes = self.repository.pacientes_sin_consultas()
        if not pacientes:
            return None, 'TODOS LOS PACIENTES TIENEN CONSULTAS.❎'
        return pacientes, None