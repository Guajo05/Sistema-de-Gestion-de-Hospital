from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.medico_controller import MedicoController
import time

controller = MedicoController()

def eliminar_medico():
    medicos, mensaje = controller.mostrar_medicos()
    limpiar_pantalla()
   
    if medicos:
        print("--- MEDICOS REGISTRADO EN EL SISTEMA👨‍⚕️ ---")
        for medico in medicos:
            print(f"ID: {medico.id} | NOMBRE: {medico.nombre:<5} | ESPECIALIDAD: {medico.especialidad} | SALARIO: {medico.salario} | TURNO: {medico.turno}")
        time.sleep(2)
    else:
        print(f"❌ERROR: {mensaje}")
    
    try:
        id = int(input("INGRESE EL ID DEL MEDICO A ELIMINAR DEL SISTEMA: "))
        estado, resultado = controller.eliminar_medico(id)

        if estado is True:
            print(resultado)

        else:
            print(resultado)

    except ValueError:
        print("EL ID DEBE SER NUMERICO.❎")
