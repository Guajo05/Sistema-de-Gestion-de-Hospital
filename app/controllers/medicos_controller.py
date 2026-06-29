from app.models.medicos_model import registrar_medico, consultas_por_medicos, medicos_ocupados
from app.views.Medicos.registrar_medico import (solicitar_datos, mostrar_mensaje_error, mostrar_mensaje_exito)
from app.views.Medicos.consultas_por_medico import mostrar_consulta_por_medico
from app.views.Medicos.medicos_ocupados import mostrar_medicos_ocupados


def ejecutar_registro_medico():
    datos = solicitar_datos() 
    turnos = ["Mañana", "Tarde", "Noche"]

    if datos is None:
        mostrar_mensaje_error("DATOS INVALIDOS.❎")
        return
    
    if datos['turno'] not in turnos:
        mostrar_mensaje_error('ESE TURNO NO ESTA DISPONIBLE')
        return

    try:
        resultado = registrar_medico(datos)

        if resultado:
            mostrar_mensaje_exito(f"EL MEDICO '{datos['nombre']} SE REGISTRO CORRECTAMENTE.✅'")
            return
    
    except Exception:
        mostrar_mensaje_error("❌ERROR; REGISTRANDO LOS DATOS.")

def ejecutar_consultas_por_medicos():
    consultas = consultas_por_medicos()

    if len(consultas) == 0:
        mostrar_mensaje_error("NO HAY MEDICOS REGISTRADOS.❎")
        return

    try:
        if consultas:
            mostrar_consulta_por_medico(consultas)
    
    except Exception:
        mostrar_mensaje_error("❌ERROR; RECOLECTANDO LOS DATOS.")

def ejecutar_mostrar_medicos_ocupados():
    medicos = medicos_ocupados()

    try:
        if len(medicos) == 0:
            mostrar_mensaje_error("NO HAY MEDICOS REGISTRADOS.❎")
            return
        
        mostrar_medicos_ocupados(medicos)
    
    except Exception:
        mostrar_mensaje_error("❌ERROR; SOLICITANDO LOS DATOS.")