from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.consultas_controller import (
    ejecutar_registrar_consuta,
    ejecutar_mostrar_busqueda_consultas,
    ejecutar_ver_historial,
    ejecutar_mostrar_consulta_mas_cara,
    ejecutar_mostrar_estadisticas_costo)

import time

def menu_consultas():
    limpiar_pantalla()
    while True:
        print("--- MENU GESTION DE CONSULTAS🩻 ---")
        print("1. REGISTRAR CONSULTAS.")
        print("2. BUSCAR CONSULTAS.")
        print("3. HISTORIAL DE CONSULTAS.")
        print("4. CONSULTA MAS CARA.")
        print("5. RESUMEN DE CONSULTAS.")
        print("6. VOLVER AL MENU PRINCIPAL")

        try:
            opcion = int(input("\nINGRESA UNA OPCION DEL MENU: "))

            if opcion == 1:
                ejecutar_registrar_consuta()
            
            elif opcion == 2:
                ejecutar_mostrar_busqueda_consultas()

            elif opcion == 3:
                ejecutar_ver_historial()
            
            elif opcion == 4:
                ejecutar_mostrar_consulta_mas_cara()
            
            elif opcion == 5:
                ejecutar_mostrar_estadisticas_costo()
            
            elif opcion == 6:
                time.sleep(1)
                break

            else: 
                print("ERROR; ESA OPCION NO ESTA DISPONIBLE EN EL MENU.❎")

        except ValueError:
            print("❌ERROR; LA OPCION INGRESADA DEBE SER UN NUMERO DEL MENU.")