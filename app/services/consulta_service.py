from app.models.consulta import Consulta
from app.repositories.repository_consulta import ConsultaRepository
from app.repositories.repository_medico import MedicoRepository
from app.repositories.repository_paciente import PacienteRepository
from app.utils.validar_datos import Validar_Datos_Existente
from datetime import datetime

class ConsultaService:
    def __init__(self):
        self.consulta_repository = ConsultaRepository()
        self.paciente_repository = PacienteRepository()
        self.medico_repository = MedicoRepository()

    def ejecutar_registrar_consulta(self, datos):
        if 'paciente' not in datos:
            return None, 'EL PACIENTE ES OBLIGATORIO.❎'

        if 'medico' not in datos:
            return None, 'EL MEDICO ES OBLIGATORIO.❎'

        if not Validar_Datos_Existente(datos['paciente'], self.paciente_repository.mostrar_pacientes(), posicion_id=0):
            return None, "ESE PACIENTE NO ESTA REGISTRADO.❎"

        if not Validar_Datos_Existente(datos['medico'], self.medico_repository.mostrar_medicos(), posicion_id=0):
            return None, "ESE MEDICO NO ESTA REGISTRADO.❎"

        try:
            costo = float(datos.get('costo'))
        except (TypeError, ValueError):
            return None, 'EL COSTO DEBE SER UN NUMERO.❎'

        if costo < 0:
            return None, 'EL COSTO DEBE SER POSITIVO.❎'

        try:
            fecha_formateada = datetime.strptime(datos.get('fecha'), "%Y-%m-%d")
        except (ValueError, TypeError):
            return False, "LA FECHA DE CONSULTA FUE MAL INGRESADA.❎"

        if fecha_formateada.date() < datetime.now().date():
            return None, "NO PUEDES REGISTRAR CONSULTAS PARA EL PASADO.❎"

        consulta = Consulta(
            fecha=fecha_formateada,
            diagnostico=datos.get('diagnostico'),
            costo=costo,
            paciente_id=datos['paciente'],
            medico_id=datos['medico'],
        )

        resultado = self.consulta_repository.registrar_consulta(consulta)

        if not resultado:
            return None, 'ERROR AL REGISTRAR LA CONSULTA.❎'

        return consulta, 'LA CONSULTA SE REGISTRO CORRECTAMENTE.✅'

    def ejecutar_mostrar_consultas(self):
        consultas = self.consulta_repository.mostrar_consultas()
        if not consultas:
            return None, 'NO HAY CONSULTAS REGISTRADAS.❎'

        return consultas, None

    def ejecutar_buscar_consulta(self, fechas):
        try:
            fecha_inicio = datetime.strptime(fechas['inicio'], "%Y-%m-%d")
            fecha_final = datetime.strptime(fechas['final'], "%Y-%m-%d")
        except (ValueError, TypeError, KeyError):
            return False, '❌ERROR EN EL FORMATO DE LAS FECHAS INTRODUCIDAS.'

        if fecha_inicio > fecha_final:
            return False, 'LA FECHA DE INICIO NO PUEDE SER MAYOR A LA FECHA FINAL.❎'

        consultas = self.consulta_repository.buscar_consulta(fecha_inicio, fecha_final)

        if not consultas:
            return None, 'NO HAY CONSULTAS REGISTRADAS EN ESAS FECHAS.❎'

        return consultas, None