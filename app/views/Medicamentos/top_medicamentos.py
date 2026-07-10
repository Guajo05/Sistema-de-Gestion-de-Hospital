import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.medicamento_controller import MedicamentoController

controller = MedicamentoController()

def mostrar_top_medicamentos():
    medicamentos, mensaje = controller.top_medicamentos()
    if medicamentos:
        print("---- TOP 5 DE MEDICAMENTOS RECETADOS💊 ---")
        for m in medicamentos:
            print(f'NOMBRE: {m.nombre:<5} | LABORATORIO: {m.laboratorio:<5} | TOTAL DE RECETAS: {m.total}')
        time.sleep(2)
        limpiar_pantalla()
    
    else:
        limpiar_pantalla()
        print(mensaje)
        time.sleep(2)