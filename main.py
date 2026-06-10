from CRUD import *
import time
import os
import subprocess

def limpiar_consola():
    comando = "cls" if os.name == "nt" else "clear"
    subprocess.run(comando, shell=True)


# ===================== PACIENTES =====================
def Sub_Menu_Pacientes():
    while True:
        limpiar_consola()
        print("--- SISTEMA HOSPITALARIO 🏥 ---")
        print("""
--- GESTIÓN DE PACIENTES 🤒 ---
1. Registrar Paciente
2. Ver Historial de Paciente
3. Pacientes Sin Consultas
4. Regresar al Menú Principal
""")

        try:
            opcion = int(input("INGRESA UNA OPCIÓN: "))

            if opcion == 1:
                Registrar_Pacientes()

            elif opcion == 2:
                Ver_Historial_Paciente()

            elif opcion == 3:
                Pacientes_Sin_Consultas()

            elif opcion == 4:
                print("VOLVIENDO AL MENÚ PRINCIPAL...")
                time.sleep(2)
                break

            else:
                print("❌ OPCIÓN NO DISPONIBLE")
                time.sleep(2)

        except ValueError:
            print("❌ DEBES INGRESAR UN NÚMERO")
            time.sleep(2)


# ===================== MEDICOS =====================
def Sub_Menu_Medicos():
    while True:
        limpiar_consola()
        print("--- SISTEMA HOSPITALARIO 🏥 ---")
        print("""
--- GESTIÓN DE MÉDICOS 👨‍⚕️ ---
1. Registrar Médico
2. Consultas por Médico
3. Médicos Más Ocupados
4. Regresar al Menú Principal
""")

        try:
            opcion = int(input("INGRESA UNA OPCIÓN: "))

            if opcion == 1:
                Registrar_Medicos()

            elif opcion == 2:
                Consultas_Por_Medico()

            elif opcion == 3:
                Medicos_Ocupados()

            elif opcion == 4:
                print("VOLVIENDO AL MENÚ PRINCIPAL...")
                time.sleep(2)
                break

            else:
                print("❌ OPCIÓN NO DISPONIBLE")
                time.sleep(2)

        except ValueError:
            print("❌ DEBES INGRESAR UN NÚMERO")
            time.sleep(2)


# ===================== CONSULTAS =====================
def Sub_Menu_Consultas():
    while True:
        limpiar_consola()
        print("--- SISTEMA HOSPITALARIO 🏥 ---")
        print("""
--- GESTIÓN DE CONSULTAS 🩻 ---
1. Registrar Consulta
2. Buscar Consulta por Fecha
3. Consulta Más Cara
4. Estadísticas de Costos
5. Regresar al Menú Principal
""")

        try:
            opcion = int(input("INGRESA UNA OPCIÓN: "))

            if opcion == 1:
                Registrar_Consultas()

            elif opcion == 2:
                Buscar_Consulta()

            elif opcion == 3:
                Consulta_Mas_Cara()

            elif opcion == 4:
                Estadisticas_Costo()

            elif opcion == 5:
                print("VOLVIENDO AL MENÚ PRINCIPAL...")
                time.sleep(2)
                break

            else:
                print("❌ OPCIÓN NO DISPONIBLE")
                time.sleep(2)

        except ValueError:
            print("❌ DEBES INGRESAR UN NÚMERO")
            time.sleep(2)


# ===================== MEDICAMENTOS =====================
def Sub_Menu_Medicamentos():
    while True:
        limpiar_consola()
        print("--- SISTEMA HOSPITALARIO 🏥 ---")
        print("""
--- GESTIÓN DE MEDICAMENTOS 💊 ---
1. Registrar Medicamento
2. Top 5 Medicamentos Más Recetados
3. Regresar al Menú Principal
""")

        try:
            opcion = int(input("INGRESA UNA OPCIÓN: "))

            if opcion == 1:
                Registrar_Medicamentos()

            elif opcion == 2:
                Top_Medicamentos()

            elif opcion == 3:
                print("VOLVIENDO AL MENÚ PRINCIPAL...")
                time.sleep(2)
                break

            else:
                print("❌ OPCIÓN NO DISPONIBLE")
                time.sleep(2)

        except ValueError:
            print("❌ DEBES INGRESAR UN NÚMERO")
            time.sleep(2)


# ===================== RECETAS =====================
def Sub_Menu_Recetas():
    while True:
        limpiar_consola()
        print("--- SISTEMA HOSPITALARIO 🏥 ---")
        print("""
--- GESTIÓN DE RECETAS 📋 ---
1. Emitir Receta Médica
2. Regresar al Menú Principal
""")

        try:
            opcion = int(input("INGRESA UNA OPCIÓN: "))

            if opcion == 1:
                Emitir_Recetas()

            elif opcion == 2:
                print("VOLVIENDO AL MENÚ PRINCIPAL...")
                time.sleep(2)
                break

            else:
                print("❌ OPCIÓN NO DISPONIBLE")
                time.sleep(2)

        except ValueError:
            print("❌ DEBES INGRESAR UN NÚMERO")
            time.sleep(2)


# ===================== MENU PRINCIPAL =====================
def Menu_Principal():

    Crear_Tablas()

    while True:
        limpiar_consola()

        print("""
╔════════════════════════════════════╗
║     SISTEMA HOSPITALARIO 🏥        ║
╚════════════════════════════════════╝
""")

        print("""
1. Gestión de Pacientes
2. Gestión de Médicos
3. Gestión de Consultas
4. Gestión de Medicamentos
5. Gestión de Recetas
6. Salir del Sistema
""")

        try:
            opcion = int(input("INGRESA UNA OPCIÓN: "))

            if opcion == 1:
                Sub_Menu_Pacientes()

            elif opcion == 2:
                Sub_Menu_Medicos()

            elif opcion == 3:
                Sub_Menu_Consultas()

            elif opcion == 4:
                Sub_Menu_Medicamentos()

            elif opcion == 5:
                Sub_Menu_Recetas()

            elif opcion == 6:
                print("GRACIAS POR UTILIZAR EL SISTEMA HOSPITALARIO 🏥")
                time.sleep(2)
                limpiar_consola()
                break

            else:
                print("❌ OPCIÓN NO DISPONIBLE")
                time.sleep(2)

        except ValueError:
            print("❌ DEBES INGRESAR UN NÚMERO")
            time.sleep(2)


if __name__ == "__main__":
    Menu_Principal()