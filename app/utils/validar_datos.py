# FUNCION PARA VALIDAR DATOS "EN ESTE CASO EL ID" EN UN REGISTRO
def Validar_Datos_Existente(id_usuario, estructura_de_datos, posicion_id=0, atributo_id='id'):
    for item in estructura_de_datos:
        # caso: subscriptable (tupla/lista)
        try:
            if item[posicion_id] == id_usuario:
                return True
        except Exception:
            pass

        # caso: objeto con atributo (por defecto 'id')
        if hasattr(item, atributo_id):
            if getattr(item, atributo_id) == id_usuario:
                return True

    return False