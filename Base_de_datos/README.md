# como levantamos la base de datos
el prototipo se basa en la casa hogar para la administracion de los horarios y los cuidados de los residebtes y vamos explicar como se levanto la base de datos mediante tkinder cada paso y los requisitos que neswcitamos:

requisitos:
-python
-MYSQL WORKBENCH 8.0 CE
-libreria tkinder
-visual studios code
primero isismo la base de datos con myslq con las tablas y sus respectivos atributos y lo normalizamos

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
| habitacion       | PK id_habitacion,numero      
                                          |


segundo isismos las librerías que nsecitas y lo conectamos y las librerías que utilizamos son 

| Código | Qué hace |
|---|---|
| `# Registrar residente - Hogar San Ramón` | Es un comentario. Lo que empieza con `#` Python no lo ejecuta, es solo una nota. |
| `import tkinter as tk` | Trae tkinter, la librería para hacer ventanas. "as tk" es un apodo para escribir menos. |
| `from tkinter import messagebox` | Trae messagebox, que sirve para mostrar las ventanitas de mensaje (éxito o error). |
| `from datetime import datetime` | Trae lo necesario para revisar si una fecha está bien escrita. |
| `import mysql.connector` | Trae la librería que conecta Python con MySQL. |

tercero hay que hacerla vinculacion de mysql con python mediante el siquiente comando :
import mysql.connector

| Código | Qué hace |
|---|---|
| `con = mysql.connector.connect(`<br>`host="localhost", user="root",`<br>`password="...",`<br>`database="hogar_san_ramon")` | Se conecta a MySQL y guarda la conexión en la variable `con`.<br><br>`host="localhost"`: MySQL está en esta misma computadora.<br>`user="root"`: el usuario administrador de MySQL.<br>`password`: su contraseña.<br>`database`: la base de datos que usamos. |
| `cursor = con.cursor()` | Crea el cursor. Es como un mensajero: lleva las órdenes (SQL) a MySQL y trae las respuestas. |


cuarto creamos el interfaz con tkinder isismo la creacion de ventana y nos salio 5 cajas para escribir (carnet,nombres,apellidos,fecha de nacimiento y numero de habitacion) y un boton de guardar 
el prototipo revisa si los datos esta bien los guarda en la base de datos y muestra un mensaje de exito
