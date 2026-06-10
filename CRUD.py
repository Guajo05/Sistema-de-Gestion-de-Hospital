import sqlite3
import time
from datetime import datetime

def Validar_Datos_Existente(id_usuario, estructura_de_datos, posicion_id = 0):
    return any(tupla[posicion_id] == id_usuario for tupla in estructura_de_datos)

def Conectar_BD():
    try:
        conn = sqlite3.connect("Sistema Hospitalario.db")
        conn.execute("PRAGMA foreign_keys = ON")
        return  conn
    
    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO CONECTAR A LA BASE DE DATOS DEBIDO A ESTO: {e}")

def Crear_Tablas():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        cursor.executescript(""" CREATE TABLE IF NOT EXISTS Pacientes(
                             id         INTEGER PRIMARY KEY AUTOINCREMENT,
                             nombre     TEXT NOT NULL,
                             edad       INTEGER NOT NULL CHECK(edad > 0),
                             sangre     TEXT NOT NULL,
                             ciudad     TEXT);
                             
                              CREATE TABLE IF NOT EXISTS Medicos(
                             id             INTEGER PRIMARY KEY AUTOINCREMENT,
                             nombre         TEXT NOT NULL,
                             especialidad   TEXT,
                             salario        REAL NOT NULL,
                             turno          TEXT NOT NULL CHECK(turno IN ("Mañana", "Tarde", "Noche")));
                             
                              CREATE TABLE IF NOT EXISTS Consultas(
                             id                       INTEGER PRIMARY KEY AUTOINCREMENT,
                             fecha_solicitud          DATE DEFAULT (DATE('now')),
                             fecha_consulta           DATE NOT NULL,
                             diagnostico              TEXT NOT NULL,
                             costo                    REAL NOT NULL,
                             paciente_id              INTEGER NOT NULL REFERENCES Pacientes(id),
                             medico_id                INTEGER NOT NULL REFERENCES Medicos(id));
                             
                             CREATE TABLE IF NOT EXISTS Medicamentos(
                             id             INTEGER PRIMARY KEY AUTOINCREMENT,
                             nombre         TEXT NOT NULL,
                             laboratorio    TEXT,
                             precio         REAL NOT NULL,
                             stock          INTEGER DEFAULT(1));
                             
                             CREATE TABLES IF NOT EXISTS Recetas(
                             id             INTEGER PRIMARY KEY AUTOINCREMENT,
                             dosis          TEXT NOT NULL,
                             dias           INTEGER NOT NULL,
                             consulta_id    INTEGER NOT NULL REFERENCES Consultas(id),
                             medicamento_id INTEGER NOT NULL REFERENCES Medicamentos(id));""")
        conn.commit()

    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO CREAR LAS TABLAS DEBIDO A ESTO: {e}")

    finally:
        cursor.close()
        conn.close()

def Registrar_Pacientes():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        tipos_de_Sangre = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        print("--- REGISTRANDO PACIENTE EN EL SISTEMA🤧---")
        nombre = input("INGRESA EL NOMBRE DEL PACIENTE: ").title()
        while True:
            edad = int(input("INGRESA LA EDAD DEL PACIENTE: "))
            if edad <= 0:
                print("LA EDAD NO PUEDE SER NEGATIVA")
                time.sleep(2)
            else: break
        sangre = input("INGRESA EL TIPO DE SANGRE DEL PACIENTE: ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']").upper()
        while True:
            if sangre not in tipos_de_Sangre:
                print('ESE TIPO DE SANGRE NO ESTA DENTRO DE LAS OPCIONES; POR LO TANTO NO EXISTE.')
                time.sleep(2)
            else: break
        ciudad = input("INGRESA LA CIUDAD DEL PACIENTE: ").title()
        cursor.execute(""" INSERT INTO Pacientes (nombre, edad, sangre, ciudad)
                       VALUES (?, ?, ?, ?)""", (nombre, edad, sangre, ciudad))
        conn.commit()
        print(f"EL PACIENTE: '{nombre}' SE REGISTRO CORRECTAMENTE EN EL SISTEMA.✅".upper())
        time.sleep(3)

    except sqlite3.Error as e:
        print(f"❌ERROR; NO SE HA PODIDO REGISTRAR PACIENTE DEBIDO A ESTO: {e}")
        time.sleep(2)

    finally:
        cursor.close()
        conn.close()

