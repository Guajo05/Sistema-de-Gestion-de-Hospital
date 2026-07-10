import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.medico_controller import MedicoController

controller = MedicoController()

def mostrar_consulta_por_medico():
    resultado, datos = controller.consultas_medicos()
    if resultado:
        consultas = datos
        limpiar_pantalla()
        print("--- CONSULTAS ANTENDIDAS POR MEDICOS👨‍⚕️ ---")
        for consulta in consultas:
            print(f"MEDICO: DR.{consulta['nombre']:<5} | ESPECIALIDAD: {consulta['especialidad']:<5} | TOTAL DE CONSULTAS: {consulta['total']}")
        time.sleep(2)
        limpiar_pantalla()
    
    else:
        limpiar_pantalla()
        print(f"❌ERORR: {datos}")
        time.sleep(2)
        limpiar_pantalla()