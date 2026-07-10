import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.medico_controller import MedicoController

controller = MedicoController()

def registrar_medico():
    limpiar_pantalla()
    print("--- REGISTRO DE MEDICO EN EL SISTEMA👨‍⚕️ ---")
    datos = {
        'nombre': input("INGRESA EL NOMBRE DEL MEDICO: ").title(),
        'especialidad': input("INGRESA LA ESPECIALIDAD: ").title(),
        'salario': int(input("INGRESA EL SALARIO: ")),
        'turno': input("INGRESA EL TURNO DE LABORAL (MAÑANA, TARDE, NOCHE): ").capitalize()
        }
    
    medico, mensaje = controller.registrar_medico(datos)
    
    if medico:
        limpiar_pantalla()
        print(mensaje)
        time.sleep(2)
        limpiar_pantalla()

    else:
        limpiar_pantalla()
        print(f"❌ERROR: {mensaje}")
        time.sleep(2)
        limpiar_pantalla()