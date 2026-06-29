from app.database.conexion import conectar

def registrar_receta(datos):
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO Recetas (dosis, dias, consulta_id, medicamento_id)
                       VALUES (?, ?, ?, ?)""", (datos['dosis'],
                                                datos['dias'],
                                                datos['consulta_id'],
                                                datos['medicamento_id']))
        
        cursor.execute(""" UPDATE Medicamentos SET stock = stock - ?""", (datos['cantidad'],))
        conn.commit()
        return True
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()