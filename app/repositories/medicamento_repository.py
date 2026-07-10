from app.database.conexion import conectar
from app.models.medicamento import Medicamento
from app.dto.top_medicamento_dto import TopMedicamentoDto

class MedicamentoRepository:
    def registrar_medicamento(self, medicamento):
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(""" INSERT INTO Medicamentos (nombre, laboratorio, precio, stock)
                           VALUES (?, ?, ?, ?)""", (medicamento.nombre,
                                                    medicamento.laboratorio,
                                                    medicamento.precio,
                                                    medicamento.stock))
            conn.commit()

        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()
    
    def mostrar_medicamentos(self):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()

            medicamentos = []
            registro = cursor.execute(""" SELECT * FROM Medicamentos """).fetchall()

            for fila in registro:
                medicamento = Medicamento(
                    id = fila['id'],
                    nombre = fila['nombre'],
                    laboratorio = fila['laboratorio'],
                    precio = fila['precio'],
                    stock = fila['stock'] 
                )
                medicamentos.append(medicamento)

            return medicamentos
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()
    
    def top_medicamentos(self):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()
            medicamentos = []
            registro = cursor.execute("""SELECT 
                                      mt.nombre AS medicamento,
                                      mt.laboratorio AS laboratorio,
                                      COUNT(r.medicamento_id) AS total
                                      FROM Medicamentos AS mt
                                      INNER JOIN Recetas AS r ON r.medicamento_id = mt.id
                                      GROUP BY mt.id, mt.nombre, mt.laboratorio
                                      ORDER BY total DESC LIMIT 5""").fetchall()
            for fila in registro:
                medicamento = TopMedicamentoDto(
                    medicamento = fila['medicamento'],
                    laboratorio = fila['laboratorio'],
                    total = fila['total']
                )
                medicamentos.append(medicamento)
            return medicamentos
        
        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()