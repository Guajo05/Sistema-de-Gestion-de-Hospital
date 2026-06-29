import time
from app.utils.limpiar_consola import limpiar_pantalla

def solicitar_fechas():
    limpiar_pantalla()
    print("--- BUSCAR CONSULTAS POR FECHAS🔍")
    try:
        fecha_incio = input("INGRESA LA FECHA DE INICIO (AAAA-MM-DD): ")
        fecha_fin = input("INGRESA LA FECHA DE FIN (AAAA-MM-DD): ")

        return fecha_incio, fecha_fin

    except ValueError:
        return None

def mostrar_busqueda_consultas(consultas):
    print("--- RESULTADOS DE BUSQUEDA🩻 ---")
    for c in consultas:
        print(f"ID CONSULTA     :{c['id']:<10}    | PACIENTE       :{c['paciente']}")
        print(f"MEDICO          :{c['medico']:<5} | DIAGNOSTICO    :{c['diagnostico']:<5}")
        print(f"COSTO           :{c['costo']:<5}  | FECHA          :{c['fecha']}")
    time.sleep(2)
    limpiar_pantalla()

def mostrar_mensaje_error(mensaje):
    limpiar_pantalla()
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()
