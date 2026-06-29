from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.medicamentos_controller import (ejecutar_registrar_medicamento, 
                                                 ejecutar_mostrar_top_medicamentos)
import time

def menu_medicamentos():
    limpiar_pantalla()
    while True:
        print("--- MENU DE GESTION DE MEDICAMENTOS💊 ---")
        print("1. REGISTRAR MEDICAMENTO.")
        print("2. VER TOP 5 MEDICAMENTOS.")
        print("3. VOLVER AL MENU PRINCIPAL.")

        try:
            opcion = int(input("\nINGRESA UNA OPCION DEL MENU: "))

            if opcion == 1:
                ejecutar_registrar_medicamento()

            elif opcion == 2:
                ejecutar_mostrar_top_medicamentos()

            elif opcion == 3:
                time.sleep(1)
                break
            
            else: 
                print("ERROR; ESA OPCION NO ESTA DISPONIBLE EN EL MENU.❎")

        except ValueError:
            print("❌ERROR; LA OPCION INGRESADA DEBE SER UN NUMERO DEL MENU.")