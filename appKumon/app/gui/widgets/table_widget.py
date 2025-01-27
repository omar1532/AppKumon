from PyQt5.QtWidgets import(
    QPushButton,
    QLabel,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)
from app.logic.grades_manager import GradesManager

class boletaTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        # Mapeo de nombres de los meses
        self.meses_nombres = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
            7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        
        # Etiqueta del Mes
        self.current_month = 1
        self.mes_label = QLabel(f"📅 Mes: {self.meses_nombres[self.current_month]}")
        self.layout.addWidget(self.mes_label)

        # Crear tabla de 14 columnas
        self.table = QTableWidget()
        self.table.setColumnCount(14)
        self.table.setHorizontalHeaderLabels([
            "Día", "Nivel", "Hoja", "Tiempo", 
            "1", "2", "3", "4", "5", 
            "6", "7", "8", "9", "10"
        ])
        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        # Botones de navegación (mes anterior/siguiente)
        self.prev_button = QPushButton("Anterior")
        self.next_button = QPushButton("Siguiente")
        
        self.layout.addWidget(self.prev_button)
        self.layout.addWidget(self.next_button)

        # Conectar botones a funciones de cambio de mes
        self.prev_button.clicked.connect(self.prev_month)
        self.next_button.clicked.connect(self.next_month)

        # Instancia del GradesManager
        self.grades_manager = GradesManager()
        self.setStyleSheet("""
                    
                    QTableWidget{
                        margin: 0px;
                        padding: 0px;
                        border-radius:2px;
                        background-color: #ffffff;
                    }
                    QHeaderView::section{
                        background-color: #f0f0f0;
                        color: #333;
                        font-weight: bold;
                        border: 1px solid #c5d1de;
                        padding: 5px;
                    }
                    
                    """)
        
        # Variables para identificar alumno y mes
        self.id_alumno = None

    def set_alumno(self, id_alumno):
        """Asigna el ID del alumno y carga sus boletas (del mes actual)."""
        self.id_alumno = id_alumno
        self.load_boletas()

    def load_boletas(self):
        """Carga las boletas del alumno self.id_alumno en self.current_month."""
        # Actualiza la etiqueta del mes
        self.mes_label.setText(f"📅 Mes: {self.meses_nombres[self.current_month]}")
        
        if not self.id_alumno:
            return  # Si no hay alumno asignado, no hace nada
        
        # <-- FIX: Llamar con ambos parámetros (id_alumno y mes)
        boletas = self.grades_manager.obtener_boletas_por_mes_y_alumno(self.id_alumno, self.current_month)
        
        # Ajustar cantidad de filas en la tabla
        self.table.setRowCount(len(boletas))
        
        # Cada boleta es una tupla como: 
        # (id_boleta, id_alumno, dia, mes, nivel, hoja, tiempo, cal1..cal10)
        for row_idx, boleta in enumerate(boletas):
            # Extraer datos que sí quieres mostrar (14 columnas en este orden):
            # dia (2), nivel (4), hoja (5), tiempo (6), cal1..cal10 (7..16)
            dia    = boleta[2]  # DIA
            nivel  = boleta[4]  # NIVEL
            hoja   = boleta[5]  # HOJA
            tiempo = boleta[6]  # TIEMPO
            cal1   = boleta[7]
            cal2   = boleta[8]
            cal3   = boleta[9]
            cal4   = boleta[10]
            cal5   = boleta[11]
            cal6   = boleta[12]
            cal7   = boleta[13]
            cal8   = boleta[14]
            cal9   = boleta[15]
            cal10  = boleta[16]
            
            # Arma una lista con el orden que coincide con los headers de la tabla
            celdas = [
                dia, nivel, hoja, tiempo,
                cal1, cal2, cal3, cal4, cal5,
                cal6, cal7, cal8, cal9, cal10
            ]
            
            # Rellenar la fila row_idx con esas celdas
            for col_idx, value in enumerate(celdas):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ""))

    def prev_month(self):
        """Navega al mes anterior (mínimo mes=1)."""
        self.current_month = max(1, self.current_month - 1)
        self.load_boletas()

    def next_month(self):
        """Navega al mes siguiente (máximo mes=12)."""
        self.current_month = min(12, self.current_month + 1)
        self.load_boletas()
