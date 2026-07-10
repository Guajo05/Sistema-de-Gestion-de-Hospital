from app.models.medico import Medico
from app.repositories.medico_repository import MedicoRepository
from app.repositories.consulta_repository import ConsultaRepository

class MedicoService:
    def __init__(self):
        self.medico_repository = MedicoRepository()
        self.consulta_repository = ConsultaRepository()

    def ejecutar_registrar_medico(self, datos):
        turnos = ['Mañana', 'Tarde', 'Noche']

        if datos['nombre'] == '':
            return None, 'EL NOMBRE DEBE SER OBLIGATORIO.❎'
        
        if datos['especialidad'] == '':
            return None, 'LA ESPECIALIDAD DEBE SER OBLIGATORIA.❎'
    
        if datos['salario'] < 0:
            return None, 'EL SALARIO DEBE SER POSITIVO.❎'
        
        if datos['turno'] not in turnos:
            return None, 'ESE TURNO NO ESTA DISPONIBLE.❎'
        
        medico = Medico(
            datos['nombre'],
            datos['especialidad'],
            datos['salario'],
            datos['turno']
        )

        self.medico_repository.registrar_medico(medico)
        return medico, 'EL MEDICO SE REGISTRO CORRECTAMENTE.✅'
    
    def ejecutar_mostrar_medicos(self):
        medicos = self.medico_repository.mostrar_medicos()

        if len(medicos) == 0:
            return None, 'NO HAY MEDICOS REGISTRADOS.❎'
        
        return medicos, None

    
    def ejecutar_medicos_ocupados(self):
        medicos = self.medico_repository.medicos_ocupados()

        if len(medicos) == 0:
            return None, 'NO HAY MEDICOS OCUPADOS.❎'
        
        return medicos, None
    
    def ejecutar_consultas_medicos(self):
        consultas = self.consulta_repository.mostrar_consultas()
        if len(consultas) > 0:
            medicos_consultas = self.medico_repository.consultas_medicos()
            
            if len(medicos_consultas) == 0:
                return None, 'NO HAY MEDICOS REGISTRADOS.❎'
        else:
            return None, 'NO HAY CONSULTAS REGISTRADAS.❎'
        
        return medicos_consultas, None