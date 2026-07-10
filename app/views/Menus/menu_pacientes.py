from app.utils.limpiar_consola import limpiar_pantalla
from app.views.Pacientes import (registrar_pacientes,
                                 mostrar_historial,
                                 pacientes_sin_consultas)
import time

def menu_pacientes():
    limpiar_pantalla()
    while True:
        print("--- MENU DE GESTION DE PACIENTES🤒 ---")
        print("1. REGISTRAR PACIENTE.")
        print("2. MOSTRAL HISTORIAL DE PACIENTE")
        print("3. VER PACIENTES SIN CONSULTAS.")
        print("4. VOLVER AL MENU PRINCIPAL.")
        
        try:
            opcion = int(input("\nINGRESA UNA OPCION DEL MENU: "))

        except ValueError:
            print("❌ ERROR; LA OPCION DEL MENU DEBE SER UN NUMERO.")
            time.sleep(2)
            continue

        if opcion == 1:
            registrar_pacientes.registrar_paciente()

        elif opcion == 2:
            mostrar_historial.ver_historial()

        elif opcion == 3:
            pacientes_sin_consultas.mostrar_pacientes_sin_consulta()

        elif opcion == 4:
            time.sleep(2)
            break
        else:
            print("ESA OPCION NO EXISTE.")