def Registrar_Medicos():
    try: 
        conn = Conectar_BD()
        cursor = conn.cursor()
        turnos = ['Mañana', 'Tarde', 'Noche']
        print("--- REGISTRANDO MEDICO EN EL SISTEMA😷---")
        nombre = input("INGRESA EL NOMBRE DEL MEDICO: ").title()
        especialidad = input("INGRESA LA ESPECIALIDAD DEL MEDICO: ").title()
        salario = float(input("INGRESA EL SALARIO DEL MEDICO: "))
        turno = input("INGRESA EL TURNO LABORAL DEL MEDICO ['Mañana', 'Tarde', 'Noche']: ").title()
        while True:
            if turno not in turnos:
                print("ESE TURNO NO ESTA DISPONIBLE")
                time.sleep(2)
            else: break
        
        cursor.execute(""" INSERT INTO Medicos (nombre, especialidad, salario, turno)
                       VALUES (?, ?, ?, ?)""", (nombre, especialidad, salario, turno))
        conn.commit()
        print(f"EL MEDICO: '{nombre}' FUE REGISTRADO CORRECTAMENTE EN EL SISTEMA.✅".upper())
        time.sleep(2)
    
    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO REGISTRAR EL MEDICO DEBIDO A ESTO: {e}")
        time.sleep(2)

    finally:
        cursor.close()
        conn.close()

def Registrar_Consultas():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        pacientes = cursor.execute(""" SELECT * FROM Pacientes""").fetchall()
        medicos = cursor.execute(""" SELECT * FROM Medicos""").fetchall()
        print("--- REGISTRANDO CONSULTA EN EL SISTEMA🩻---")

        if pacientes and medicos:
            print("--- PACIENTES REGISTRADOS EN EL SISTEMA 🤒")
            for paciente in pacientes:
                print(f"ID: {paciente[0]} | NOMBRE: {paciente[1]:<8} | EDAD: {paciente[2]:<8} | TIPO DE SANGRE: {paciente[3]:<8} | CIUDAD: {paciente[4]}")
                
                while True:
                    paciente_id = int(input("INGRESE EL ID DEL PACIENTE PARA SU CONSULTA: "))
                    if Validar_Datos_Existente(paciente_id, pacientes, posicion_id=0):
                        break
                    else:
                        print("EL ID INGRESADO NO EXISTE; INTENTE DE NUEVO.❎")

            print("--- MEDICOS REGISTRADOS EN EL SISTEMA 👨‍⚕️")
            for medico in medicos:
                print(f"ID: {medico[0]} | NOMBRE: {paciente[1]:<8} | ESPECIALIDAD: {paciente[2]:<8} | SALARIO: {paciente[3]:<8} | TURNO: {paciente[4]}")
            
                while True:
                    medico_id = int(input("INGRESE EL ID DEL MEDICO PARA SU CONSULTA: "))
                    if Validar_Datos_Existente(medico_id, medicos, posicion_id=0):
                        break
                    else:
                        print("EL ID INGRESADO NO EXISTE; INTENTE DE NUEVO.❎")

                diagnostico = input("INGRESE EL DIAGNOSTICO DE LA CONSULTA: ").title()
                costo = float(input("INGRESE EL COSTO DE LA CONSULTA: "))
                entrada = input("INGRESE LA FECHA PARA LA CONSULTA (AAAA-MM-DD): ")

                try:
                    fecha_valida = datetime.strptime(entrada, "%Y-%m-%d")

                    if fecha_valida.date() < datetime.now().date():
                        print("NO PUEDES REGISTRAR CONSULTAS PARA EL PASADO.❎")
                        continue
                    else:
                        return fecha_valida.date()

                except ValueError as e:
                    print("❌ ERORR; INGRESO DE FORMATO INCORRECTO UTILIZA EL EJEMPLO PROPORCIONADO.")

            cursor.execute(""" INSERT INTO Consultas (fecha_consulta, diagnostico, costo, paciente_id, medico_id)
                           VALUES (?, ?, ?, ?, ?)""", (fecha_valida, diagnostico, costo, paciente_id, medico_id))
            conn.commit()
            print("LA CONSULTA HA SIDO REGISTRADA EXISTOSAMENTE.✅")
            time.sleep(2)

        else:
            print("NO PUEDES REGISTRAR CONSULTAS, DEBIDO A QUE NO HAY PACIENTES NI MEDICOS REGISTRADOS.❎")
            time.sleep(2)

    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO REGISTRAR LA CONSULTA DEBIDO A ESTO: {e}")
        time.sleep(2)

    finally:
        cursor.close()
        conn.close()

