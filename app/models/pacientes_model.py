from app.database.conexion import conectar

def registrar_paciente(datos):
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO Pacientes (nombre, edad, sangre, ciudad)
                                  VALUES (?, ?, ?, ?)""", (datos['nombre'], datos['edad'], datos['sangre'], datos['ciudad']))
        conn.commit()
        return True

    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()
        
        if conn:
            conn.close()

def mostrar_pacientes():
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        pacientes = cursor.execute("SELECT * FROM Pacientes").fetchall()

        return pacientes
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def pacientes_sin_consultas():
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        pacientes = cursor.execute("""SELECT nombre, edad, sangre, ciudad
                                   FROM Pacientes
                                   WHERE id NOT IN (SELECT paciente_id FROM Consultas)""").fetchall()
        
        return pacientes
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()