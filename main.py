from app.views.Menus.menu_principal import menu_principal
from app.database.db_init import Crear_Tablas

if __name__ == "__main__":
    Crear_Tablas()
    menu_principal()