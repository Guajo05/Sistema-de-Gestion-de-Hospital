from app.models.recetas_model import registrar_receta
from app.models.consultas_model import mostrar_consultas
from app.models.medicamentos_model import mostrar_medicamentos
from app.views.Recetas.registrar_recetas import solicitar_datos, mostrar_mensaje_error, mostrar_mensaje_exito
from app.utils.validar_datos import Validar_Datos_Existente

def ejecutar_registrar_recetas():
    datos = solicitar_datos()
    medicamentos = mostrar_medicamentos()
    consultas = mostrar_consultas()

    if len(medicamentos) == 0:
        mostrar_mensaje_error("NO HAY MEDICAMENTOS REGISTRADOS.❎")
        return

    if len(consultas) == 0:
        mostrar_mensaje_error("NO HAY CONSULTAS REGISTRADAS.❎")
        return

    if datos is None:
        mostrar_mensaje_error('DATOS INVALIDOS.❎')
        return

    if not Validar_Datos_Existente(datos['medicamento_id'], medicamentos, posicion_id=0):
        mostrar_mensaje_error("ERROR; ESTE ID NO EXISTE.❎")

    if not Validar_Datos_Existente(datos['consulta_id'], consultas, posicion_id=0):
        mostrar_mensaje_error("ERROR; ESTE ID NO EXSITE.❎")

    if datos['cantidad'] > medicamentos['stock']:
        mostrar_mensaje_error("ERROR; LA CANTIDAD INGRESADA DE MEDICAMENTOS ES MAYOR A LA QUE TENEMOS DISPONIBLES.❎")

    try:
        resultados = registrar_receta(datos)
        if resultados:
            mostrar_mensaje_exito("LA RECETA SE REGISTRO CORRECTAMENTE.✅")

    except Exception:
        mostrar_mensaje_error("❌ERROR REGISTRANDO LOS DATOS.")