import time
from app.utils.limpiar_consola import limpiar_pantalla

def mostrar_medicos_ocupados(medicos):
    limpiar_pantalla()
    print("--- MEDICOS OCUPADOS👨‍⚕️ ---")
    for medico in medicos:
        print(f"MEDICO: Dr.{medico['nombre']:<5} | ESPECIALIDAD: {medico['especialidad']:<5} | TOTAL DE CONSULTAS: {medico['total']}")
    time.sleep()

def mostrar_mensaje_error(mensaje):
    limpiar_pantalla()
    print(mensaje)
    time.sleep(2)