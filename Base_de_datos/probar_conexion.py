import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="#########",
    database="hogar_san_ramon")
print("Conectado a MySQL")

cur = con.cursor()
cur.execute("SHOW TABLES")
for tabla in cur.fetchall():
    print(tabla[0])

con.close()