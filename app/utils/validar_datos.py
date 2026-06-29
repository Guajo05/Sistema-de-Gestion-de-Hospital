# FUNCION PARA VALIDAR DATOS "EN ESTE CASO EL ID" EN UN REGISTRO
def Validar_Datos_Existente(id_usuario, estructura_de_datos, posicion_id = 0):
    return any(tupla[posicion_id] == id_usuario for tupla in estructura_de_datos)
    