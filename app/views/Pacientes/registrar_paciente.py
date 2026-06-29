from app.utils.limpiar_consola import limpiar_pantalla

def solicitar_datos():
    limpiar_pantalla()
    try:
        print("--- REGISTRO DE PACIENTE EN EL SISTEMA🤒 ---")
        datos = {
        "nombre":   input("INGRESA EL NOMBRE DEL PACIENTE: ").title(), 
        "edad":     int(input("INGRESA LA EDAD DEL PACIENTE: ")),
        "sangre":   input("INGRESA LA SANGRE DEL PACIENTE('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'): ").upper(),
        "ciudad":   input("INGRESA LA CIUDAD DEL PACIENTE: ").title()
        }
        
        return datos
    
    except ValueError:
        return None
    

def mostrar_mensaje_error(mensaje):
    limpiar_pantalla()
    print(mensaje)
    limpiar_pantalla()

def mostrar_mensaje_exito(mensaje):
    limpiar_pantalla()
    print(mensaje)
    limpiar_pantalla()