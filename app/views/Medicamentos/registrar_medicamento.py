import time
from app.utils.limpiar_consola import limpiar_pantalla

def solicitar_datos():
    limpiar_pantalla()
    try:
        print("--- REGISTRANDO MEDICAMENTO AL SISTEMA💊 ---")
        datos = {
            'nombre':      input("INGRESA EL NOMBRE DEL MEDICAMENTO: ").capitalize(),
            'laboratorio': input("INGRESA EL LABORATORIO: ").capitalize(),
            'precio':      float(input("INGRESA EL PRECIO DEL MEDICAMENTO: ")),
            'stock':       int(input("INGRESA LA CANTIDAD EN STOCK: "))
        }

        return datos
    
    except ValueError:
        return None

def mostrar_mensaje_error(mensaje):
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()

def mostrar_mensaje_exito(mensaje):
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()