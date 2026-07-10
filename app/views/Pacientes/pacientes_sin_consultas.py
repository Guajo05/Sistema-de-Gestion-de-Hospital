import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.paciente_controller import PacienteController

controller = PacienteController()

def mostrar_pacientes_sin_consulta():
    pacientes, mensaje = controller.pacientes_sin_consultas()
    if pacientes:
        limpiar_pantalla()
        print("--- PACIENTES SIN CONSULTAS🤒 ---")
        for p in pacientes:
            print(f"NOMBRE: {p.nombre:<5} | EDAD: {p.edad:<1} | CIUDAD: {p.ciudad}")
        time.sleep(2)
        limpiar_pantalla()
    else:
        print(mensaje)
        time.sleep(2)
        return