from app.models.consulta import Consulta
from app.repositories.consulta_repository import ConsultaRepository
from app.repositories.medico_repository import MedicoRepository
from app.repositories.paciente_repository import PacienteRepository
from app.utils.validar_datos import Validar_Datos_Existente
from datetime import datetime

class ConsultaService:
    def __init__(self):
        self.consulta_repository = ConsultaRepository()
        self.paciente_repository = PacienteRepository()
        self.medico_repository = MedicoRepository()

    def ejecutar_registrar_consulta(self, datos):
        
        if not Validar_Datos_Existente(datos['paciente'], self.paciente_repository.mostrar_pacientes(), posicion_id=0):
            return None, "ESE PACIENTE NO ESTA REGISTRADO.❎"
        
        if not Validar_Datos_Existente(datos['medico'], self.medico_repository.mostrar_medicos(), posicion_id=0):
            return None, "ESE MEDICO NO ESTA REGISTRADO.❎"
        
        if datos['costo'] < 0:
            return None, 'EL COSTO DEBE POSITIVO.❎'
        
        try:
            fecha_formateada = datetime.strptime(datos['fecha'], "%Y-%m-%d")
            if fecha_formateada.date() < datetime.now().date():
                return None, "NO PUEDES REGISTRAR CONSULTAS PARA EL PASADO.❎"
            else:
                datos['fecha_consulta'] = fecha_formateada
                consulta = Consulta(
                    fecha = datos['fecha'],
                    diagnostico = datos['diagnostico'],
                    costo = datos['costo'],
                    paciente = datos['paciente'],
                    medico = datos['medico'],
                )
                self.consulta_repository.registrar_consulta(consulta)
                return None, 'LA CONSULTA SE REGISTRO CORRECTAMENTE.✅'

        except ValueError:
             return False, "LA FECHA DE CONSULTA FUE MAL INGRESADA.❎"
        
    def ejecutar_mostrar_consultas(self):
        consultas = self.consulta_repository.mostrar_consultas()
        if len(consultas) == 0:
            return None, 'NO HAY CONSULTAS REGISTRADAS.❎'
        
        return consultas, None

    def ejecutar_consulta_mas_cara(self):
        consulta = self.consulta_repository.consulta_mas_cara()
        if consulta is None:
            return None, 'NO HAY CONSULTAS REGISTRADAS.❎'
        
        return consulta, None
    
    def ejecutar_estadisticas_costo(self):
        estadistica = self.consulta_repository.estadisticas_costo()
        if estadistica is None:
            return None, 'NO HAY CONSULTAS REGISTRADAS.❎'
        
        return estadistica, None
    
    def ejecutar_buscar_consulta(self, fechas):
        try:
            fecha_inicio = datetime.strptime(fechas['inicio'], "%Y-%m-%d")
            fecha_final = datetime.strptime(fechas['final'], "%Y-%m-%d")

            if fecha_inicio and fecha_final:
                fechas['inicio'] = fecha_inicio
                fechas['final'] = fecha_final
                fechas = Consulta(
                    fechas['inicio'],
                    fechas['final']
                )
                consultas = self.consulta_repository.buscar_consulta(fechas)
                if len(consultas) == 0:
                    return None, 'NO HAY CONSULTAS REGISTRADAS EN ESAS FECHAS.❎'
                
                return consultas, None
        
        except ValueError:
            return False, '❌ERROR EN EL FORMATO DE LAS FECHAS INTRODUCCIDAS.'