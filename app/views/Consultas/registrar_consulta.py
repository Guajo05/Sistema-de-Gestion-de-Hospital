import time
from app.utils.limpiar_consola import limpiar_pantalla

def ver_medicos(medicos):
    limpiar_pantalla()
    print("--- MEDICOS REGISTRADO EN EL SISTEMA👨‍⚕️ ---")
    for medico in medicos:
        print(f"ID: {medico['id']} | NOMBRE: {medico['nombre']:<5} | ESPECIALIDAD: {medico['especialidad']}")
    time.sleep(2)
    print()

def ver_pacientes(pacientes):
    limpiar_pantalla()
    print("--- PACIENTES REGISTRADO EN EL SISTEMA🤒 ---")
    for paciente in pacientes:
        print(f"ID: {paciente['id']} | NOMBRE: {paciente['nombre']:<5} | CIUDAD: {paciente['ciudad']}")
    time.sleep(2)
    print()

def solicitar_datos():
    limpiar_pantalla()
    try:
        print("--- REGISTRANDO CONSULTA EN EL SISTEMA🩻 ---")
        datos = {
            'fecha_consulta': input("INGRESA LA FECHA PARA LA CONSULTA (AAAA-MM-DD): "),
            'diagnostico': input("INGRESA EL DIAGNOSTICO DEL PACIENTE: ").title(),
            'costo': float(input("INGRESA EL COSTO DE LA CONSULTA: ")),
            'medico_id': int(input("INGRESA EL ID DEL MEDICO PARA LA CONSULTA: ")),
            'paciente_id': int(input("INGRESA EL ID DEL PACIENTE PARA LA CONSULTA: "))
        }

        return datos
    
    except ValueError:
        return None
    
def mostrar_mensaje_error(mensaje):
    limpiar_pantalla()
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()

def mostrar_mensaje_exito(mensaje):
    limpiar_pantalla()
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()