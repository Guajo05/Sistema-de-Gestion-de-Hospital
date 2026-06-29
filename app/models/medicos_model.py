from app.database.conexion import conectar

def registrar_medico(datos):
    conn = None
    cursor = None
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO Medicos (nombre, especialidad, salario, turno)
                       VALUES (?, ?, ?, ?)""", (datos['nombre'], datos['especialidad'], datos['salario'], datos['turno']))
        conn.commit()
        return True
    
    except Exception as ex:
        raise ex

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def mostrar_medicos():
    conn = None
    cursor = None

    try: 
        conn = conectar()
        cursor = conn.cursor()
        medicos = cursor.execute("SELECT * FROM Medicos").fetchall()
        return medicos
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def consultas_por_medicos():
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()
        consultas_medico = cursor.execute(""" SELECT md.nombre, md.especialidad, COUNT(c.id) AS total
                                          FROM Medicos AS md
                                          LEFT JOIN Consultas AS c ON c.medico_id = md.id
                                          GROUP BY md.id, md.nombre, md.especialidad
                                          ORDER BY total DESC""").fetchall()
        return consultas_medico
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def medicos_ocupados():
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        medicos = cursor.execute(""" SELECT md.nombre, md.especialidad, COUNT(c.id) as total
                                 FROM Medicos AS md
                                 INNER JOIN Consultas AS c ON md.id = c.medico_id
                                 GROUP BY md.id, md.nombre, md.especialidad
                                 HAVING COUNT(c.id) > 2
                                 ORDER BY total DESC""").fetchall()
        return medicos
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()