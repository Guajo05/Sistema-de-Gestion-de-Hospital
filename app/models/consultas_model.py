from app.database.conexion import conectar

def registrar_consulta(datos):
    conn = None
    cursor = None
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(""" INSERT INTO Consultas (fecha_consulta, diagnostico, costo, paciente_id, medico_id)
                       VALUES (?, ?, ?, ?, ?)""", (datos['fecha'], 
                                                   datos['diagnostico'], 
                                                   datos['costo'], 
                                                   datos['paciente_id'], 
                                                   datos['medico_id']))
        conn.commit()

        return True

    except Exception as ex:
        raise Exception
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def mostrar_consultas():
    conn = None
    cursor = None
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        consultas = cursor.execute("""SELECT c.id AS id_consulta, 
                                             p.nombre AS nombre_paciente, 
                                             md.nombre AS nombre_medico, 
                                             c.fecha_consulta AS fecha
                                   FROM Consultas AS c
                                   INNER JOIN Pacientes AS p ON c.paciente_id = p.id
                                   INNER JOIN Medicos AS md ON c.medico_id = md.id
                                   ORDER BY c.fecha_consulta ASC""").fetchall()

        return consultas
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def historial_consulta(id_paciente):
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        historial = cursor.execute(""" SELECT 
                                        p.nombre AS paciente,
                                        md.nombre AS medico,
                                        c.diagnostico AS diagnostico,
                                        c.costo AS costo
                                        COALESCE(mt.nombre, 'SIN MEDICAMENTOS') AS medicamento
                                   FROM Consultas AS c
                                   INNER JOIN Paciente AS p ON c.paciente_id = p.id
                                   INNER JOIN Medicos AS md ON c.medico_id = md.id
                                   LEFT JOIN Recetas AS r ON r.consulta_id = c.id
                                   LEFT JOIN Medicamentos AS mt ON r.medicamento_id = mt.id
                                   WHERE p.id = ?
                                   ORDER BY c.fecha_consulta DESC""", (id_paciente,)).fetchall()
        return historial
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def estadisticas_costo():
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        estadistica = cursor.execute("""SELECT MIN(costo) AS barata,
                                 MAX(costo) AS cara,
                                 AVG(costo) AS promedio,
                                 SUM(costo) AS total
                                 FROM Consultas""").fetchone()
        
        return estadistica
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def consulta_mas_cara():
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        consulta = cursor.execute(""" SELECT p.nombre AS paciente,
                                  md.nombre AS medico,
                                  c.diagnostico AS diagnostico,
                                  c.costo AS costo,
                                  c.fecha_consulta AS fecha
                                  FROM Consultas AS c
                                  INNER JOIN Pacientes AS p ON c.paciente_id = p.id
                                  INNER JOIN Medicos AS md ON c.medico_id = md.id
                                  WHERE c.costo = (SELECT MAX(costo) FROM Consultas)""").fetchone()
        return consulta
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

def buscar_consultas(fecha_inicio, fecha_fin):
    conn = None
    cursor = None
    
    try:
        conn = conectar()
        cursor = conn.cursor()

        consultas = cursor.execute(""" SELECT 
                                   c.id AS id,
                                   p.nombre AS paciente,
                                   md.nombre AS medico,
                                   c.diagnostico AS diagnostico,
                                   c.costo AS costo,
                                   c.fecha_consulta AS fecha
                                   FROM Consultas AS c
                                   INNER JOIN Pacientes AS p ON c.paciente_id = p.id
                                   INNER JOIN Medicos AS md ON c.medico_id = md.id
                                   WHERE fecha BETWEEN ? AND ?
                                   ORDER BY fecha DESC""", (fecha_inicio, fecha_fin)).fetchall()
        return consultas
    
    except Exception as ex:
        raise ex
    
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()