import time
from app.utils.limpiar_consola import limpiar_pantalla

def mostrar_consulta_mas_cara(consulta):
    limpiar_pantalla()
    print("--- CONSULTA MAS CARA REGISTRADA💸 ---")
    for c in consulta:
        print(f"PACIENTE:       {c['paciente']}")
        print(f"MEDICO:         Dr.{c['medico']}")
        print(f"DIAGNOSTICO:    {c['diagnostico']}")
        print(f"COSTO:          {c['costo']}")
        print(f"FECHA:          {c['fecha']}")
    time.sleep(2)
    limpiar_pantalla()

def mostrar_mensaje_error(mensaje):
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()