import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.consulta_controller import ConsultaController

controller = ConsultaController()

def mostrar_consulta_mas_cara():
    consulta, mensaje = controller.consulta_mas_cara()
    limpiar_pantalla()
    if consulta:
        print("--- CONSULTA MAS CARA REGISTRADA💸 ---")
        print(f"PACIENTE:       {consulta.paciente}")
        print(f"MEDICO:         Dr.{consulta.medico}")
        print(f"DIAGNOSTICO:    {consulta.diagnostico}")
        print(f"COSTO:          {consulta.costo}")
        print(f"FECHA:          {consulta.fecha}")
        time.sleep(2)
        limpiar_pantalla()
    else:
        print(mensaje)
        time.sleep(2)
        limpiar_pantalla()