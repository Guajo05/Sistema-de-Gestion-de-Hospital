from app.models.consultas_model import (registrar_consulta, 
                                        historial_consulta, 
                                        estadisticas_costo, 
                                        consulta_mas_cara, 
                                        buscar_consultas,
                                        mostrar_consultas)
from app.models.medicos_model import mostrar_medicos
from app.models.pacientes_model import mostrar_pacientes
from app.views.Consultas.registrar_consulta import mostrar_mensaje_error, mostrar_mensaje_exito, solicitar_datos, ver_medicos, ver_pacientes
from app.views.Consultas.historial_consultas import mostrar_historial, solicitar_id
from app.views.Consultas.estadisticas_costo import mostrar_estadisticas_costo
from app.views.Consultas.consulta_mas_cara import mostrar_consulta_mas_cara
from app.views.Consultas.buscar_consulta import solicitar_fechas, mostrar_busqueda_consultas
from datetime import datetime
from app.utils.validar_datos import Validar_Datos_Existente

def ejecutar_registrar_consuta():
    try:
        medicos = mostrar_medicos()
        pacientes = mostrar_pacientes()

        if len(medicos) == 0:
            mostrar_mensaje_error("NO HAY MEDICOS REGISTRADOS.❎")
            return
        
        if len(pacientes) == 0:
            mostrar_mensaje_error("NO HAY PACIENTES REGISTRADOS.❎")
            return
        
        datos = solicitar_datos()

        if datos is None:
             mostrar_mensaje_error("DATOS INVALIDOS.❎")
             return

        if not Validar_Datos_Existente(datos['medico_id'], medicos, posicion_id=0):
             mostrar_mensaje_error("ESE MEDICO NO ESTA REGISTRADO.❎")
             return

        if not Validar_Datos_Existente(datos['paciente_id'], pacientes, posicion_id=0):
             mostrar_mensaje_error('ESE PACIENTE NO ESTA REGISTRADO.❎')
             return

        try:
            fecha_formateada = datetime.strptime(datos['fecha_consulta'], "%Y-%m-%d")
            if fecha_formateada.date() < datetime.now().date():
                mostrar_mensaje_error("NO PUEDES REGISTRAR CONSULTAS PARA EL PASADO.❎")
                return
            
            else:
                datos['fecha_consulta'] = fecha_formateada

            ver_medicos(medicos)
            ver_pacientes(pacientes)
            resultado = registrar_consulta(datos)

            if resultado:
                mostrar_mensaje_exito("LA CONSULTA SE REGISTRO CORRECTAMENTE.✅")
                return

        except ValueError:
             mostrar_mensaje_error("LA FECHA DE CONSULTA FUE MAL INGRESADA.❎")
             return
        
    except Exception:
            mostrar_mensaje_error("❌ERROR; REGISTRANDO LOS DATOS.")

def ejecutar_ver_historial():
    try:
        consultas = mostrar_consultas()
        if len(consultas) == 0:
            mostrar_mensaje_error("NO HAY CONSULTAS REGISTRADAS.❎")
            return
        
        id_paciente = solicitar_id()
        pacientes = mostrar_pacientes()

        if len(pacientes) == 0:
             mostrar_mensaje_error("NO HAY PACIENTES REGISTRADOS.❎")
             return
        
        if id_paciente is None:
             mostrar_mensaje_error("ERROR; DATO INVALIDO")
             return
        
        resultado = historial_consulta(id_paciente)
        mostrar_historial(resultado)
    
    except Exception:
         mostrar_mensaje_error("ERROR MOSTRANDO LOS DATOS.❎")

def ejecutar_mostrar_estadisticas_costo():
    try:    
        estadistica = estadisticas_costo()

        if estadistica is None:
          mostrar_mensaje_error("NO HAY CONSULTAS REGISTRADAS.❎")
          return
        
        mostrar_estadisticas_costo(estadistica)

    except Exception:
        mostrar_mensaje_error("❌ERROR; MOSTRANDO LAS ESTADISTICAS.")

def ejecutar_mostrar_consulta_mas_cara():
    try:
        consulta = consulta_mas_cara()

        if consulta is None:
            mostrar_mensaje_error("NO HAY CONSULTAS REGISTRADAS.❎")
            return
        
        mostrar_consulta_mas_cara(consulta)
    
    except Exception:
        mostrar_mensaje_error("❌ERROR; SOLICITANDO LOS DATOS.")

def ejecutar_mostrar_busqueda_consultas():
    try:
        consultas = mostrar_consultas()
        
        if len(consultas) == 0:
            mostrar_mensaje_error("NO HAY CONSULTAS REGISTRADAS.❎")
            return
        
        fecha_inicio, fecha_fin = solicitar_fechas()

        if fecha_inicio or fecha_fin is None:
            mostrar_mensaje_error("DATOS INVALIDOS.❎")
            return

        fecha_inicio = datetime.strptime(fecha_inicio, 'Y%-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

        consultas = buscar_consultas(fecha_inicio, fecha_fin)

        if len(consultas) == 0:
            mostrar_mensaje_error("NO HAY CONSULTAS REGISTRADAS.❎")
            return

        if consultas:
            mostrar_busqueda_consultas(consultas)

    except Exception:
        mostrar_mensaje_error("❌ERROR BUSCANDO LAS CONSULTAS.")