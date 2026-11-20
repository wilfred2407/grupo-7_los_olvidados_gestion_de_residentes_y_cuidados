# 11,12-11-2026
Proyecto integrador en programación.
utlizando MySQL Workbench creamos la base de datos para el hogar san ramon des pues de haber creado isismos las tablas que en total eran 6
eran cuidados, personal, turno, usuario, residente y asistencia con claramente con sus respectivos atributos y las claves foranias creando asi ya la base de datos
|tablas       |atributos                                                                             |
|-------------|--------------------------------------------------------------------------------------|
| cuidado     | id_cuidado,descripcion,horario,id_personal,id_residente                              |  
| personal    | id_personal,nombre,apellidos,cargo,telefoono                                         |
| turno       | id_turno,fecha;hora,id_personal,id_asitencia                                         |
| usuario     | id_usuario,nombre,contraseña,rol,estado                                              |
| resisdente  | id_residente,ci_residente,nombre,fecha_nac,num_habitacion,estado_salud,plan_atencion |
| asistencia  | id_asistencia,fecha,hora_ingreso,hora_salida,id_personal                             |


# 13-11-2026

ya despues de crear la base de datos lo normalizamos con las 3 normas primero lo convertimos en valores atomicos sin grupos repetivos y
con clave primaria y algunas correcciones que se realizo después hicimos que cada tabla tenga una llave primaria y quitamos los atributos que
dependen de otro atributo y no directamente de la clave primaria y al implmentar las normas nos dio el resultado de 10 tablas y son :
|tablas       |atributos                                                                        |
|-------------|---------------------------------------------------------------------------------|
| cuidado          | PK id_cuidado,descripcion,horario,FK id_personal,FK id_residente           |  
| personal         | PK id_personal,nombres,apellidos,telefono,FK id_cargo                      |
| cargo            | PK id_cargo,nombre_cargo                                                   |
| turno            | PK id_turno,fecha,hora_inicio,hora_fin,id_personal                         |
| usuario          | PK id_usuario,nombre_usuario,contraseña,estado,FK id_rol,FK id_personal    |
| resisdente       | PK id_residente,ci_residente,nombres,apellidos,fecha_nac,FK id_habitacion  |
| asistencia       | PK id_asistencia,hora_ingreso,hora_salida,FK id_turno                      |
| plan de atencion | PK id_plan,descripcion,fecha_inicio,fecha_fin,FK id_residente              |
| rol              | PK id_rol,nombre_rol                                                       |
| habitacion       | PK id_habitacion,numero                                                    |


# 14-11-2026
ya este dia vinculamos el MySQL Workbench con python mediante el siguinte comando:
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
ya al realizar la vinculación realizamos los últimos arreglos del código
# 15-11-2026
ya al terminar de arreglar algunos errores se hizo las ventanas con Python Ttinker y MySQL la primera ventana con 5 cajas para escribir
(carnet, nombre, apellidos, fecha de nacimiento y numero de habitación) y un botón para guardar al colocar en la cajas los datos se guardan automáticamente y si hay algunos errores hay una ventana dice error 
# 19-11-2026
el dia de hoy colocamos limitaciones a las ventanas para que coloquen lo indicado en las ventanas y en la base de datos igual colocamos las restricciones para que no haiga ningun inconveniente en la base de datos 