def Registrar_Medicamentos():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        print("--- REGISTRANDO MEDICAMENTOS EN EL SISTEMA💊---")
        nombre = input("INGRESA EL NOMBRE DEL MEDICAMENTO: ").title()
        laboratorio = input("INGRESE EL LABORATORIO PERTENECIENTE EL MEDICAMENTO: ").title()
        precio = float(input("INGRESE EL PRECIO DEL MEDICAMENTO: "))
        cantidad = int(input("INGRESE LA CANTIDAD QUE HAY EN STOCK: "))
        cursor.execute(""" INSERT INTO Medicamentos (nombre, laboratorio, precio, stock)
                       VALUES (?, ?, ?, ?) """, (nombre, laboratorio, precio, cantidad))
        conn.commit()
        print(f"EL MEDICAMENTO: {nombre} FUE REGISTRADO EXSITOSAMENTE.✅".upper())
        time.sleep(2)
    
    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO REGISTRAR EL MEDICAMENTO DEBIDO A ESTO: {e}")
        time.sleep(2)

    finally:
        cursor.close()
        conn.close()

def Emitir_Recetas():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        consultas = cursor.execute("SELECT * FROM Consultas").fetchall()
        medicamentos = cursor.execute("SELECT * FROM Medicamentos").fetchall()
        print("--- EMITIENDO RECETA MEDICA🏥 ---")
        if consultas and medicamentos:
            print("--- CONSULTAS REGISTRADAS EN EL SISTEMA 🩻")
            for consulta in consultas:
                print(f"ID CONSULTA: {consulta[0]:<8} | ID PACIENTE: {consulta[1]:<8} | ID MEDICO: {consulta[2]:<8} | FECHA: {consulta[3]:<8} | DIAGNOSTICO: {consulta[4]:<8} | COSTO: {consulta[5]}")
            
            while True:
                consulta_id = int(input("INGRESE EL ID DE LA CONSULTA, PARA EMITIR LA RECETA: "))
                if Validar_Datos_Existente(consulta_id, consultas, posicion_id=0):
                    break
                else:
                    print("EL ID INGRESADO NO EXISTE; INTENTE DE NUEVO.❎")
                    time.sleep(2)

            print("--- MEDICAMENTOS REGISTRADOS EN EL SISTEMA💊---")
            for medicamento in medicamentos:
                print(f"ID: {medicamento[0]} | NOMBRE: {medicamento[1]:<8} | LABORATORIO: {medicamento[2]:<8} | PRECIO: {medicamento[3]} | STOCK: {medicamento[4]}")
            
            while True:
                medicamento_id = int(input("INGRESA EL ID DEL MEDICAMENTO PARA EMITIR LA RECETA: "))
                if Validar_Datos_Existente(medicamento_id, medicamentos, posicion_id=0):
                    break
                else:
                    print("EL ID INGRESADO NO EXISTE; INTENTE DE NUEVO.❎")
                    time.sleep(2)
            
            dosis = input("INGRESA LA CANTIDAD DE MEDICAMENTOS: (EJEMPLO: 2 TABLETAS AL DIA)")
            dias = int(input("INGRESA LA CANTIDAD DE DIAS QUE DEBE CONSUMIR EL MEDICAMENTO: "))
            cantidad_medicamento = cursor.execute(""" SELECT stock FROM Medicamentos WHERE id = ?""", (medicamento_id,)).fetchone()
            
            while True:
                cantidad = int(input("INGRESE LA CANTIDAD DEL MEDICAMENTO A EMITIR"))
                if cantidad > cantidad_medicamento:
                    print("ERROR; LA CANTIDAD INGRESADA ES MAYOR A LA QUE HAY EN STOCK")
                    time.sleep(2)
                else:
                    break
            cursor.execute(""" INSERT INTO Recetas (consulta_id, medicamento_id, dosis, dias) 
                           VALUES(?, ?, ?, ?)""", (consulta_id, medicamento_id, dosis, dias))
            
            cursor.execute(""" UPDATE Medicamentos 
                           WHERE stock = stock - ?""", (cantidad,))
            conn.commit()
            print("LA RECETA FUE EMITIDA CORRECTAMENTE.✅")
            time.sleep(2)

        else:
            print("NO SE PUEDE EMITIR RECETA, DEBIDO A QUE NO HAY CONSULTAS NI MEDICAMENTOS REGISTRADOS.❎")
            time.sleep(2)

    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO EMITIR LA RECETA DEBIDO A ESTO: {e}")
        time.sleep(2)

    finally:
        cursor.close()
        conn.close()

