# como levantamos la base de datos
el prototipo se basa en la casa hogar para la administracion de los horarios y los cuidados de los residebtes y vamos explicar como se levanto la base de datos mediante tkinder cada paso y los requisitos que neswcitamos:

requisitos:
-python
-MYSQL WORKBENCH 8.0 CE
-libreria tkinder
-visual studios code
primero que realizamos la base de datos con myslq con las tablas y sus respectivos atributos y lo normalizamos y podemos ver en la siguiente tabla:

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


segundo realizamos es buscar las librerías y lo conectamos y lo vinculamos con python y podemos ver en la siguiente tabla las librerías que realizamos y que hace son 

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
| `con = mysql.connector.connect(`<br>`host="localhost", user="root",`<br>`password="...",`<br>`database="hogar_san_ramon")` | Se conecta a MySQL y guarda la conexión en la variable `con`.<br><br>`host="sql10.freesqldatabase.com"`: MySQL está en esta misma computadora.<br>`user="sql10841006"`: el usuario administrador de MySQL.<br>`password`: mymKMsTsga .<br>`database`: sql10841006. |
| `cursor = con.cursor()` | Crea el cursor. Es como un mensajero: lleva las órdenes (SQL) a MySQL y trae las respuestas. |


cuarto creamos el interfaz con tkinder isismo la creacion de ventana y nos salio 5 cajas para escribir (carnet,nombres,apellidos,fecha de nacimiento y numero de habitacion) y un boton de guardar 
el prototipo revisa si los datos esta bien los guarda en la base de datos y muestra un mensaje de exito

# TUTORIAL

# PASO : 

ABRIR MySQL WORKBENCH                   

# PASO : CREAR UNA NUEVA CONSULTA SQL            

PASO : COPIAR Y PEGAR EL CODIGO SQL            

PASO : CREAR 6 TABLAS                          

PASO : EJECUTAR EL CODIGO SQL                  

PASO : COMPROBAR SI SE CREO LA BASE DE DATOS   

PASO : COMPROBAR QUE SE CREARON LAS 6 TABLAS   

PASO : COMPROBAR LA ESTRUCTURA DE LA TABLA     

PASO : INSERTAR DATOS DE PRUEBA                

PASO : CONSULTA LO DATOS GUARDADOS            

PASO : INSERTAR UN CUIDADO PARA UN RESIDENTE  

PASO : REGISTRAR UN TURNO                     

PASO : REGISTRAR LA ASISTENCIA                

PASO : VERIFICAR QUE TODO FUNCIONA            

PASO : INICIAR PROGRAMA
