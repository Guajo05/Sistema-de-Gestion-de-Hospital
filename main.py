import sys
import os
from app.Views.Vistas.vista_base import ModernCareApp
from app.database.db_init import init_db

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
init_db()

if __name__ == "__main__":
    app = ModernCareApp()
    app.mainloop()