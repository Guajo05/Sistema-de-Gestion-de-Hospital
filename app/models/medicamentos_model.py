from app.database.conexion import conectar

def registrar_medicamento(datos):
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO Medicamentos (nombre, laboratorio, precio, stock)
                       VALUES (?, ?, ?, ?)""", (datos['nombre'], 
                                                datos['laboratorio'], 
                                                datos['precio'], 
                                                datos['stock']))
        conn.commit()
        return True
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def mostrar_medicamentos():
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        medicamentos = cursor.execute(""" SELECT * FROM Medicamentos
                                      WHERE stock > 0""").fetchall()
        
        return medicamentos
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def top_medicamentos():
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn. cursor()

        medicamentos = cursor.execute(""" SELECT 
                                      mt.nombre AS medicamento,
                                      mt.laboratorio AS laboratorio,
                                      COUNT(r.medicamento_id) AS total
                                      FROM Medicamentos AS mt
                                      INNER JOIN Recetas AS r ON r.medicamento_id = mt.id
                                      GROUP BY mt.nombre, mt.laboratorio
                                      ORDER BY total DESC
                                      LIMIT 5""").fetchall()
        return medicamentos
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()