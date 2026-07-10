import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.consulta_controller import ConsultaController

controller = ConsultaController()

def mostrar_estadisticas_costo():
    estadistica, mensaje = controller.estadisticas_costo()
    limpiar_pantalla()
    if estadistica:
        print("--- RESUMEN DE LAS ESTADISTICAS SOBRE LA CONSULTAS📊 ---")
        print(f"LA CONSULTA MAS BARATA                      :{estadistica.barata}")
        print(f"LA CONSULTA MAS CARA                        :{estadistica.cara}")
        print(f"EL PROMEDIO DE COSTO DE CONSULTAS           :{estadistica.promedio}")
        print(f"TOTAL DE COSTO DE LAS CONSULTAS EMITIDAS    :{estadistica.total}")
        time.sleep(2)
        limpiar_pantalla()
    else:
        print(mensaje)