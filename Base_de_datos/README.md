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

# COMO ACTIVA EL CODIGO MySQL

PASO 1: ABRIR MySQL WORKBENCH

PASO 2: EN LA PANTALLA PRINCIPAL ENCONTRARAS UNA CONEXCION LLAMADA `Local instance MySQL`

PASO 3: DARLE CLICK A ESA CONEXCION

PASO 4: Introduce la contraseña del servidor si es necesario.

PASO 5: Espera a que se establezca la conexión.

PASO 6: En el panel SCHEMAS, busca sql10841006.

PASO 7: Si aparece, selecciónala.

PASO 8: Si no aparece, significa que todavía no está creada en ese servidor.

PASO 9: Dirígete al menú File.

PASO 10: Selecciona Open SQL Script.

PASO 11: Busca el archivo donde guardaste el código de Hogar San Ramón.

PASO 12: Selecciónalo y pulsa Open.

PASO 13: El contenido aparecerá en una pestaña del editor SQL.

PASO 14: Comprueba que tienes abierto el archivo correcto.

PASO 15: Localiza el botón Execute (icono del rayo)

PASO 16: Haz clic para ejecutar el script completo.

PASO 17: Espera a que finalice la ejecución.

PASO 18: Revisa el apartado Output para comprobar si hubo errores.

PASO 19: En el panel SCHEMAS, pulsa el botón de actualizar.

PASO 20: Despliega sql10841006.

PASO 21: Abre el apartado Tables.

PASO 22: Comprueba que aparecen las diez tablas del proyecto.

PASO 23: Pulsa Raw.

PASO 24: Descarga el archivo MySQL_grupo7 corregido.sql.

PASO 25: En MySQL Workbench, abre ese archivo descargado.

PASO 26: EJECUTAR EL CODIGO SQL

PASO 27: Ejecuta el contenido con el botón del rayo.

PASO 28: TODO ESO YA SE GUARDA EN UN ENLACE SIGUIENTE `https://github.com/wilfred2407/grupo-7_los_olvidados_gestion_de_residentes_y_cuidados/blob/f4a2166a03fb4481210563706cad24a825da7b73/Base_de_datos/MySQL_grupo7%20corregido.sql`
