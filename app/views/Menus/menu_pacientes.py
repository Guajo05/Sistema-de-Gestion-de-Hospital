from app.utils.limpiar_consola import limpiar_pantalla
from app.views.Pacientes import (registrar_pacientes,
                                 actualizar_paciente,
                                 eliminar_paciente,
                                 mostrar_historial,
                                 pacientes_sin_consultas)
import time

def menu_pacientes():
    limpiar_pantalla()
    while True:
        print("--- MENU DE GESTION DE PACIENTES🤒 ---")
        print("1. REGISTRAR PACIENTE.")
        print("2. ACTUALIZAR DATOS PACIENTE")
        print("3. ELIMINAR PACIENTE")
        print("4. MOSTRAL HISTORIAL DE PACIENTE")
        print("5. VER PACIENTES SIN CONSULTAS.")
        print("6. VOLVER AL MENU PRINCIPAL.")
        
        try:
            opcion = int(input("\nINGRESA UNA OPCION DEL MENU: "))

        except ValueError:
            print("❌ ERROR; LA OPCION DEL MENU DEBE SER UN NUMERO.")
            time.sleep(2)
            continue

        if opcion == 1:
            registrar_pacientes.registrar_paciente()

        elif opcion == 2:
            actualizar_paciente.actualizar_paciente()

        elif opcion == 3:
            eliminar_paciente.eliminar_paciente()

        elif opcion == 4:
            mostrar_historial.ver_historial()

        elif opcion == 5:
            pacientes_sin_consultas.mostrar_pacientes_sin_consulta()

        elif opcion == 6:
            time.sleep(2)
            break
        else:
            print("ESA OPCION NO EXISTE.")