def Ver_Historial_Paciente():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        datos = {
            "Consultas": cursor.execute("SELECT * FROM Consultas").fetchall(),
            "Medicamentos": cursor.execute("SELECT * FROM Medicamentos").fetchall(),
            "Medicos": cursor.execute("SELECT * FROM Medicos").fetchall(),
            "Recetas": cursor.execute("SELECT * FROM Recetas").fetchall(),
            "Pacientes": cursor.execute("SELECT * FROM Pacientes").fetchall()
        }

        if all(datos.values()):
            pacientes = cursor.execute("SELECT * FROM Pacientes").fetchall()
            
            print("--- PACIENTES REGISTRADOS EN EL SISTEMA 🤒")
            for paciente in pacientes:
                print(f"ID: {paciente[0]} | NOMBRE: {paciente[1]:<8} | EDAD: {paciente[2]:<8} | TIPO DE SANGRE: {paciente[3]:<8} | CIUDAD: {paciente[4]}")
                
                while True:
                    paciente_id = int(input("INGRESE EL ID DEL PACIENTE PARA SU CONSULTA: "))
                    if Validar_Datos_Existente(paciente_id, pacientes, posicion_id=0):
                        break
                    else:
                        print("EL ID INGRESADO NO EXISTE; INTENTE DE NUEVO.❎")
                        
            historial = cursor.execute(""" SELECT c.id, p.nombre, md.nombre, c.diagnostico, c.costo, COALESCE(mt.nombre, 'Sin Medicamento')
                                        FROM Consultas as c
                                        INNER JOIN Pacientes as p ON c.paciente_id = p.id
                                        INNER JOIN Medicos as md ON c.medico_id = md.id
                                        LEFT JOIN Recetas as r ON r.consulta_id = c.id
                                        LEFT JOIN Medicamentos as mt ON r.medicamento_id = mt.id
                                        WHERE p.id = ?""", (paciente_id,)).fetchall()
            
            print("--- HISTORIAL DE PACIENTE🤒---")
            for consulta in historial:
                print(f"ID CONSULTA: {consulta[0]} | PACIENTE: {consulta[1]:<5} | MEDICO: {consulta[2]:<5} | DIAGNOSTICO: {consulta[3]:<5} | COSTO: {consulta[4]:<4} | MEDICAMENTO: {consulta[5]}")
            
            time.sleep(3)

        else:
            print("ERROR; NO PUEDES VER EL HISTORIAL DEBIDO A QUE HAY DATOS FALTANTES.❎")
            time.sleep(1)
            for tabla, contenido in datos.items():
                if not contenido:
                    print(f"{tabla} ESTA ES LA TABLA A LA CUAL LE FALTAN DATOS.")
            time.sleep(2)


    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO VER EL HISTORIAL DEBIDO A ESTO: {e}")
        time.sleep(2)
    
    finally:
        cursor.close()
        conn.close()

def Consultas_Por_Medico():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        datos = {
            'Consultas': cursor.execute("SELECT * FROM Consultas").fetchall(),
            'Medicos': cursor.execute("SELECT * FROM Medicos").fetchall()
        }

        if all(datos.values()):
            consultas = cursor.execute("""SELECT md.nombre, md.especialidad, COUNT(c.id) AS total
                                       FROM Medicos AS md
                                       LEFT JOIN Consultas as c ON c.medico_id = md.id
                                       GROUP BY md.id, md.nombre, md.especialidad
                                       ORDER BY total DESC""").fetchall()
            
            print("--- MEDICOS REGISTRADOS EN EL SISTEMA👨‍⚕️ ---")
            for consulta in consultas:
                print(f'NOMBRE: {consulta[0]} | ESPECIALIDAD: {consulta[1]:<5} | TOTAL DE CONSULTA: {consulta[2]}')
            time.sleep(2)
        
        else:
            print("ERROR; NO PUEDES VER EL HISTORIAL DEBIDO A QUE HAY DATOS FALTANTES.❎")
            time.sleep(1)

            for tabla, contenido in datos.items():
                if not contenido:
                    print(f"{tabla} ESTA ES LA TABLA A LA CUAL LE FALTAN DATOS.")
            time.sleep(2)
        
                
    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO VER EL HISTORIAL DEBIDO A ESTO: {e}")
        time.sleep(2)
    
    finally:
        cursor.close()
        conn.close()

