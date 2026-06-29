import time
from app.utils.limpiar_consola import limpiar_pantalla

def ver_pacientes(paccientes):
    limpiar_pantalla()
    print("--- PACIENTES REGISTRADOS EN EL SISTEMA🤒 ---")
    for paciente in paccientes:
        print(f"ID: {paciente['id']} | NOMBRE: {paciente['nombre']:<5} | CIUDAD: {paciente['ciudad']}")
    time.sleep(2)

def solicitar_id():
    limpiar_pantalla()
    try:
        print("--- HISTORIAL DE CONSULTASZ🩻 ---")
        id_paciente = int(input("INGRESA EL ID DEL PACIENTE: "))
        return id_paciente
    
    except ValueError:
        return None
    
def mostrar_historial(historial):
    limpiar_pantalla()
    print(f"--- HISTORIAL DE {historia['paciente']}🤒 ---")
    for historia in historial:
        print(f"MEDICO: {historia['medico']:<5} | DIAGNOSTICO: {historia['diagnostico']:<5} | COSTO: {historia['costo']:<5} | MEDICAMENTO: {historia['medicamento']}")
    time.sleep(2)
    limpiar_pantalla()

def mostrar_mensaje_error(mensaje):
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()

def mostrar_mensaje_exito(mensaje):
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()