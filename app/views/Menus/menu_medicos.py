from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.medicos_controller import (ejecutar_registro_medico, 
                                            ejecutar_mostrar_medicos_ocupados, 
                                            ejecutar_consultas_por_medicos)
import time

def menu_medicos():
    limpiar_pantalla()
    while True:
        print("--- MENU DE GESTION DE MEDICOS👨‍⚕️ ---")
        print("1. REGISTRAR MEDICO.")
        print("2. VER MEDICOS OCUPADOS.")
        print("3. VER HISTORIAL DE LAS CONSULTAS POR MEDICOS.")
        print("4. VOLVER AL MENU PRINCIPAL")

        try:
            opcion = int(input("\nINGRESA UNA OPCION DEL MENU: "))
            
            if opcion == 1:
                ejecutar_registro_medico()
            
            elif opcion == 2:
                ejecutar_mostrar_medicos_ocupados()

            elif opcion == 3:
                ejecutar_consultas_por_medicos()

            elif opcion == 4:
                time.sleep(1)
                break

            else: 
                print("ERROR; ESA OPCION NO ESTA DISPONIBLE EN EL MENU.❎")

        except ValueError:
            print("❌ERROR; LA OPCION INGRESADA DEBE SER UN NUMERO DEL MENU.")