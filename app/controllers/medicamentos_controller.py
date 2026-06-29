from app.views.Medicamentos.registrar_medicamento import solicitar_datos, mostrar_mensaje_error, mostrar_mensaje_exito
from app.views.Medicamentos.top_medicamentos import mostrar_top_medicamentos
from app.models.medicamentos_model import registrar_medicamento, top_medicamentos

def ejecutar_registrar_medicamento():
    datos = solicitar_datos()
    
    if datos is None:
        mostrar_mensaje_error("DATOS INVALIDOS.❎")
        return

    if datos['stock'] < 0:
        mostrar_mensaje_error("LA CANTIDAD DEBE SER POSITIVA.❎")
        return
    
    try:
        resultado = registrar_medicamento(datos)

        if resultado:
            mostrar_mensaje_exito("EL MEDICAMENTO SE REGISTRO CORRECTAMENTE.✅")
            return
    
    except Exception:
        mostrar_mensaje_error("❌ERROR; REGISTRANDO LOS DATOS.")

def ejecutar_mostrar_top_medicamentos():
    try:
        medicamentos = top_medicamentos()

        if len(medicamentos) == 0:
            mostrar_mensaje_error("NO HAY MEDICAMENTOS REGISTRADOS.❎")

        if medicamentos:
            mostrar_top_medicamentos(medicamentos)
    
    except Exception:
        mostrar_mensaje_error("❌ ERROR SOLICITANDOS LOS DATOS.")