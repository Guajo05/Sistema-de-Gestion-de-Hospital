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

    def ejecutar_registrar_receta(self, datos: dict) -> tuple:
        if 'consulta' not in datos:
            return None, 'EL ID DE LA CONSULTA DEBE SER REQUERIDO.❎'

        try:
            consulta = int(datos['consulta'])

        except (TypeError, ValueError):
            return None, 'ID INVALIDO.❎'

        if 'medicamento' not in datos:
            return None, 'EL ID DEL MEDICAMENTO DEBE SER REQUERIDO.❎'

        try:
            medicamento = int(datos['medicamento'])

        except (TypeError, ValueError):
            return None, 'ID INVALIDO.❎'

        try:
            cantidad = int(datos.get('cantidad'))

        except (TypeError, ValueError):
            return None, 'LA CANTIDAD DEBE SER UN NUMERO.❎'

        try:
            dias = int(datos.get('dias'))

        except (TypeError, ValueError):
            return None, 'LOS DIAS DE TRATAMIENTO DEBEN SER UN NUMERO.❎'

        dosis = datos.get('dosis')

        if not isinstance(dosis, str) or not dosis.strip():
            return None, 'LA DOSIS DEBE SER OBLIGATORIA.❎'

        if not Validar_Datos_Existente(consulta, self.c_repository.mostrar_consultas(), posicion_id=0):
            return None, 'ESA CONSULTA NO ESTA REGISTRADA.❎'

        medicamentos = self.m_repository.mostrar_medicamentos()

        if not Validar_Datos_Existente(medicamento, medicamentos, posicion_id=0):
            return None, 'ESE MEDICAMENTO NO ESTA REGISTRADO.❎'

        medicamento_obj = next((m for m in medicamentos if m.id == medicamento), None)

        if medicamento_obj is not None and medicamento_obj.stock < cantidad:
            return None, 'NO HAY STOCK SUFICIENTE PARA ESA CANTIDAD.❎'

        receta = Receta(
            medicamento_id=medicamento,
            consulta_id=consulta,
            cantidad=cantidad,
            dosis=dosis,
            dias=dias
        )

        resultado = self.r_repository.registrar_receta(receta)

        if not resultado:
            return None, 'NO SE PUDO REGISTRAR LA RECETA.❎'

        return True, 'RECETA EMITIDA CORRECTAMENTE.✅'

    def ejecutar_mostrar_recetas(self):
        recetas = self.r_repository.mostrar_recetas()

        if not recetas:
            return None, 'NO HAY RECETAS REGISTRADAS.❎'

        return recetas, None