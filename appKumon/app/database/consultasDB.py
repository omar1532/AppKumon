import sqlite3

db_path = "app/database/kumonDB.sqlite"
con = sqlite3.connect(db_path)
cur = con.cursor()

# Verificar si la tabla `alumnos` existe
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alumnos';")
tabla_existe = cur.fetchone()

if tabla_existe:
    print("✅ La tabla 'alumnos' existe.")
    
    # Obtener lista de alumnos
    cur.execute("SELECT * FROM alumnos;")
    alumnos = cur.fetchall()

    print("\n📂 Lista de alumnos en la base de datos:")
    for alumno in alumnos:
        print(alumno)

else:
    print("🚨 La tabla 'alumnos' NO existe.")

con.close()
