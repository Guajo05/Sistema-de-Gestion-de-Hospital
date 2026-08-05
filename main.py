from app.views.Menus.menu_principal import menu_principal
from app.database.db_init import init_db

if __name__ == "__main__":
    init_db()
    menu_principal()