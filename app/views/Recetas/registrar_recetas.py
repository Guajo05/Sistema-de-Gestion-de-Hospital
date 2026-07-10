import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.consulta_controller import ConsultaController
from app.controllers.medicamento_controller import MedicamentoController
from app.controllers.receta_controller import RecetaController

c_controller = ConsultaController()
m_controller = MedicamentoController()
r_controller = RecetaController()

def ver_medicamentos():
    limpiar_pantalla()
    medicamentos, mensaje = m_controller.mostrar_medicamentos()
    
    if medicamentos:
        print("--- MEDICAMENTOS REGISTRADOS EN EL SISTEMA💊 ---")
        for medicamento in medicamentos:
            print(f"ID: {medicamento.id} | NOMBRE: {medicamento.nombre} | STOCK: {medicamento.stock}")
        time.sleep(2)
    else: 
        print(mensaje)
        time.sleep(2)
        return

def ver_consultas():
    consultas, mensaje = c_controller.mostrar_consultas()
    if consultas:
        print("--- CONSULTAS REGISTRADAS EN EL SISTEMA🩻 ---")
        for consulta in consultas:
            print(f"ID: {consulta.id} | COSTO: {consulta.costo} | FECHA: {consulta.fecha}")
        time.sleep(2)
    else:
        print(mensaje)
        time.sleep(2)
        return

def solicitar_datos():
    try:
        print("--- REGISTRANDO RECETAS EN EL SISTEMA🏥 ---")
        datos = {
            'medicamento': int(input("INGRESA EL ID DEL MEDICAMENTO: ")),
            'consulta': int(input("INGRESA EL ID DE LA CONSULTA: ")),
            'cantidad': int(input("INGRESA LA CANTIDAD DEL MEDICAMENTO: ")),
            'dosis': input("INGRESA LA DOSIS DEL MEDICAMENTO (500 mg CADA 8 HORAS): ").title(),
            'dias': int(input("INGRESA CANTIDAD DE DIAS QUE DEBE CONSUMIR ESTE MEDICAMENTO: "))
        }

        return datos
    
    except ValueError:
        print("❌ERROR INGRESANDO LOS DATOS.")
        time.sleep(2)
        return

def registrar_receta():
    ver_medicamentos()
    ver_consultas()
    datos = solicitar_datos()
    resultado, mensaje = r_controller.registrar_receta(datos)
    if resultado:
        print(mensaje)
        time.sleep(2)
        limpiar_pantalla()
    else:
        print(mensaje)
        time.sleep(2)
        limpiar_pantalla()