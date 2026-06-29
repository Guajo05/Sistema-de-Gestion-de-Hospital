import subprocess
import os

def limpiar_pantalla():
    comando = "cls" if os.name == "nt" else "clear"
    subprocess.run(comando, shell=True)