import time
from app.controllers.paciente_controller import PacienteController
from app.utils.limpiar_consola import limpiar_pantalla

controller = PacienteController()

def registrar_paciente():
    limpiar_pantalla()
    print("--- REGISTRO DE PACIENTE EN EL SISTEMA🤒 ---")
    datos = {
    "nombre":   input("INGRESA EL NOMBRE DEL PACIENTE: ").title(), 
    "edad":     int(input("INGRESA LA EDAD DEL PACIENTE: ")),
    "sangre":   input("INGRESA LA SANGRE DEL PACIENTE('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'): ").upper(),
    "ciudad":   input("INGRESA LA CIUDAD DEL PACIENTE: ").title()}

    paciente, mensaje = controller.registrar_paciente(datos)
    
    if paciente:
        limpiar_pantalla()
        print(mensaje)
        time.sleep(2)

    else:
        limpiar_pantalla()
        print(f'❌ERROR: {mensaje}')
        time.sleep(2)
        return