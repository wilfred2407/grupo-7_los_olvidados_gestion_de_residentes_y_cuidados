#  Grupo#7_Los_Olvidados
# Gestion_de_residentes_y_cuidados_y_Asignacion_de_turnos_de_cuidadores
# CASA_HOGAR_SAN_RAMON_LA_PAZ
# DESCRIPCION DEL PROYECTO/PRESENTACION DEL CASO
ver los recursos de las personas mayores de edad y gestionar el turnos de los médicos.
El Hogar San Ramón, un albergue de escasos recursos en la zona sur de La Paz que atiende a 265 adultos mayores en situación de vulnerabilidad(2017),
enfrenta grandes desafíos operativos al gestionar en papel o de memoria tanto las necesidades médicas, 
alimenticias y terapéuticas de cada residente como los turnos continuos de su personal.
Para evitar olvidos o confusiones en esta atención ininterrumpida, el proyecto propone implementar un sistema sencillo 
con base de datos enfocado en centralizar la gestión de cuidados y organizar la asignación de horarios de los cuidadores.
# PROBLEMA 
se identificado un problema en el albergue como el hogar de san Ramon la informacion de los residentes y turnos del personal se manejan de forma manual
Sin un sistema central el personal no podra encargarse del de San Ramón y las personas mayores de edad ya que causan errores en los cuidados y los horarios del personal.
# SOLUCION.
crear sistema administrativo sencillo para el albergue de adultos mayores consiste en una base de datos y un programa con interfaz grafica.
cabe recalcar que ciertos datos y aspectos del problema son propuestos de parte del grupo 
ya que no esta verificado al 100% los datos .
asi adjuntamos la tabla de los integrantes del grupos (integrantes del equipo).

## 👥 Integrantes del equipo

| N.º | Nombre del integrante | Rol | Usuario de GitHub |
|:---:|------------------------|-----|-------------------|
| 1 | Alejandro Antonio Quispe Urizacari | Líder del proyecto, programador. | alejandro antonio |
| 2 | Dalmir Calamares Palluca | Publicista, programador. | dalbug03-eng |
| 3 | Jhilmar Jadiel Luna Gisbert | Desarrollador, programador. | jhilmarjadiellunagisbert-ux |
| 4 | Daniel Wilfredo Pomarez Huaranca | Programador. | wilfred2407 |
| 5 | Apolo Omar Vasquez Peralta | Programador. | peraltaomar409-409-cloud |

# como levantamos la base de datos
el prototipo se basa en la casa hogar para la administracion de los horarios y los cuidados de los residebtes y vamos explicar como se levanto la base de datos mediante tkinder cada paso y los requisitos que neswcitamos:

requisitos:

-python

-MYSQL WORKBENCH 8.0 CE

-libreria tkinder

-visual studios code

|PASO 1:| ABRIR MySQL WORKBENCH
una ves abrir el MYSQL WORKBENCH apretar colocar nuevo servidor y colocar los datos necesarios que son :

    host="sql10.freesqldatabase.com",
    user="sql10841006",
    password="############"
    port=3306

|PASO 2:| CREAR UNA NUEVA CONSULTA SQL
tenemos que crear la base de datos que vamos a utilizar luego tenemos que usar la base de datos con los siguientes comandos

  CREATE DATABASE sql10841006
  USE sql10841006;

|PASO 3:| COMPROBAR LA ESTRUCTURA DE LAS TABLAS
comprobamos la estructura de las tablas y la normalizamos con las 3 normas y nos dio el resultado con las 3 normas
|PASO 4:| CREAR 10 TABLAS 
para crear las 10 tablas vimos las tablas necesitarais que vamos a utilizar en la base de datos con sus respectivos atributos y a cada tabla la relacionamos con otra y con sus claves foraneas como:

id_residente int primary key auto_increment,
ci_residente varchar (11) not null unique,
nombres varchar (40) not null,
apellidos varchar (30) not null,
fecha_nac date not null,
id_habitacion int not null,
foreign key (id_habitacion) references habitacion (id_habitacion)
);

con el ejemplo que mostramos realizamos las 10 tablas 
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


|PASO 5:| EJECUCION DEL CODIGO SQL Y COMPROVACION DE LAS TABLAS       
una vez realizado la creación pasamos ala ejecución y comprobación si se ejecuto correctamente los comandos que reali8zamos con los siguiente
escogemos la tabla completa y apretamos las teclas "ctrl" y "enter" una es eso esperamos la confirmación si se ejecuto correctamente y seleccionamos con los siguiente comando 

select * from cuidado;

y utilizamos el procedimiento con cada tabla   

|PASO 6:| INSERTAR DATOS DE PRUEBA Y CONSULTA LO DATOS GUARDADOS      
insertamos algunos datos de prueba para ver si funciona y lo logramos con éxito con las restricciones que tiene Y se guardo correctamente en la base de datos
         


segundo realizamos es buscar las librerías y lo conectamos y lo vinculamos con python y podemos ver en la siguiente tabla las librerías que realizamos y que hace son 

