import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.medicamento_controller import MedicamentoController

controller = MedicamentoController()

def solicitar_datos():
    limpiar_pantalla()
    print("--- REGISTRANDO MEDICAMENTO AL SISTEMA💊 ---")
    datos = {
            'nombre':      input("INGRESA EL NOMBRE DEL MEDICAMENTO: ").capitalize(),
            'laboratorio': input("INGRESA EL LABORATORIO: ").capitalize(),
            'precio':      float(input("INGRESA EL PRECIO DEL MEDICAMENTO: ")),
            'stock':       int(input("INGRESA LA CANTIDAD EN STOCK: "))
        }

    return datos

def registrar_medicamento():
    datos = solicitar_datos()
    resultado, mensaje = controller.registrar_medicamento(datos)
    
    if resultado:
        limpiar_pantalla()
        print(mensaje)
        time.sleep(2)

    else:
        limpiar_pantalla()
        print(mensaje)
        time.sleep(2)
