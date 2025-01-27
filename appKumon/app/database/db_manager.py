import sqlite3
import os

# Ruta de la base de datos
db_path = r"C:\Users\omari\OneDrive\Escritorio\appKumon\app\database\kumonDB.sqlite"
class DBmanager():
    def __init__(self):
        os.makedirs(os.path.dirname(db_path),exist_ok=True)
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
        self._enable_foreign_keys()
        self._create_tables()
    def _enable_foreign_keys(self):
        """ACTIVAR CLAVES FORANEAS EN SQLITE"""
        self.cur.execute("PRAGMA foreign_keys = ON;")
        estado = self.cur.execute("PRAGMA foreign_keys;").fetchone()

        print("Claves foráneas activas:", estado)
    
    def _create_tables(self): 
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id_alumno INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_nacimiento DATE NOT NULL,
            fecha_inscripcion DATE NOT NULL,
            nivel TEXT CHECK(nivel IN ('5A','4A','3A','2A','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O')) NOT NULL,
            telefono TEXT NOT NULL
        );
        ''')
        
        # Crear tabla `boletas`
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS boletas (
            id_boleta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_alumno INTEGER NOT NULL,
            dia INTEGER CHECK(dia BETWEEN 1 AND 31),
            mes INTEGER CHECK(mes BETWEEN 1 AND 12),
            nivel TEXT CHECK(nivel IN ('5A','4A','3A','2A','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O')),
            hoja INTEGER CHECK(hoja BETWEEN 1 AND 200),
            tiempo INTEGER,
            cal1 INTEGER CHECK(cal1 BETWEEN 0 AND 100),
            cal2 INTEGER CHECK(cal2 BETWEEN 0 AND 100),
            cal3 INTEGER CHECK(cal3 BETWEEN 0 AND 100),
            cal4 INTEGER CHECK(cal4 BETWEEN 0 AND 100),
            cal5 INTEGER CHECK(cal5 BETWEEN 0 AND 100),
            cal6 INTEGER CHECK(cal6 BETWEEN 0 AND 100),
            cal7 INTEGER CHECK(cal7 BETWEEN 0 AND 100),
            cal8 INTEGER CHECK(cal8 BETWEEN 0 AND 100),
            cal9 INTEGER CHECK(cal9 BETWEEN 0 AND 100),
            cal10 INTEGER CHECK(cal10 BETWEEN 0 AND 100),
            FOREIGN KEY (id_alumno) REFERENCES alumnos (id_alumno) ON DELETE CASCADE
        );
        ''')

        self.con.commit()
    def get_table_names(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        return [tabla[0] for tabla in self.cur.fetchall()]
    def get_table_info(self,table_name):
        self.cur.execute(f"PRAGMA table_info({table_name})")
        return [col[1] for col in self.cur.fetchall()]
    def get_table_schema(self, table_name):
        """Obtiene la estructura de la tabla especificada."""
        self.cur.execute(f"PRAGMA table_info({table_name})")
        schema = self.cur.fetchall()
        
        print(f"Estructura de la tabla '{table_name}':")
        for col in schema:
            print(col)  # Imprime información sobre cada columna
        return schema
    def get_nombres_alumnos(self):
        self.cur.execute("""SELECT * FROM alumnos""")
        alumns = self.cur.fetchall()
        return alumns
    def get_boletas_alumnos(self):
        self.cur.execute(
            """SELECT * FROM boletas"""
        )
        boletas = self.cur.fetchall()
        return boletas
    def close(self):
        self.con.close()

if __name__ == "__main__":
    db = DBmanager()
    db.get_table_schema("boletas")
    print(db.get_nombres_alumnos())
    db.close()