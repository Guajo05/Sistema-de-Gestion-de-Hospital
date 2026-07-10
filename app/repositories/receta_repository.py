from app.database.conexion import conectar

class RecetaRepository:
    def registrar_receta(self, receta):
        conn = None
        cursor = None

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(""" INSERT INTO Recetas (dosis, dias, consulta_id, medicamento_id)
                           VALUES (?, ?, ?, ?)""", (receta.dosis,
                                                    receta.dias,
                                                    receta.consulta,
                                                    receta.medicamento))
            
            cursor.execute(""" UPDATE Medicamentos 
                           SET stock = stock - ?
                           WHERE id = ? """, (receta.cantidad, receta.medicamento))
            conn.commit()

        except Exception as ex:
            raise ex
        
        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()