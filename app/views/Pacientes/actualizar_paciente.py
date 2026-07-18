import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.paciente_controller import PacienteController

controller = PacienteController()

def actualizar_paciente():
    pacientes, mensaje = controller.mostrar_paciente()
    limpiar_pantalla()
   
    if pacientes:
        print("--- PACIENTES REGISTRADO EN EL SISTEMA👨‍⚕️ ---")
        for paciente in pacientes:
            print(f"ID: {paciente.id} | NOMBRE: {paciente.nombre:<5} | EDAD: {paciente.edad} | SANGRE: {paciente.sangre} | CIUDAD: {paciente.ciudad}")
        time.sleep(2)
    else:
        print(f"❌ERROR: {mensaje}")

    print("--- ACTUALIZACION DE DATOS DE PACIENTE EN EL SISTEMA👨‍⚕️ ---")
    datos = {
        'id':       int(input("INGRESE EL ID DEL PACIENTE: ")),
        "nombre":   input("INGRESA EL NOMBRE DEL PACIENTE: ").title(), 
        "edad":     int(input("INGRESA LA EDAD DEL PACIENTE: ")),
        "sangre":   input("INGRESA LA SANGRE DEL PACIENTE('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'): ").upper(),
        "ciudad":   input("INGRESA LA CIUDAD DEL PACIENTE: ").title()}
    
    paciente, mensaje = controller.actualizar_paciente(datos)
    
    if paciente:
        print("\n--- DATOS ACTUALIZADOS DEL MEDICO👨‍⚕️ ---")
        print(f"NOMBRE:         {paciente.nombre}")
        print(f"EDAD:           {paciente.edad}")
        print(f"TIPO DE SANGRE: {paciente.sangre}")
        print(f"CIUDAD:         {paciente.ciudad}")
        time.sleep(2)
        limpiar_pantalla()

    else:
        limpiar_pantalla()
        print(f"❌ERROR: {mensaje}")
        time.sleep(2)
        limpiar_pantalla()