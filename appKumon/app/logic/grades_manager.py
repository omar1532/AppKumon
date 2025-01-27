import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.database import DBmanager

class GradesManager():
    def __init__(self):
        self.db = DBmanager()

    def registrar_boletas(self,id_alumno, dia, mes, nivel, hoja, tiempo, calificaciones):
        """Registra una boleta para un alumno"""
        if len(calificaciones) < 10:
            calificaciones += [None] * (10 - len(calificaciones))
        query = '''
            INSERT INTO boletas (id_alumno, dia, mes, nivel, hoja, tiempo, cal1, cal2, cal3, cal4, cal5, cal6, cal7, cal8, cal9, cal10)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        try:
            self.db.cur.execute(query, (id_alumno, dia, mes, nivel, hoja, tiempo, *calificaciones))
            self.db.con.commit()
            print(f"✅ Boleta registrada con éxito para el alumno {id_alumno}, día {dia}, mes {mes}")
        except Exception as e:
            print(f"❌ Error al registrar boleta: {e}")

    def obtener_boletas_por_mes_y_alumno(self, id_alumno,mes):
        """Obtiene todas las boletas de un mes"""
        query = "SELECT * FROM boletas WHERE id_alumno = ? AND mes = ? ORDER BY dia ASC;"
        try:
            self.db.cur.execute(query, (id_alumno,mes))
            return self.db.cur.fetchall()
        except Exception as e:
            print(f"❌ Error al extraer boletas del mes {mes}: {e}")
            return []

    def poblar_boletas_vacias(self, id_alumno):
        """Crea boletas vacías para todos los días y meses si no existen"""
        try:
            for mes in range(1, 13):  # 12 meses
                for dia in range(1, 32):  # Días del 1 al 31 (SQLite lo permite aunque algunos meses tengan menos días)
                    query = '''
                        INSERT INTO boletas (id_alumno, dia, mes, nivel, hoja, tiempo, cal1, cal2, cal3, cal4, cal5, cal6, cal7, cal8, cal9, cal10)
                        SELECT ?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL
                        WHERE NOT EXISTS (
                            SELECT 1 FROM boletas WHERE id_alumno = ? AND dia = ? AND mes = ?
                        )
                    '''
                    self.db.cur.execute(query, (id_alumno, dia, mes, id_alumno, dia, mes))

            self.db.con.commit()
            print(f"✅ Boletas vacías generadas para el alumno {id_alumno}")
        except Exception as e:
            print(f"❌ Error poblando boletas para {id_alumno}: {e}")

    def poblar_boletas_todos(self):
        """Crea boletas vacías para todos los alumnos en la base de datos"""
        try:
            query = "SELECT id_alumno FROM alumnos"
            self.db.cur.execute(query)
            alumnos = self.db.cur.fetchall()

            for alumno in alumnos:
                id_alumno = alumno[0]
                self.poblar_boletas_vacias(id_alumno)

            self.db.con.commit()
            print("✅ Boletas vacías generadas para todos los alumnos")
        except Exception as e:
            print(f"❌ Error al poblar boletas para todos los alumnos: {e}")
    def cerrar(self):
        self.db.close()
        