import sys
import os

# Asegurar que el directorio raíz esté en el sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from PyQt5.QtWidgets import QApplication, QMainWindow
from app.gui.widgets.table_widget import boletaTableWidget  # Asegúrate de que la ruta es correcta
from app.logic.grades_manager import GradesManager

# test_table.py

def main():
    app = QApplication(sys.argv)

    # ID de un alumno existente
    alumno_id = 1 

    # Instancia el widget de boletas
    w = boletaTableWidget()

    # (Opcional) Pobla boletas vacías para el alumno si quieres pruebas inmediatas
    gm = GradesManager()
    gm.poblar_boletas_vacias(alumno_id)

    # Asigna el alumno
    w.set_alumno(alumno_id)

    # Muestra la ventana
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()