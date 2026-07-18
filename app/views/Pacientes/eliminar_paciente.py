import time
from app.controllers.paciente_controller import PacienteController
from app.utils.limpiar_consola import limpiar_pantalla

controller = PacienteController()

def eliminar_paciente():
    pacientes, mensaje = controller.mostrar_paciente()
    if pacientes:
        print("--- PACIENTES REGISTRADO EN EL SISTEMA🤒 ---")
        for paciente in pacientes:
            print(f"ID: {paciente.id} | NOMBRE: {paciente.nombre:<5} | CIUDAD: {paciente.ciudad}")
        time.sleep(2)
    else:
        print(f"❌ERROR: {mensaje}")
        limpiar_pantalla()

    try:
        id = int(input("INGRESE EL ID DEL PACIENTE A ELIMINAR DEL SISTEMA: "))
        estado, resultado = controller.eliminar_paciente(id)

        if estado is True:
            print(resultado)

        else:
            print(resultado)

    except ValueError:
        print("EL ID DEBE SER NUMERICO.❎")