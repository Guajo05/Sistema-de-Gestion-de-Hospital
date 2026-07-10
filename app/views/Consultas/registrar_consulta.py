import time
from app.utils.limpiar_consola import limpiar_pantalla
from app.controllers.consulta_controller import ConsultaController
from app.controllers.medico_controller import MedicoController
from app.controllers.paciente_controller import PacienteController

c_controller = ConsultaController()
m_controller = MedicoController()
p_controller = PacienteController()


def ver_medicos():
    medicos, mensaje = m_controller.mostrar_medicos()
    limpiar_pantalla()
    if medicos:
        print("--- MEDICOS REGISTRADO EN EL SISTEMA👨‍⚕️ ---")
        for medico in medicos:
            print(f"ID: {medico.id} | NOMBRE: {medico.nombre:<5} | ESPECIALIDAD: {medico.especialidad}")
        time.sleep(2)
    else:
        print(f"❌ERROR: {mensaje}")
        limpiar_pantalla()

def ver_pacientes():
    pacientes, mensaje = p_controller.mostrar_paciente()
    if pacientes:
        print("--- PACIENTES REGISTRADO EN EL SISTEMA🤒 ---")
        for paciente in pacientes:
            print(f"ID: {paciente.id} | NOMBRE: {paciente.nombre:<5} | CIUDAD: {paciente.ciudad}")
        time.sleep(2)
    else:
        print(f"❌ERROR: {mensaje}")
        limpiar_pantalla()

def solicitar_datos():
    print("--- REGISTRANDO CONSULTA EN EL SISTEMA🩻 ---")
    datos = {
            'medico': int(input("INGRESA EL ID DEL MEDICO PARA LA CONSULTA: ")),
            'paciente': int(input("INGRESA EL ID DEL PACIENTE PARA LA CONSULTA: ")),
            'fecha': input("INGRESA LA FECHA PARA LA CONSULTA (AAAA-MM-DD): "),
            'diagnostico': input("INGRESA EL DIAGNOSTICO DEL PACIENTE: ").title(),
            'costo': float(input("INGRESA EL COSTO DE LA CONSULTA: ")),
        }
    return datos

def registrar_consulta():
    ver_medicos()
    ver_pacientes()
    datos = solicitar_datos()
    resultado, mensaje = c_controller.registrar_consulta(datos)

    if resultado:
        print(mensaje)
        time.sleep(2)
        limpiar_pantalla()

    else:
        print(mensaje)
        time.sleep(2)
        limpiar_pantalla()