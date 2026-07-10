from app.views.Menus.menu_consultas import menu_consultas
from app.views.Menus.menu_medicamentos import menu_medicamentos
from app.views.Menus.menu_medicos import menu_medicos
from app.views.Menus.menu_pacientes import menu_pacientes
from app.views.Menus.menu_recetas import menu_recetas
from app.views.Informe.resumen_ventas import solicitar_nombre_archivo
from app.utils.limpiar_consola import limpiar_pantalla
import time

def menu_principal():
    while True:
        limpiar_pantalla()
        print("---- SISTEMA DE GESTION DE HOSPITAL🏥 ----\n")
        print("----           MENU PRINCIPAL          ----")
        print("1. GESTIONAR PACIENTES.")
        print("2. GESTIONAR MEDICOS.")
        print("3. GESTIONAR CONSULTAS.")
        print("4. GESTIONAR MEDICAMENTOS.")
        print("5. GESTIONAR RECETAS.")
        print("6. EXPORTAR INFORME.")
        print("7. SALIR DEL SISTEMA.")

        try:
            opcion = int(input("\nINGRESA UNA OPCION DEL MENU: "))

            if opcion == 1:
                menu_pacientes()

            elif opcion == 2:
                menu_medicos()

            elif opcion == 3:
                menu_consultas()

            elif opcion == 4:
                menu_medicamentos()

            elif opcion == 5:
                menu_recetas()

            elif opcion == 6:
                solicitar_nombre_archivo()
            
            elif opcion == 7:
                print("GRACIAS POR UTILIZAR NUESTRO SISTEMA.😁🔥👾")
                time.sleep(2)
                limpiar_pantalla()
                break
            else: 
                print("ERROR; ESA OPCION NO ESTA DISPONIBLE EN EL MENU.❎")

        except ValueError:
            print("❌ERROR; LA OPCION INGRESADA DEBE SER UN NUMERO DEL MENU.")