| Código | Qué hace |
|---|---|
| `# Registrar residente - Hogar San Ramón` | Es un comentario. Lo que empieza con `#` Python no lo ejecuta, es solo una nota. |
| `import tkinter as tk` | Trae tkinter, la librería para hacer ventanas. "as tk" es un apodo para escribir menos. |
| `from tkinter import messagebox` | Trae messagebox, que sirve para mostrar las ventanitas de mensaje (éxito o error). |
| `from datetime import datetime` | Trae lo necesario para revisar si una fecha está bien escrita. |
| `import mysql.connector` | Trae la librería que conecta Python con MySQL. |

TUTORIAL: INSTALACIÓN DE LIBRERÍAS EN VISUAL STUDIO CODE

## 1. Instalación de Python

*Paso 1:* Ingresar a la página oficial https://www.python.org/downloads/

*Paso 2:* Descargar Python para Windows.

*Paso 3:* Ejecutar el instalador y marcar la opción Add Python to PATH.

*Paso 4:* Presionar Install Now y esperar a que termine la instalación.

*Paso 5:* Abrir Visual Studio Code y seleccionar Terminal → New Terminal.

*Paso 6:* Escribir el comando para comprobar la instalación:

bash
python --version


## 2. Instalación de la extensión Python

*Paso 1:* Abrir Visual Studio Code.

*Paso 2:* Ingresar a la sección de extensiones.

*Paso 3:* Buscar Python en el buscador.

*Paso 4:* Seleccionar la extensión desarrollada por Microsoft.

*Paso 5:* Presionar Install.

## 3. Librería Tkinter

*Paso 1:* Abrir Visual Studio Code.

*Paso 2:* Crear un archivo con extensión .py.

*Paso 3:* Escribir el siguiente código:

python
import tkinter as tk


*Paso 4:* Ejecutar el archivo para comprobar que la librería funciona.

*Paso 5:* Verificar que se pueda crear una ventana. Esta librería normalmente ya viene incluida con Python.

## 4. Librería Messagebox

*Paso 1:* Abrir el archivo de Python del proyecto.

*Paso 2:* Escribir el siguiente código:

python
from tkinter import import messagebox


*Paso 3:* Utilizar la instrucción para mostrar un mensaje:

python
messagebox.showinfo("Aviso", "Instalación correcta")


*Paso 4:* Ejecutar el programa y comprobar que aparezca la ventana del mensaje.

*Paso 5:* Verificar que funcione correctamente. No necesita instalación adicional porque forma parte de Tkinter.

## 5. Librería Datetime

*Paso 1:* Abrir el archivo de Python.

*Paso 2:* Escribir el siguiente código:

python
from datetime import datetime


*Paso 3:* Crear una variable para almacenar una fecha.

*Paso 4:* Utilizar datetime.strptime() para comprobar el formato de la fecha.

*Paso 5:* Ejecutar el programa y verificar que no aparezcan errores. Esta librería ya viene incluida con Python.

## 6. Instalación de MySQL Connector

*Paso 1:* Abrir Visual Studio Code.

*Paso 2:* Ingresar a Terminal → New Terminal.

*Paso 3:* Escribir el siguiente comando:

bash
python -m pip install mysql-connector-python


*Paso 4:* Presionar Enter y esperar a que termine la instalación.

*Paso 5:* Crear o abrir un archivo de Python.

*Paso 6:* Escribir el siguiente código:

python
import mysql.connector


*Paso 7:* Ejecutar el archivo para comprobar que la librería se importó correctamente.

## 7. Conexión de Python con MySQL

*Paso 1:* Abrir el archivo de Python del proyecto.

*Paso 2:* Importar la librería:

python
import mysql.connector


*Paso 3:* Escribir la instrucción para establecer la conexión:

python
con = mysql.connector.connect(
    host="DIRECCION_DEL_SERVIDOR",
    user="USUARIO",
    password="CONTRASEÑA",
    database="NOMBRE_DE_LA_BASE_DE_DATOS"
)


*Paso 4:* Colocar los datos correspondientes del servidor MySQL.

*Paso 5:* Guardar la conexión en una variable llamada con.

*Paso 6:* Crear el cursor mediante el siguiente código:

python
cursor = con.cursor()


*Paso 7:* Ejecutar el programa y comprobar que la conexión con MySQL funcione correctamente

tercero hay que hacerla vinculacion de mysql con python mediante el siquiente comando :
import mysql.connector

| Código | Qué hace |
|---|---|
| `con = mysql.connector.connect(`<br>`host="localhost", user="root",`<br>`password="...",`<br>`database="hogar_san_ramon")` | Se conecta a MySQL y guarda la conexión en la variable `con`.<br><br>`host="sql10.freesqldatabase.com"`: MySQL está en esta misma computadora.<br>`user="sql10841006"`: el usuario administrador de MySQL.<br>`password`: mymKMsTsga .<br>`database`: sql10841006. |
| `cursor = con.cursor()` | Crea el cursor. Es como un mensajero: lleva las órdenes (SQL) a MySQL y trae las respuestas. |


cuarto creamos el interfaz con tkinder isismo la creacion de ventana y nos salio 5 cajas para escribir (carnet,nombres,apellidos,fecha de nacimiento y numero de habitacion) y un boton de guardar 
el prototipo revisa si los datos esta bien los guarda en la base de datos y muestra un mensaje de exito

