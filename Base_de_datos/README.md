# como levantamos la base de datos
vamos explicar como se levandto la base de datos mediante tkinder cada paso ylos requissitos 
requisitos:
-python
-MYSQL WORKBENCH 8.0 CE
-libreria tkinder
-visual studios code
primero isismo la base de datos con myslq con las tablas y sus respectivos atributos y lo normalizamos
segundo hay que hacerla vinculacion de mysql con python mediante el siquiente comando :
import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="d13960315",
    database="hogar_san_ramon")
print("Conectado a MySQL")

cur = con.cursor()
cur.execute("SHOW TABLES")
for tabla in cur.fetchall():
    print(tabla[0])

con.close()
tercero creamos el interfaz con tkinder isismo la creacion de ventana y nos salio 5 cajas para escribir (carnet,nombres,apellidos,fecha de nacimiento y numero de habitacion) y un boton de guardar 
el prototipo revisa si los datos esta bien los guarda en la base de datos y muestra un mensaje de exito
