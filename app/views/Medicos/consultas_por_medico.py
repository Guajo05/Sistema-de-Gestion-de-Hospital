import time
from app.utils.limpiar_consola import limpiar_pantalla

def mostrar_consulta_por_medico(consultas):
    print("--- CONSULTAS ANTENDIDAS POR MEDICOS👨‍⚕️ ---")
    for consulta in consultas:
        print(f"MEDICO: DR.{consulta['nombre']:<5} | ESPECIALIDAD: {consulta['especialidad']:<5} | TOTAL DE CONSULTAS: {consulta['total']}")
    time.sleep(2)
    limpiar_pantalla()

def mostrar_mensaje_error(mensaje):
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()