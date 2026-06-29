from app.views.Informe.resumen_ventas import solicitar_nombre_archivo, mostrar_exito, mostrar_error
from app.models.consultas_model import estadisticas_costo, consulta_mas_cara
from app.models.medicamentos_model import top_medicamentos
from app.models.medicos_model import consultas_por_medicos
import os

def ejecutar_exportar_informe():
    try:
        nombre_archivo = solicitar_nombre_archivo()
        estadistica = estadisticas_costo()
        consulta_cara = consulta_mas_cara()
        medicamentos = top_medicamentos()
        consultas = consultas_por_medicos()

        carpeta = "reports"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        ruta_archivo = os.path.join(carpeta, nombre_archivo)

        with open(ruta_archivo, 'w+', encoding='utf-8') as informe:
            informe.write("---- INFORME DE LAS ESTADISTICAS DEL HOSPITAL📊🏥 ----\n")
            informe.write("---- ESTADISTICAS COSTO DE CONSULTAS📊 ----")
            informe.write(f"CONSULTA MAS BARATA                         :{estadistica['barata']}")
            informe.write(f"LA CONSULTA MAS CARA                        :{estadistica['cara']}")
            informe.write(f"EL PROMEDIO DE COSTO DE CONSULTAS           :{estadistica['promedio']}")
            informe.write(f"TOTAL DE COSTO DE LAS CONSULTAS EMITIDAS    :{estadistica['total']}\n")

            informe.write("---- INFORME DE LA CONSULTA MAS CARA DEL HOSPITAL💸🏥 ----")
            informe.write(f"PACIENTE:       {consulta_cara['paciente']}")
            informe.write(f"MEDICO:         Dr.{consulta_cara['medico']}")
            informe.write(f"DIAGNOSTICO:    {consulta_cara['diagnostico']}")
            informe.write(f"COSTO:          {consulta_cara['costo']}")
            informe.write(f"FECHA:          {consulta_cara['fecha']}\n")

            informe.write("---- INFORME DEL TOP MEDICAMENTOS DEL HOSPITAL💊🏥 ----")
            for m in medicamentos:
                informe.write(f'NOMBRE: {m['nombre']:<5} | LABORATORIO: {m['laboratorio']:<5} | TOTAL DE RECETAS: {m['total']}')

            informe.write("\n---- INFORME DE CONSULTAS POR MEDICO DEL HOSPITAL👨‍⚕️🏥 ----")
            for consulta in consultas:
                informe.write(f"MEDICO: DR.{consulta['nombre']:<5} | ESPECIALIDAD: {consulta['especialidad']:<5} | TOTAL DE CONSULTAS: {consulta['total']}")

        mostrar_exito(ruta_archivo)

    except Exception:
        mostrar_error("ERROR SOLICITANDO LOS DATOS.❌")