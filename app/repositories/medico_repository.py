from app.database.conexion import conectar
from app.models.medico import Medico
from app.dto.medicos_dto import MedicosDto

class MedicoRepository:
    def registrar_medico(self, medico):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO Medicos (nombre, especialidad, salario, turno)
            VALUES (?, ?, ?, ?)""", (medico.nombre,
                                    medico.especialidad,
                                    medico.salario,
                                    medico.turno))
            conn.commit()
            return True
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()
    
    def mostrar_medicos(self):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()
            medicos = []
            registro = cursor.execute("SELECT * FROM Medicos").fetchall()

            for fila in registro:
                medico = Medico(
                    id = fila['id'],
                    nombre = fila['nombre'],
                    especialidad = fila['especialidad'],
                    salario = fila['salario'],
                    turno = fila['turno']
                )
                medicos.append(medico)
            return medicos
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    def medicos_ocupados(self):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()
            medicos = []
            
            registros = cursor.execute("""SELECT md.nombre, md.especialidad, COUNT(c.medico_id) AS total
                                     FROM Consultas AS c
                                     INNER JOIN Medicos AS md ON c.medico_id = md.id
                                     GROUP BY md.id, md.nombre, md.especialidad
                                     HAVING COUNT(c.medico_id) > 2
                                     ORDER BY total DESC""").fetchall()
            for fila in registros:
                medico = MedicosDto(
                    nombre = fila['nombre'], 
                    especialidad = fila['especialidad'], 
                    total = fila['total']
                    )
                medicos.append(medico)
            return medicos
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()
    
    def consultas_medicos(self):
        conn = None
        cursor = None

        try: 
            conn = conectar()
            cursor = conn.cursor()

            consultas = []

            registros = cursor.execute(""" SELECT md.nombre, md.especialidad, COUNT(c.medico_id) as total
                                       FROM Consultas AS c
                                       LEFT JOIN Medicos AS md ON c.medico_id = md.id
                                       GROUP BY md.id, md.nombre, md.especialidad
                                       ORDER BY total DESC""").fetchall()
            for fila in registros:
                consulta = MedicosDto(
                    nombre = fila['nombre'], 
                    especialidad = fila['especialidad'], 
                    total = fila['total']
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