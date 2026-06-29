from app.models.pacientes_model import registrar_paciente, pacientes_sin_consultas
from app.views.Pacientes.registrar_paciente import solicitar_datos, mostrar_mensaje_error, mostrar_mensaje_exito
from app.views.Pacientes.pacientes_sin_consultas import mostrar_pacientes_sin_consulta

def ejecutar_registrar_pacientes():
    tipos_de_Sangre = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    datos = solicitar_datos()

    if datos is None:
        mostrar_mensaje_error("DATOS INVALIDOS❎.")
        return

    if datos['edad'] <= 0:
        mostrar_mensaje_error("LA EDAD DEBE SER POSITIVA❎")
        return
    
    if datos['sangre'] not in tipos_de_Sangre:
        mostrar_mensaje_error("ESE TIPO DE SANGRE NO ESTA EN LA LISTA POR LO TANTO NO EXISTE.❎")
        return
    
    try:
        resultado = registrar_paciente(datos)
        if resultado:
            mostrar_mensaje_exito(f"EL PACIENTE '{datos['nombre']}' SE REGISTRO CORRECTAMENTE.✅".upper())
    
    except Exception:
        mostrar_mensaje_error("❌ERROR; REGISTRANDO LOS DATOS.")

def ejecutar_mostrar_pacientes_sin_consulta():
    try:
        pacientes = pacientes_sin_consultas()

        if len(pacientes) == 0:
            mostrar_mensaje_error("NO HAY PACIENTES REGISTRADOS.❎")
            return
        
        if pacientes:
            mostrar_pacientes_sin_consulta(pacientes)

    except Exception:
        mostrar_mensaje_error("❌ERROR SOLICITANDO LOS DATOS.")