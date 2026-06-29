import time
from app.utils.limpiar_consola import limpiar_pantalla

def mostrar_pacientes_sin_consulta(pacientes):
    limpiar_pantalla()
    print("--- PACIENTES SIN CONSULTAS🤒 ---")
    for p in pacientes:
        print(f"NOMBRE: {p['nombre']:<5} | EDAD: {p['edad']:<1} | SANGRE: {p['sangre']:<2} | CIUDAD: {p['ciudad']}")
    time.sleep(2)
    limpiar_pantalla()

def mostrar_mensaje_error(mensaje):
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()