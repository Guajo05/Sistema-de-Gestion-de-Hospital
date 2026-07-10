from app.database.conexion import conectar
from app.models.consulta import Consulta
from app.dto import (consulta_mas_cara_dto,
                     estadistica_costo_dto,
                     buscar_consulta_dto,
                     mostrar_historial_dto,
                     mostrar_consulta_dto)

class ConsultaRepository:
    def registrar_consulta(self, consulta):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(""" INSERT INTO Consultas (fecha, diagnostico, costo, paciente_id, medico_id)
                           VALUES (?, ?, ?, ?, ?)""", (consulta.fecha, consulta.diagnostico, consulta.costo, consulta.paciente, consulta.medico))
            conn.commit()

        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()
            
            if conn:
                conn.close()

    def mostrar_consultas(self):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()

            consultas = []
            registro = cursor.execute(""" SELECT id, costo, fecha FROM Consultas""").fetchall()

            for fila in registro:
                consulta = mostrar_consulta_dto.MostrarConsultaDto(
                    id = fila['id'],
                    costo = fila['costo'],
                    fecha = fila['fecha']
                )
                consultas.append(consulta)

            return consultas
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()
    
    def consulta_mas_cara(self):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()
            registro = cursor.execute(""" SELECT
                                      p.nombre AS paciente,
                                      md.nombre AS medico,
                                      c.diagnostico AS diagnostico,
                                      c.costo AS costo,
                                      c.fecha AS fecha
                                      FROM Consultas AS c
                                      INNER JOIN Pacientes AS p ON c.paciente_id = p.id
                                      INNER JOIN Medicos AS md ON c.medico_id = md.id
                                      WHERE c.costo = (SELECT MAX(costo) FROM Consultas)""").fetchone()
            if registro is None:
                return []
            
            consulta = consulta_mas_cara_dto.ConsultaMasCaraDto(
                    paciente = registro['paciente'],
                    medico = registro['medico'],
                    diagnostico = registro['diagnostico'],
                    costo = registro['costo'],
                    fecha = registro['fecha']            
                    )
            return consulta

        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()
    
    def estadisticas_costo(self):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()

            estadisticas = cursor.execute("""SELECT MIN(costo) AS barata,
                                 MAX(costo) AS cara,
                                 AVG(costo) AS promedio,
                                 SUM(costo) AS total
                                 FROM Consultas""").fetchone()
            
            estadisticas = estadistica_costo_dto.EstadisticaCostoDto(
                barata = estadisticas['barata'],
                cara= estadisticas['cara'],
                promedio= estadisticas['promedio'],
                total= estadisticas['total']
            )

            return estadisticas
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    def buscar_consulta(self, fechas):
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            consultas = []
            registro = cursor.execute("""SELECT
                                      c.id AS id
                                      p.nombre AS paciente,
                                      md.nombre AS medico,
                                      c.costo AS costo
                                      FROM Consultas AS c
                                      INNER JOIN Pacientes AS p ON c.paciente_id = p.id
                                      INNER JOIN Medicos AS md ON c.medico_id = md.id
                                      WHERE c.fecha_consulta BETWEEN ? AND ?
                                      ORDER BY c.fecha_consulta DESC""", (fechas.inicio, fechas.final)).fetchall()
            for fila in registro:
                consulta = buscar_consulta_dto.BuscarConsultaDto(
                    id= fila['id'],
                    paciente= fila['paciente'],
                    medico= fila['medico'],
                    costo=fila['costo']
                )
                consultas.append(consulta)
            return consultas
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    def mostrar_historial(self, id):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()

            historial = []
            registro = cursor.execute(""" SELECT 
                                      md.nombre AS medico, 
                                      c.costo AS costo, 
                                      c.diagnostico AS diagnostico
                                      COALESCE(mt.nombre, 'SIN MEDICAMENTOS') AS medicamento
                                      FROM Consultas AS c 
                                      INNER JOIN Pacientes AS p ON c.paciente_id = p.id
                                      INNER JOIN Medicos AS md ON c.medico_id = md.id
                                      LEFT JOIN Recetas AS r ON r.consulta_id = c.id
                                      LEFT JOIN Medicamentos AS mt ON r.medicamento_id = mt.id
                                      WHERE p.id = ?
                                      ORDER BY pc.fecha_consulta DESC""", (id)).fetchall()
            
            for fila in registro:
                historia = mostrar_historial_dto.MostrarHistorialDto(
                    medico= fila['medico'],
                    costo= fila['costo'],
                    diagnostico= fila['diagnostico'],
                    medicamento=fila['medicamento']
                )
                historial.append(historia)

            return historial
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()