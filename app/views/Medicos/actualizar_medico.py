import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.medico_controller import MedicoController

controller = MedicoController()

def actualizar_medico():
    medicos, mensaje = controller.mostrar_medicos()
    limpiar_pantalla()
   
    if medicos:
        print("--- MEDICOS REGISTRADO EN EL SISTEMA👨‍⚕️ ---")
        for medico in medicos:
            print(f"ID: {medico.id} | NOMBRE: {medico.nombre:<5} | ESPECIALIDAD: {medico.especialidad} | SALARIO: {medico.salario} | TURNO: {medico.turno}")
        time.sleep(2)
    else:
        print(f"❌ERROR: {mensaje}")

    print("--- ACTUALIZACION DE DATOS DE MEDICO EN EL SISTEMA👨‍⚕️ ---")
    datos = {
        'id': int(input("INGRESE EL ID DEL MEDICO: ")),
        'nombre': input("INGRESA EL NOMBRE DEL MEDICO: ").title(),
        'especialidad': input("INGRESA LA ESPECIALIDAD: ").title(),
        'salario': int(input("INGRESA EL SALARIO: ")),
        'turno': input("INGRESA EL TURNO DE LABORAL (MAÑANA, TARDE, NOCHE): ").capitalize()
        }
    
    medico, mensaje = controller.actualizar_medico(datos)
    
    if medico:
        print("\n--- DATOS ACTUALIZADOS DEL MEDICO👨‍⚕️ ---")
        print(f"NOMBRE:         {medico.nombre}")
        print(f"ESPECIALIDAD:   {medico.especialidad}")
        print(f"SALARIO:        {medico.salario}")
        print(f"TURNO:          {medico.turno}")
        time.sleep(2)
        limpiar_pantalla()

    else:
        limpiar_pantalla()
        print(f"❌ERROR: {mensaje}")
        time.sleep(2)
        limpiar_pantalla()