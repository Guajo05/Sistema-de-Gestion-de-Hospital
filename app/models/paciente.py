class Paciente:
    def __init__(self, nombre, edad, sangre, ciudad, estado, id = None):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.sangre = sangre
        self.ciudad = ciudad
        self.estado = estado