def Estadisticas_Costo():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        consulta = cursor.execute(""" SELECT MIN(costo), MAX(costo), AVG(costo), SUM(costo)
                                      FROM Consultas""").fetchone()
        if consulta:
            print("--- ESTADISTICAS DEL COSTO DE LAS CONSULTAS📊 ---")
            print(f"COSTO MINIMO: {consulta[0]} | COSTO MAXIMO: {consulta[1]:<5} | PROMEDIO DE COSTO: {consulta[2]:<5} | TOTAL: {consulta[3]}")
            time.sleep(2)
        
        else:
            print("ERROR; NO PUEDES VER LAS ESTADISTICAS DEBIDO A QUE HAY DATOS FALTANTES.❎")

    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO VER LAS ESTADISTICAS DEBIDO A ESTO: {e}")
        time.sleep(2)
    
    finally:
        cursor.close()
        conn.close()

def Medicos_Ocupados():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        datos = {
            'Consultas': cursor.execute("SELECT * FROM Consultas").fetchall(),
            'Medicos': cursor.execute("SELECT * FROM Medicos").fetchall(),
        }

        if all(datos.values()):
            medicos = cursor.execute(""" SELECT md.nombre, md.especialidad, COUNT(c.id) AS Total
                                 FROM Consultas AS c
                                 INNER JOIN Medicos AS md ON c.medico_id = md.id
                                 GROUP BY md.nombre, md.especialidad
                                 HAVING COUNT(c.id) > 2
                                 ORDER BY Total DESC""").fetchall()
            
            if medicos:
                print("---🔥MEDICOS CON MAS DE 2 CONSULTAS👨‍⚕️ ---")
                for medico in medicos:
                    print(f'Dr.{medico[0]:<5} | ESPECIALIDAD: {medico[1]:<5} | {medico[2]} CONSULTAS')
                time.sleep(2)
            
        else:
            print("ERROR; NO PUEDES VER LA CONSULTA DEBIDO A QUE HAY DATOS FALTANTES.❎")
            time.sleep(1)

            for tabla, contenido in datos.items():
                if not contenido:
                    print(f"{tabla} ESTA ES LA TABLA A LA CUAL LE FALTAN DATOS.")
            time.sleep(2)
    
    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO VER LAS ESTADISTICAS DEBIDO A ESTO: {e}")
        time.sleep(2)
    
    finally:
        cursor.close()
        conn.close()

def Consulta_Mas_Cara():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        
        datos = {
            'Consultas': cursor.execute("SELECT * FROM Consultas").fetchall(),
            'Medicos': cursor.execute("SELECT * FROM Medicos").fetchall(),
            'Pacientes': cursor.execute("SELECT * FROM Pacientes").fetchall()
        }

        if all(datos.values()):
            consulta = cursor.execute(""" SELECT p.nombre, md.nombre, c.diagnostico, c.costo
                                  FROM Consultas AS c
                                  INNER JOIN Pacientes AS p ON c.paciente_id = p.id
                                  INNER JOIN Medicos AS md ON c.medico_id = md.id
                                  WHERE c.costo = (SELECT MAX(costo) FROM Consultas)""").fetchone()
        
            if consulta:
                print("--- 🏥CONSULTA MAS CARA💸 ---")
                print(f"""PACIENTE  : {consulta[0]}
                      MEDICO        : {consulta[1]}
                      DIAGNOSTICO   : {consulta[2]}
                      COSTO         : {consulta[3]}""")
                
        else:
            print("ERROR; NO PUEDES VER LA CONSULTA DEBIDO A QUE HAY DATOS FALTANTES.❎")
            time.sleep(1)

            for tabla, contenido in datos.items():
                if not contenido:
                    print(f"{tabla} ESTA ES LA TABLA A LA CUAL LE FALTAN DATOS.")
            time.sleep(2)

    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO VER LA CONSULTA DEBIDO A ESTO: {e}")
        time.sleep(2)
    
    finally:
        cursor.close()
        conn.close()

