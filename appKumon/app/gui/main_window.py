from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QMainWindow,
    QSpacerItem,
    QSizePolicy,
    QStackedWidget,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QInputDialog,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QScrollArea,
    QGroupBox,
    QFrame
)
from PyQt5.QtGui import QPixmap,QRegExpValidator
from PyQt5.QtCore import Qt,QRegExp,QDate
import sys
import sqlite3
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.gui.widgets.table_widget import boletaTableWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boletas Kumon")
        self.setGeometry(250, 100, 1080, 1220)

        # Widget Principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Configuración del STACKED
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Agregar las vistas al STACKED
        self.home_view = self.createHomeView()
        self.admin_view = self.createAdminView()
        self.add_alumno_view = self.createAddAlumnoView()
        self.Alumnos_view = self.createAlumnosView()
        self.stacked_widget.addWidget(self.home_view)
        self.stacked_widget.addWidget(self.admin_view)
        self.stacked_widget.addWidget(self.add_alumno_view)
        self.stacked_widget.addWidget(self.Alumnos_view)
        
        
        self.boleta_view = boletaTableWidget()
        self.boleta_view.setObjectName("BoletaView")
        self.stacked_widget.addWidget(self.boleta_view)
        

        # Mostrar la vista inicial (Home)
        self.stacked_widget.setCurrentWidget(self.home_view)

    def createHomeView(self):
        """Crea la vista principal (Home)."""
        home_widget = QWidget()
        home_layout = QVBoxLayout(home_widget)

        # Logo
        logo_label = QLabel()
        try:
            pixmap = QPixmap(
                r"C:\Users\omari\OneDrive\Escritorio\appKumon\app\gui\assets\kumon-institute-of-education-co-ltd-logo-vector.png"
            )
            if not pixmap.isNull():
                pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Error al cargar el logo: {e}")
            logo_label.setText("Logo no disponible")

        logo_label.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(logo_label, alignment=Qt.AlignTop)

        # Espaciador
        home_layout.addSpacerItem(QSpacerItem(10, 20, QSizePolicy.Minimum))

        # Botones
        button_layout = QHBoxLayout()
        alumnos_button = QPushButton("Alumnos")
        admin_button = QPushButton("Admin")
        alumnos_button.setFixedSize(200, 100  )
        admin_button.setFixedSize(200, 100)

        button_layout.addWidget(alumnos_button)
        button_layout.addWidget(admin_button)

        home_layout.addLayout(button_layout)
        home_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Conexión del botón "Admin" para cambiar a la vista Admin
        admin_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.admin_view))
        alumnos_button.clicked.connect(self.alumnosBoletas)

        return home_widget
    def createAlumnosView(self):
        alumnos_widget = QWidget()
        alumnos_layout = QVBoxLayout(alumnos_widget)
        
        title_label = QLabel("Boletas Alumnos")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight:bold;")
        alumnos_layout.addWidget(title_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        alumnos_layout.addWidget(scroll_area)
        
        #contenedor fichas
        self.alumnos_boleta_container = QWidget()
        self.alumnos_boleta_layout = QVBoxLayout(self.alumnos_boleta_container)
        self.alumnos_boleta_layout.setContentsMargins(10,10,10,10)
        self.alumnos_boleta_layout.setSpacing(10)
        
        scroll_area.setWidget(self.alumnos_boleta_container)
        
        #boton para volver al homeView
        back_button = QPushButton("Volver")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_view))
        alumnos_layout.addWidget(back_button)
        
        self.loadAlumnosAsFicha()
        
        return alumnos_widget
    def loadAlumnosBoletaFichas(self):
        #1) Limpiar las fichas anteriores
        for i in reversed(range(self.alumnos_boleta_layout.count())):
            item = self.alumnos_boleta_layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        #2)Obtener Alumnos de la DB
        try:
            con = sqlite3.connect(r"C:\Users\omari\OneDrive\Escritorio\appKumon\app\database\kumonDB.sqlite")
            cur = con.cursor()
            query = """
                    SELECT id_alumno, nombre, fecha_nacimiento, fecha_inscripcion,nivel, telefono
                    FROM alumnos
                    ORDER BY id_alumno ASC"""
            cur.execute(query)
            rows = cur.fetchall()
            con.close()
        except Exception as e:
            print(f"Error al cargar alumnos: {e}")
            return 
        
        #3) Crear ficha a cada alumno
        for(id_alumno,nombre,f_nac,f_insc,nivel,telefono) in rows:
            ficha = self.createAlumnoBoletaCard(id_alumno,nombre,f_nac,f_insc,nivel,telefono)
            self.alumnos_boleta_layout.addWidget(ficha)
        self.alumnos_boleta_layout.addStretch()
    def createAlumnoBoletaCard(self,id_alumno,nombre,f_nac,f_insc,nivel,telefono):
        card_widget = QFrame()
        card_widget.setFrameShape(QFrame.StyledPanel)
        card_widget.setStyleSheet("""
                                QFrame{
                                    background-color: #f9f9f9;
                                    border: 1px solid #ddd;
                                    border-radius: 8px;
                                }
                            """
                                )
        card_layout = QVBoxLayout(card_widget)
        card_layout.setContentsMargins(15,15,15,15)
        card_layout.setSpacing(15)
        
        #Datos
        label_nombre = QLabel(nombre)
        label_nombre.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        label_telefono = QLabel(telefono)
        label_nac = QLabel(f_nac)
        label_insc = QLabel(f_insc)
        label_nivel = QLabel(nivel)
        
        card_layout.addWidget(label_nombre)
        card_layout.addWidget(label_telefono)
        card_layout.addWidget(label_nac)
        card_layout.addWidget(label_insc)
        card_layout.addWidget(label_nivel)
        
        #Boton "Boleta":
        boleta_button = QPushButton("Boleta")
        boleta_button.clicked.connect(lambda _, x=id_alumno: self.showBoleta(x))
        
        card_layout.addWidget(boleta_button)
        
        return card_widget
    def showBoleta(self, id_alumno):
        
        #1) Asignar alumno a boleta_view:
        self.boleta_view.set_alumno(id_alumno)
        
        #2)Cambiar vista del stack
        self.stacked_widget.setCurrentWidget(self.boleta_view)
    def createAdminView(self):
        """vista de aministracion con alumnos para agregar, eliminar"""
        
        #widget principal
        admin_widget = QWidget()
        admin_layout = QVBoxLayout(admin_widget)
        
        #texto de incio
        title_admin = QLabel("Administracion de alumnos")
        title_admin.setAlignment(Qt.AlignCenter)
        title_admin.setStyleSheet("font-size: 24px; font-family:Arial; font-weight: bold;")
        admin_layout.addWidget(title_admin)
        
        #Scrool Area de fichas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        admin_layout.addWidget(scroll_area)
        
        #Contenedor de las tarjetas
        self.alumnos_container = QWidget()
        self.alumnos_layout = QVBoxLayout(self.alumnos_container)
        self.alumnos_layout.setContentsMargins(10,10,10,10)
        self.alumnos_layout.setSpacing(10)
        
        scroll_area.setWidget(self.alumnos_container)
        
        #Botones (AGREGAR Y VOLVER)
        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Agregar Alumno")
        add_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.add_alumno_view))
        back_button = QPushButton("Volver")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_view))
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(back_button)
        admin_layout.addLayout(buttons_layout)
        
        self.loadAlumnosAsFicha()
        
        return admin_widget
    def alumnosBoletas(self):
        
        #1) Cargar fichas
        self.loadAlumnosBoletaFichas()
        
        #2) Cambiar vista
        self.stacked_widget.setCurrentWidget(self.Alumnos_view)
        
        
    def createAddAlumnoView(self):
        # 1) Crear el widget contenedor y su layout principal
        add_widget = QWidget()
        main_layout = QVBoxLayout()  # NO pasamos `add_widget` aquí
        add_widget.setLayout(main_layout)  # Al final asignamos el layout al widget

        # 2) Crear el ScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)  # El scroll_area se agrega al layout principal

        # 3) Crear un QWidget contenedor y un layout para el formulario
        form_container = QWidget()
        form_layout = QVBoxLayout()
        form_container.setLayout(form_layout)  # Asigna layout AL CONTENEDOR
        scroll_area.setWidget(form_container)  # El contenedor se mete en el scroll

        # 4) Agregar un título
        title_label = QLabel("Agregar Nuevo Alumno")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size:32px; font-family:Arial; font-weight:bold;")
        form_layout.addWidget(title_label)

        # 5) Estilos
        input_style = """
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 5px;
            font-size: 16px;
            font-family: Arial;
            background-color: white;
        """
        date_style = """
            QDateEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 16px;
                font-family: Arial;
                background-color: white;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: right;
                width: 20px;
                border-left: 1px solid #aaa;
            }
            QDateEdit::up-button,
            QDateEdit::down-button {
                width: 16px;
                border: none;
                background-color: #f0f0f0;
            }
            QDateEdit::up-button:hover,
            QDateEdit::down-button:hover {
                background-color: #e0e0e0;
            }
        """

        # 6) Crear campos de texto
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del alumno")
        self.name_input.setFixedHeight(40)
        self.name_input.setStyleSheet(input_style)
        form_layout.addWidget(QLabel("Nombre"))
        form_layout.addWidget(self.name_input)

        self.dop_input = QDateEdit()
        self.dop_input.setCalendarPopup(True)
        self.dop_input.setDisplayFormat("yyyy-MM-dd")
        self.dop_input.setFixedSize(200, 100)
        self.dop_input.setDate(QDate.currentDate())
        self.dop_input.setStyleSheet(date_style)
        form_layout.addWidget(QLabel("Fecha de nacimiento (YYYY-MM-DD)"))
        form_layout.addWidget(self.dop_input)

        self.doi_input = QDateEdit()
        self.doi_input.setCalendarPopup(True)
        self.doi_input.setDisplayFormat("yyyy-MM-dd")
        self.doi_input.setFixedSize(200, 100)
        self.doi_input.setDate(QDate.currentDate())
        self.doi_input.setStyleSheet(date_style)
        form_layout.addWidget(QLabel("Fecha de inscripción (YYYY-MM-DD)"))
        form_layout.addWidget(self.doi_input)

        self.level_input = QComboBox()
        self.level_input.addItems([chr(i) for i in range(ord('A'), ord('P'))])
        self.level_input.setFixedHeight(40)
        self.level_input.setStyleSheet(input_style)
        form_layout.addWidget(QLabel("Nivel Inicial"))
        form_layout.addWidget(self.level_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Número de teléfono (10 dígitos)")
        self.phone_input.setValidator(QRegExpValidator(QRegExp(r"^\d{10}$")))
        self.phone_input.setFixedHeight(40)
        self.phone_input.setStyleSheet(input_style)
        form_layout.addWidget(QLabel("Número de teléfono"))
        form_layout.addWidget(self.phone_input)

        # 7) Botones
        button_layout = QHBoxLayout()
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.saveAlumno)
        back_button = QPushButton("Volver")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.admin_view))
        button_layout.addWidget(save_button)
        button_layout.addWidget(back_button)
        form_layout.addLayout(button_layout)

        # 8) Retornar el widget principal
        return add_widget

    def saveAlumno(self):
        #obtener datos del formulario
        nuevo_nombre = self.name_input.text().strip()
        fecha_de_nacimiento = self.dop_input.date().toString("yyyy-MM-dd")
        fecha_de_inscripcion = self.doi_input.date().toString("yyyy-MM-dd")
        nivel = self.level_input.currentText()
        telefono = self.phone_input.text().strip()
        
        #validaciones
        if not nuevo_nombre:
            print("Error: El nombre no puede estar vacio")
            return
        if not telefono or len(telefono) != 10:
            print("Error: El telefono no puede estar vacio y debe tener 10 digitos")
            return
        try:
            conect = sqlite3.connect(r"C:\Users\omari\OneDrive\Escritorio\appKumon\app\database\kumonDB.sqlite")
            cur = conect.cursor()
            
            query = """
            INSERT INTO alumnos (nombre,fecha_nacimiento,fecha_inscripcion,nivel,telefono)
            VALUES(?,?,?,?,?)
            """
            cur.execute(query,(nuevo_nombre,fecha_de_nacimiento,fecha_de_inscripcion,nivel,telefono))
            conect.commit()
            
            nuevo_id_alumno = cur.lastrowid
            conect.close()
            
            from app.logic.grades_manager import GradesManager
            gm = GradesManager()
            gm.poblar_boletas_vacias(nuevo_id_alumno)            
            self.name_input.clear()
            self.phone_input.clear()
            
            self.loadAlumnosAsFicha()
            
            self.loadAlumnos()
            self.stacked_widget.setCurrentWidget(self.admin_view)
            print(f'alumno {nuevo_nombre} agregado exitosamente')
        except Exception as e:
            print(f"Error {e}")
    def deleteAlumno(self,id_alumno):
        try:
            con = sqlite3.connect("C:/Users/omari/OneDrive/Escritorio/appKumon/app/database/kumonDB.sqlite")
            cur = con.cursor()
            query = "DELETE FROM alumnos WHERE id_alumno=?"
            cur.execute(query,(id_alumno,))
            con.commit()
            con.close()
            print("Alumno Eliminado con exito")
        except Exception as e:
            print(f"Error: {e}")
    def updateAlumno(self,id_alumno):
        nuevo_nombre,ok = QInputDialog.getText(self,"Actualizar_alumno","nuevo nombre")
        if ok and nuevo_nombre:
            try:
                con = sqlite3.connect("C:/Users/omari/OneDrive/Escritorio/appKumon/app/database/kumonDB.sqlite")
                cur = con.cursor()
                query = "UPDATE alumnos SET nombre = ? WHERE id_alumno = ?"
                cur.execute(query,(nuevo_nombre,id_alumno))
                con.commit()
                con.close()
                print("Alumno Actualizado con exito")
            except Exception as e:
                print(f"Error: {e}")  
        self.loadAlumnosAsFicha()
    def loadAlumnosAsFicha(self):
        #LIMPIAR FICHAS ANTERIORES
        for i in reversed(range(self.alumnos_layout.count())):
            widget_to_remove = self.alumnos_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.deleteLater()
        #CONECTAR A LA BASE DE DATOS
        try:
            con = sqlite3.connect("C:/Users/omari/OneDrive/Escritorio/appKumon/app/database/kumonDB.sqlite")
            cur = con.cursor()
            query = """SELECT id_alumno, nombre, fecha_nacimiento,fecha_inscripcion,nivel,telefono
                    FROM alumnos
                    ORDER BY id_alumno ASC"""
            cur.execute(query)
            rows = cur.fetchall()
            con.close()
        except Exception as e:
            print(f"Error: {e}")
            return 
        
        #crear fichas de alumnos
        for(id_alumno,nombre,f_nac,f_insc,nivel,telefono) in rows:
            ficha = self.createAlumnoCard(id_alumno,nombre,f_nac,f_insc,nivel,telefono)
            self.alumnos_layout.addWidget(ficha)
            
        #empujar fichas pa arriba
        self.alumnos_layout.addStretch()
    def loadAlumnos(self):
        #conectar a la base de datos
        try:
            conection = sqlite3.connect(r"C:\Users\omari\OneDrive\Escritorio\appKumon\app\database\kumonDB.sqlite")
            cur = conection.cursor()
            
            #query y consulta a la base de datos
            query = "SELECT id_alumno,nombre FROM alumnos"
            cur.execute(query)
            rows = cur.fetchall()
            
            #limpiar la tabla antes de agregar
            self.table_widget.setRowCount(0)
            
            for row_index,(alumno_id,nombre) in enumerate(rows):
                self.table_widget.insertRow(row_index)
                self.table_widget.setItem(row_index,0,QTableWidgetItem(str(alumno_id)))
                self.table_widget.setItem(row_index,1,QTableWidgetItem(nombre))
                
                #boton de actualizar
                update_button = QPushButton("Actualizar")
                update_button.clicked.connect(lambda _,id=alumno_id:self.updateAlumno(id))
                
                #agregar el boton a la celda
                button_widget = QWidget()
                layout = QHBoxLayout(button_widget)
                layout.addWidget(update_button)
                layout.setContentsMargins(0,0,0,0)
                layout.setAlignment(Qt.AlignmentCenter)
                self.table_widget.setCellWidget(row_index,2,button_widget)
            conection.close()
                
        except Exception as e:
            print(f"se ha producido del error {e}")
    def createAlumnoCard(self,id_alumno,nombre,f_nac,f_insc,nivel,telefono):
        card_widget = QFrame()
        card_widget.setFrameShape(QFrame.StyledPanel)
        card_widget.setStyleSheet("""
                            QFrame{
                                background-color:#f9f9f9;
                                border: 1px solid #ddd;
                                border-radius: 8px;
                                }""")
        card_layout = QVBoxLayout(card_widget)
        card_layout.setContentsMargins(15,15,15,15)
        card_layout.setSpacing(5)
        
        #Datos del alumno
        label_nombre = QLabel(f"{nombre}")
        label_nombre.setStyleSheet("font-size: 18px;font-weight:bold;")
        
        label_telefono = QLabel(f"{telefono}")
        label_nac = QLabel(f"{f_nac}")
        label_insc = QLabel(f"{f_insc}")
        label_nivel = QLabel(f"{nivel}")
        
        card_layout.addWidget(label_nombre)
        card_layout.addWidget(label_telefono)
        card_layout.addWidget(label_nac)
        card_layout.addWidget(label_insc)
        card_layout.addWidget(label_nivel)
        
        #BOTONES POR FICHA
        button_layout = QHBoxLayout()
        update_button  =QPushButton("Actualizar")
        update_button.clicked.connect(lambda _, x=id_alumno: self.updateAlumno(x))
        
        delete_button = QPushButton("Eliminar")
        delete_button.clicked.connect(lambda _, x=id_alumno: self.deleteAlumno(x))
        
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        
        card_layout.addLayout(button_layout)
        return card_widget



if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss = """
    QMainWindow {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #d4e7f5, stop:1 #a3d9f4);
    }
    QWidget{
        background-color: white;
        border: 1px solid #c5d1de;
        border-radius: 15px;
        padding: 15px;
        margin: 30px;
    }
    QWidget#BoletaView{
        background-color: black;
        margin: 0;
        padding: 0;
        border-radius: 0;
        border:none;
    }
    QPushButton {
        background-color: #008cba;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #007bb5;
    }
    QPushButton:pressed {
        background-color: #005f87;
    }
    QLabel {
        font-size: 16px;
        color: #555;
        margin: 20px;
        text-align: center;
    }
    """
    app.setStyleSheet(qss)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
