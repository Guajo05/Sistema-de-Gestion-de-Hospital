from app.utils.limpiar_consola import limpiar_pantalla
from app.views.Recetas import registrar_recetas
import time

def menu_recetas():
    limpiar_pantalla()
    while True:
        print("MENU DE GESTION DE RECETAS MEDICAS🩻 ---")
        print("1. EMITIR RECETA.")
        print("2. VOLVER AL MENU PRINCIPAL.")
        
        try:
            opcion = int(input("INGRESA UNA OPCION DEL MENU: "))

            if opcion == 1:
                registrar_recetas.registrar_receta()
            
            elif opcion == 2:
                time.sleep(2)
                break

            else: 
                print("ERROR; ESA OPCION NO ESTA DISPONIBLE EN EL MENU.❎")

        except ValueError:
            print("❌ERROR; LA OPCION INGRESADA DEBE SER UN NUMERO DEL MENU.")