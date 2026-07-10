from app.utils.limpiar_consola import limpiar_pantalla
from app.views.Consultas import (registrar_consulta, 
                                 estadisticas_costo,
                                 consulta_mas_cara, 
                                 buscar_consulta)
import time


def menu_consultas():
    limpiar_pantalla()
    while True:
        print("--- MENU GESTION DE CONSULTAS🩻 ---")
        print("1. REGISTRAR CONSULTAS.")
        print("2. BUSCAR CONSULTAS.")
        print("3. CONSULTA MAS CARA.")
        print("4. RESUMEN DE CONSULTAS.")
        print("5. VOLVER AL MENU PRINCIPAL")

        try:
            opcion = int(input("\nINGRESA UNA OPCION DEL MENU: "))

            if opcion == 1:
                registrar_consulta.registrar_consulta()

            elif opcion == 2:
                buscar_consulta.mostrar_busqueda_consultas()

            elif opcion == 3:
                consulta_mas_cara.mostrar_consulta_mas_cara()
            
            elif opcion == 4:
                estadisticas_costo.mostrar_estadisticas_costo()
            
            elif opcion == 5:
                time.sleep(1)
                break

            else: 
                print("ERROR; ESA OPCION NO ESTA DISPONIBLE EN EL MENU.❎")

        except ValueError:
            print("❌ERROR; LA OPCION INGRESADA DEBE SER UN NUMERO DEL MENU.")