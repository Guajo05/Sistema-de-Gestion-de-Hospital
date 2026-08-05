from app.models.medico import Medico
from app.repositories.repository_medico import MedicoRepository
from app.repositories.repository_consulta import ConsultaRepository
from app.utils.validar_datos import Validar_Datos_Existente

class MedicoService:
    def __init__(self):
        self.medico_repository = MedicoRepository()
        self.consulta_repository = ConsultaRepository()
        self._turnos = {'Mañana', 'Tarde', 'Noche'}

    def ejecutar_registrar_medico(self, datos: dict) -> tuple[Medico]:
        nombre = datos.get('nombre')

        if not isinstance(nombre, str):
            return None, 'EL NOMBRE DEBE SER OBLIGATORIO.❎'

        especialidad = datos.get('especialidad')
        
        if not isinstance(especialidad, str):
            return None, 'LA ESPECIALIDAD DEBE SER OBLIGATORIA.❎'

        try:
            salario = float(datos.get('salario'))

        except (TypeError, ValueError):
            return None, 'EL SALARIO DEBE SER UN NUMERO.❎'

        turno = str(datos.get('turno')).capitalize()

        if turno not in self._turnos:
            return None, 'ESTE TURNO NO ESTA DISPONIBLE.❎'

        medico = Medico(
            nombre = nombre,
            especialidad = especialidad,
            salario = salario,
            turno = turno
        )

        resultado = self.medico_repository.registrar_medico(medico)

        if not resultado:
            return None, 'ERROR AL REGISTRAR MEDICO.❎'
        
        return medico, 'MEDICO REGISTRADO CORRECTAMENTE.✅'
        
    def ejecutar_actualizar_medico(self, datos: dict) -> tuple[Medico]:
        if 'id' not in datos:
            return None, 'ID DEL MEDICO REQUERIDO.❎'
        
        try:
            medico_id = int(datos['id'])
        
        except (TypeError, ValueError):
            return None, 'ID INVALIDO.❎'
        
        nombre = datos.get('nombre', '')
        
        if not isinstance(nombre, str):
            return None, 'EL NOMBRE DEBE SER OBLIGATORIO.❎'

        especialidad = datos.get('especialidad')

        if not isinstance(especialidad, str):
            return None, 'LA ESPECIALIDAD DEBE SER OBLIGATORIA.❎'
        
        try:
            salario = float(datos.get('salario'))

        except (TypeError, ValueError):
            return None, 'LA EDAD DEBE SER UN NÚMERO.❎'
        
        turno = str(datos.get('turno')).capitalize()

        if turno not in self._turnos:
            return None, 'ESTE TURNO NO ESTA DISPONIBLE.❎'
        
        medico = Medico(
            id = medico_id,
            nombre = nombre,
            especialidad = especialidad,
            salario = salario,
            turno = turno
        )
        
        resultado = self.medico_repository.actualizar_medico(medico)

        if resultado is None:
            return None, 'NO SE PUDO ACTUALIZAR LOS DATOS.❎'

        return resultado, 'MEDICO ACTUALIZADO CORRECTAMENTE.✅'
        
    def ejecutar_eliminar_medico(self, id: int) -> bool:
        medicos = self.medico_repository.mostrar_medicos()

        if not Validar_Datos_Existente(id, medicos, posicion_id = 0):
            return False, 'ID INVALIDO.❎'
        
        eliminado = self.medico_repository.eliminar_medico(id)
        if not eliminado:
            return False, 'NO SE PUDO ELIMINAR EL MEDICO.❎'

        return True, 'MEDICO ELIMINADO CORRECTAMENTE.✅'

    def ejecutar_mostrar_medicos(self):
        medicos = self.medico_repository.mostrar_medicos()

        if not medicos:
            return None, 'NO HAY MEDICOS REGISTRADOS.❎'
        
        return medicos, None

    
    def ejecutar_medicos_ocupados(self):
        medicos = self.medico_repository.medicos_ocupados()

        if not medicos:
            return None, 'NO HAY MEDICOS OCUPADOS.❎'
        
        return medicos, None
    
    def ejecutar_consultas_medicos(self):
        consultas = self.consulta_repository.mostrar_consultas()

        if not consultas:
            medicos_consultas = self.medico_repository.consultas_medicos()
            
            if not medicos_consultas:
                return None, 'NO HAY MEDICOS REGISTRADOS.❎'
        else:
            return None, 'NO HAY CONSULTAS REGISTRADAS.❎'
        
        return medicos_consultas, None