def Buscar_Consulta():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        print("--- BUSQUEDA DE CONSULTAS🏥 ---")
        inicio = input("INGRESA LA FECHA DE INICIO PARA LA BUSQUEDA (AAAA-MM-DD): ")
        fin = input("INGRESA LA FECHA DEL FIN PARA LA BUSQUEDA (AAAA-MM-DD): ")

        try:
            fecha_inicio = datetime.strptime(inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fin, '%Y-%m-%d')

            consultas = cursor.execute(""" SELECT p.nombre, md.nombre, c.costo, c.fecha
                                   FROM Consultas AS c
                                   INNER JOIN Pacientes AS p ON c.paciente_id = p.id
                                   INNER JOIN Medicos AS md ON c.medico_id = md.id
                                   WHERE c.fecha BETWEEN ? AND ?
                                   ORDER BY c.fecha""", (fecha_inicio, fecha_fin)).fetchall()
            if consultas:
                print("--- RESULTADOS DE CONSULTAS🩻 ---")
                for consulta in consultas:
                    print(f"PACIENTE: {consulta[0]:<5} | MEDICO: {consulta[1]:<5} | COSTO: {consulta[2]:<5} | FECHA: {consulta[3]}")
                time.sleep(2)
            
            else:
                print("NO HAY CONSULTAS REGISTRADAS EN ESAS FECHAS.❎")
                time.sleep(2)

        except ValueError as e:
            print(f"ERROR; INGRESO DE FECHA CON FORMATO INCORRECTO.❎")
            time.sleep(2)

    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO VER LA CONSULTA DEBIDO A ESTO: {e}")
        time.sleep(2)
    
    finally:
        cursor.close()
        conn.close()

def Top_Medicamentos():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()

        medicamentos = cursor.execute(""" SELECT mt.nombre, mt.laboratorio, COUNT(r.medicamento_id) AS Total
                                      FROM Medicamentos AS mt
                                      INNER JOIN Recetas AS r ON mt.id = r.medicamento_id
                                      GROUP BY mt.id, mt.nombre, mt.laboratorio
                                      ORDER BY Total DESC
                                      LIMIT 5""").fetchall()
        if medicamentos:
            print("--- TOP 5 DE LOS MEDICAMENTOS MAS RECETADOS📊 ---")
            for medicamento in medicamentos:
                print(f"NOMBRE: {medicamento[0]} | LABORATORIO: {medicamento[1]:<5} | TOTAL: {medicamento[2]}")
            time.sleep(2)
        
        else:
            print("ERROR; NO SE HA REGISTRADOS MEDICAMENTOS/RECETAS POR EL MOMENTO.❎")
            time.sleep(2)
    
    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO VER EL TOP DEBIDO A ESTO: {e}")
        time.sleep(2)
    
    finally:
        cursor.close()
        conn.close()

def Pacientes_Sin_Consultas():
    try:
        conn = Conectar_BD()
        cursor = conn.cursor()
        pacientes = cursor.execute(""" SELECT nombre, edad, sangre, ciudad
                                   FROM Pacientes
                                   WHERE id NOT IN (SELECT paciente_id FROM Consultas)""").fetchall()
        if pacientes:
            print("--- PACIENTES SIN CONSULTAS🤒 ---")
            for paciente in pacientes:
                print(f"NOMBRE: {paciente[0]:<5} | EDAD: {paciente[1]} | SANGRE: {paciente[2]} | CIUDAD: {paciente[3]}")
            time.sleep(2)
        
        else:
            print("ERROR; NO HAY PACIENTES REGISTRADOS.❎")
            time.sleep(2)
            
    except sqlite3.Error as e:
        print(f"❌ ERROR; NO SE HA PODIDO VER LA LISTA DE PACIENTE DEBIDO A ESTO: {e}")
        time.sleep(2)
    
    finally:
        cursor.close()
        conn.close()   