import time
from app.utils.limpiar_consola import limpiar_pantalla

def solicitar_datos():
    limpiar_pantalla()
    try:
        print("--- REGISTRO DE MEDICO EN EL SISTEMA👨‍⚕️ ---")
        datos = {
            'nombre': input("INGRESA EL NOMBRE DEL MEDICO: ").title(),
            'especialidad': input("INGRESA LA ESPECIALIDAD: ").title(),
            'salario': input("INGRESA EL SALARIO: "),
            'turno': input("INGRESA EL TURNO DE LABORAL (MAÑANA, TARDE, NOCHE): ").capitalize()
        }

        return datos
    
    except ValueError as e:
        return None

def mostrar_mensaje_error(mensaje):
    limpiar_pantalla()
    print(mensaje)
    time.sleep(2)

def mostrar_mensaje_exito(mensaje):
    limpiar_pantalla()
    print(mensaje)
    time.sleep(2)