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
ya al realizar la vinculación realizamos los últimos arreglos de base de datos

# 15-11-2026
ya al terminar de arreglar algunos errores se hizo la ventanas con Python Ttinker y MySQL la primera ventana con 5 cajas para escribir
(carnet, nombre, apellidos, fecha de nacimiento y numero de habitación) y un botón para guardar al colocar en la cajas los datos se guardan automáticamente y si hay algunos errores hay una ventana dice error falta colocar restricciones a las cjas para que coloquen la informacion necesaria

# 19-11-2026
el dia de hoy colocamos limitaciones a las ventanas para que coloquen lo indicado en las ventanas y en la base de datos igual colocamos las restricciones para que no haiga ningún inconveniente en la base de datos la caja de nombre tiene un mínimo de 3 letras y un máximo de 15 letras y colocar fechas antes del 2000

# 20-11-2026
integramos ventanas nuevas al prototipo una ventana de login que permite entrar solo el administrador pueda ingresar con su usuario y su contraseña y Cuidados que de cada residente se busca por CI con descripción 
y horario y la ultima ventana es planes de atención de un residente que tiene fecha de inicio y fecha de fin opcional y salió falto colocar las restricciones necesarias pero aparte presento algunos fallos y lo estamos arreglando

# 22-11-2026
 al corregirlo y arreglar los fallos le colocamos restricciones y se ejecutarlo con éxito asimos las demás ventanas que son 3 y son personal que tiene las cajas de  Nombres, apellidos, teléfono y cargo la siguiente ventana es turnos y lleva las
cajas de Fecha, hora de inicio, hora de fin y persona asignada y la ultima ventana es asistencia  que tiene las cajas de Hora de ingreso y de salida (opcional) de un turno salió con éxito pero fallo en la restricciones y lo estamos viendo

# 25-11-2026
en el día de hoy después de realizar las restricciones realizamos la ultimas ventana creo que es el de matemáticas que es un análisis de la semana y designación de turnos y también se agrego la parte del aporte de las matemáticas en nuestro programa de Python. interfaz grafica final.
