import time
from app.utils.limpiar_consola import limpiar_pantalla

def solicitar_nombre_archivo():
    limpiar_pantalla()
    print("--- EXPORTACION DE ARCHIVO DEL RESUMEN DE ESTADISTICAS DEL HOSPITAL🏥📊")
    nombre = input("\nINGRESE EL NOMBRE DEL ARCHIVO DEL INFORME: ")

    if not nombre.endswith(".txt"):
        nombre += ".txt"

    return nombre


def mostrar_exito(nombre):
    print(f"\nINFORME GENERANDO CORRECTAMENTE: {nombre}")
    time.sleep(2)
    limpiar_pantalla()


def mostrar_error(error):
    limpiar_pantalla()
    print(error)
    time.sleep(2)
    limpiar_pantalla()