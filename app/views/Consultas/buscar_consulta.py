import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.consulta_controller import ConsultaController

controller = ConsultaController()

def solicitar_fechas():
    limpiar_pantalla()
    print("--- BUSCAR CONSULTAS POR FECHAS🔍")
    fechas = {
        "fecha_incio": input("INGRESA LA FECHA DE INICIO (AAAA-MM-DD): "),
        "fecha_fin": input("INGRESA LA FECHA DE FIN (AAAA-MM-DD): ")
        }

    return fechas

def mostrar_busqueda_consultas():
    fechas = solicitar_fechas()
    consultas, mensaje = controller.buscar_consultas(fechas)
    if consultas:
        print("--- RESULTADOS DE BUSQUEDA🩻 ---")
        for c in consultas:
            print(f"ID CONSULTA     :{c.id:<10}    | PACIENTE       :{c.paciente}")
            print(f"MEDICO          :{c.medico:<5} | COSTO          :{c.costo}")
        time.sleep(2)
        limpiar_pantalla()
    else:
        print(mensaje)
