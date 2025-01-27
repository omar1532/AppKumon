import sys
import os
import sqlite3

db_path = r"C:\Users\omari\OneDrive\Escritorio\appKumon\app\database\kumonDB.sqlite"



def drop_table():
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    cur.execute("DROP TABLE IF EXISTS boletas;")
    
    con.commit()
    con.close()
    
if __name__ == "__main__":
    drop_table()
