from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.paciente_controller import PacienteController
import time

controller = PacienteController()

def ver_historial():
    pacientes, mensaje = controller.mostrar_paciente()
    
    if not pacientes:
        print(mensaje)
        time.sleep(2)
        limpiar_pantalla()
        return
    
    print("PACIENTES REGISTRADOS EN EL SISTEMA🤒")
    for paciente in pacientes:
        print(f"ID: {paciente.id} | NOMBRE: {paciente.nombre} | EDAD: {paciente.edad}")

    try:
        id = int(input("INGRESA EL ID DEL PACIENTE PARA VISUALIZAR SU HISTORIAL: "))
    except ValueError:
        print("ERROR INGRESANDO LOS DATOS.❎")
        time.sleep(2)
        limpiar_pantalla()
        return
    
    historial, mensaje = controller.mostrar_historial(id)
    if historial:
        for consulta in historial:
            print(f"MEDICO: {consulta.medico} | COSTO: {consulta.costo} | DIAGNOSTICO: {consulta.diagnostico} | MEDICAMENTO: {consulta.medicamento}")
        time.sleep(2)
        limpiar_pantalla()

    else:
        print(mensaje)
        time.sleep(2)
        limpiar_pantalla()