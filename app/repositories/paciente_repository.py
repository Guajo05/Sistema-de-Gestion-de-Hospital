from app.database.conexion import conectar
from app.models.paciente import Paciente
from app.dto import (mostrar_historial_dto,
                     paciente_sin_consulta_dto)

class PacienteRepository:
    def registrar_paciente(self, paciente):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO Pacientes (nombre, edad, sangre, ciudad)
            VALUES (?, ?, ?, ?)""", (paciente.nombre, 
                                    paciente.edad, 
                                    paciente.sangre, 
                                    paciente.ciudad))
            conn.commit()
            return True

        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    def mostrar_pacientes(self):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()
            pacientes = []
            registro = cursor.execute("SELECT * FROM Pacientes").fetchall()

            for fila in registro:
                paciente = Paciente(
                    id = fila['id'],
                    nombre = fila['nombre'],
                    edad = fila['edad'],
                    sangre = fila['sangre'],
                    ciudad = fila['ciudad']
                )
                pacientes.append(paciente)

            return pacientes
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    def mostrar_historial(self, paciente_id):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()
            historial = []
            registros = cursor.execute("""SELECT
                                        md.nombre AS medico,
                                        c.diagnostico AS diagnostico,
                                        c.costo AS costo,
                                        COALESCE(mt.nombre, 'SIN MEDICAMENTOS') AS medicamento
                                   FROM Consultas AS c
                                   INNER JOIN Pacientes AS p ON c.paciente_id = p.id
                                   INNER JOIN Medicos AS md ON c.medico_id = md.id
                                   LEFT JOIN Recetas AS r ON r.consulta_id = c.id
                                   LEFT JOIN Medicamentos AS mt ON r.medicamento_id = mt.id
                                   WHERE p.id = ?
                                   ORDER BY c.fecha DESC""", (paciente_id,)).fetchall()
            for fila in registros:
                dto = mostrar_historial_dto.MostrarHistorialDto(
                    medico = fila['medico'],
                    diagnostico = fila['diagnostico'],
                    costo = fila['costo'],
                    medicamento = fila['medicamento']
                )
                historial.append(dto)
            return historial
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()
            
            if conn:
                conn.close()

    def pacientes_sin_consultas(self):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()
            pacientes = []
            registros = cursor.execute("""SELECT nombre, edad, ciudad
                                       FROM Pacientes
                                       WHERE id NOT IN (SELECT paciente_id FROM Consultas)""").fetchall()
            for fila in registros:
                paciente = paciente_sin_consulta_dto.PacienteSinConsultaDto(
                    nombre = fila['nombre'],
                    edad = fila['edad'],
                    ciudad = fila['ciudad']
                )
                pacientes.append(paciente)
            return pacientes
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()
            
            if conn:
                conn.close()