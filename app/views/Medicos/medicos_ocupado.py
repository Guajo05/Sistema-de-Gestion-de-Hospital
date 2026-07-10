import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.medico_controller import MedicoController

controller = MedicoController()

def mostrar_medicos_ocupados():
    limpiar_pantalla()
    resultado, datos = controller.medicos_ocupados()
    if resultado:
        medicos = datos
        print("--- MEDICOS OCUPADOS👨‍⚕️ ---")
        for medico in medicos:
            print(f"MEDICO: Dr.{medico.nombre:<5} | ESPECIALIDAD: {medico.especialidad:<5} | TOTAL DE CONSULTAS: {medico.total}")
        time.sleep(2)
        limpiar_pantalla()

    else:
        print(f"❌ERROR: {datos}")
        time.sleep(2)
        limpiar_pantalla()