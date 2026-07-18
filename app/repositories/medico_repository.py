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

    def actualizar_medico(self, datos):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(""" UPDATE Medicos
                           SET nombre = ?,
                           especialidad = ?,
                           salario = ?,
                           turno = ?
                           WHERE id = ?""", (
                               datos.nombre, 
                               datos.especialidad,
                               datos.salario,
                               datos.turno,
                               datos.id))
            if cursor.rowcount == 0:
                return None
            
            conn.commit()
            
            registro = cursor.execute("""SELECT * FROM Medicos WHERE id = ?""", (datos.id,)).fetchone()
            
            if registro is None:
                return None
            
            medico = Medico(
                id = registro['id'],
                nombre = registro['nombre'],
                especialidad = registro['especialidad'],
                salario = registro['salario'],
                turno = registro['turno'],
                estado = registro['estado']
            )
            
            return medico
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    def eliminar_medico(self, id):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(""" UPDATE Medicos
                           SET estado = False
                           WHERE id = ?""", (id,))
            
            if cursor.rowcount == 0:
                return None
            
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
            registro = cursor.execute("SELECT * FROM Medicos WHERE estado = True").fetchall()

            for fila in registro:
                medico = Medico(
                    id = fila['id'],
                    nombre = fila['nombre'],
                    especialidad = fila['especialidad'],
                    salario = fila['salario'],
                    turno = fila['turno'],
                    estado = fila['estado']
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
                                     WHERE md.estado = True  
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