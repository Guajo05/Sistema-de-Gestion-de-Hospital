from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.pacientes_controller import (ejecutar_registrar_pacientes, ejecutar_mostrar_pacientes_sin_consulta)
import time

def menu_pacientes():
    limpiar_pantalla()
    while True:
        print("--- MENU DE GESTION DE PACIENTES🤒 ---")
        print("1. REGISTRAR PACIENTE.")
        print("2. VER PACIENTES SIN CONSULTAS.")
        print("3. VOLVER AL MENU PRINCIPAL.")

        try:
            opcion = int(input("\nINGRESA UNA OPCION DEL MENU: "))

            if opcion == 1:
                ejecutar_registrar_pacientes()

            elif opcion == 2:
                ejecutar_mostrar_pacientes_sin_consulta()

            elif opcion == 3:
                time.sleep(1)
                break

            else: 
                print("ERROR; ESA OPCION NO ESTA DISPONIBLE EN EL MENU.❎")
                limpiar_pantalla()

        except ValueError:
            print("❌ERROR; LA OPCION INGRESADA DEBE SER UN NUMERO DEL MENU.")
            limpiar_pantalla()