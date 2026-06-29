import time
from app.utils.limpiar_consola import limpiar_pantalla

def ver_medicamentos(medicamentos):
    limpiar_pantalla()
    print("--- MEDICAMENTOS REGISTRADOS EN EL SISTEMA💊 ---")
    for medicamento in medicamentos:
        print(f"ID: {medicamento['id']} | NOMBRE: {medicamento['NOMBRE']:<5} | STOCK: {medicamento['stock']}")
    time.sleep(2)

def ver_consultas(consultas):
    print("--- CONSULTAS REGISTRADAS EN EL SISTEMA🩻 ---")
    for consulta in consultas:
        print(f"ID: {consulta['id_consulta']} | PACIENTE: {consulta['nombre_paciente']:<5} | MEDICO: {consulta['nombre_medico']:<5} | FECHA: {consulta['fecha']}")
    time.sleep(2)

def solicitar_datos():
    try:
        print("--- REGISTRANDO RECETAS EN EL SISTEMA🏥 ---")
        datos = {
            'medicamento_id': int(input("INGRESA EL ID DEL MEDICAMENTO: ")),
            'consulta_id': int(input("INGRESA EL ID DE LA CONSULTA: ")),
            'cantidad': int(input("INGRESA LA CANTIDAD DEL MEDICAMENTO: ")),
            'dosis': input("INGRESA LA DOSIS DEL MEDICAMENTO: ").title(),
            'dias': int(input("INGRESA CANTIDAD DE DIAS QUE DEBE CONSUMIR ESTE MEDICAMENTO: "))
        }

        return datos
    
    except ValueError:
        return None
    

def mostrar_mensaje_error(mensaje):
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()

def mostrar_mensaje_exito(mensaje):
    print(mensaje)
    time.sleep(2)
    limpiar_pantalla()