##  Grupo#7_Los_Olvidados
## Gestion_de_residentes_y_cuidados_y_Asignacion_de_turnos_de_cuidadores
## CASA_HOGAR_SAN_RAMON_LA_PAZ
## DESCRIPCION DEL PROYECTO/PRESENTACION DEL CASO
ver los recursos de las personas mayores de edad y gestionar el turnos de los médicos.
El Hogar San Ramón, un albergue de escasos recursos en la zona sur de La Paz que atiende a 265 adultos mayores en situación de vulnerabilidad(2017),
enfrenta grandes desafíos operativos al gestionar en papel o de memoria tanto las necesidades médicas, 
alimenticias y terapéuticas de cada residente como los turnos continuos de su personal.
Para evitar olvidos o confusiones en esta atención ininterrumpida, el proyecto propone implementar un sistema sencillo 
con base de datos enfocado en centralizar la gestión de cuidados y organizar la asignación de horarios de los cuidadores.
## PROBLEMA 
se identificado un problema en el albergue como el hogar de san Ramon la informacion de los residentes y turnos del personal se manejan de forma manual
Sin un sistema central el personal no podra encargarse del de San Ramón y las personas mayores de edad ya que causan errores en los cuidados y los horarios del personal.
## SOLUCION.
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

## como levantamos la base de datos
el prototipo se basa en la casa hogar para la administración de los horarios y los cuidados de los residentes y vamos explicar como se levanto la base de datos mediante tkinder
el prototipo sirve para administrar el albergue san Ramon: cuidados, residentes, plan de atención, personal, turnos, asistencia y usuarios del sistema y analiza la cobertura de
turnos y repartos de horas del personal y lo que necesitamos para correr el prototipo es :

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

# TUTORIAL: CONEXIÓN DE PYTHON CON MYSQL Y CREACIÓN DE INTERFAZ

## 1. Conexión de Python con MySQL

**Paso 1:** Abrir el archivo de Python del proyecto.

**Paso 2:** Importar la librería:

\`\`\`python
import mysql.connector
\`\`\`

**Paso 3:** Escribir la instrucción para establecer la conexión:

\`\`\`python
con = mysql.connector.connect(
    host="sql10.freesqldatabase.com",
    user="sql10841006",
    password="CONTRASEÑA",
    database="sql10841006"
)
\`\`\`

**Paso 4:** Colocar los datos correspondientes del servidor MySQL.

**Paso 5:** Guardar la conexión en una variable llamada `con`.

**Paso 6:** Crear el cursor mediante el siguiente código:

\`\`\`python
cursor = con.cursor()
\`\`\`

**Paso 7:** Ejecutar el programa y comprobar que la conexión con MySQL funcione correctamente.

## 2. Creación de la interfaz con Tkinter

**Paso 1:** Abrir el archivo de Python del proyecto.

**Paso 2:** Importar la librería Tkinter mediante el siguiente código:

\`\`\`python
import tkinter as tk
\`\`\`

**Paso 3:** Crear la ventana principal del programa.

**Paso 4:** Crear cinco cajas de texto para escribir los datos correspondientes (carnet, nombres, apellidos, fecha de nacimiento y número de habitación).

**Paso 5:** Agregar etiquetas para identificar cada una de las cajas de texto.

**Paso 6:** Crear un botón para guardar los datos ingresados.

**Paso 7:** Ejecutar el programa y comprobar que la interfaz gráfica se muestre correctamente.

## 3. Guardar los datos en la base de datos

**Paso 1:** Ingresar los datos correspondientes en las cinco cajas de texto de la interfaz.

**Paso 2:** Presionar el botón Guardar para registrar los datos.

**Paso 3:** Verificar que los datos ingresados estén correctamente registrados en la base de datos.

**Paso 4:** Mostrar un mensaje de éxito cuando los datos se hayan guardado correctamente.

**Paso 5:** Ejecutar el programa y comprobar que los datos se guarden en MySQL y que aparezca el mensaje de éxito.

cuarto creamos el interfaz con tkinder isismo la creacion de ventana y nos salio 5 cajas para escribir (carnet,nombres,apellidos,fecha de nacimiento y numero de habitacion) y un boton de guardar 
el prototipo revisa si los datos esta bien los guarda en la base de datos y muestra un mensaje de exito


# Hogar San Ramón – Sistema de gestión de residentes y turnos

Programa de escritorio hecho en **Python (tkinter)** que se conecta a una base de datos **MySQL**.
Sirve para administrar un albergue de adultos mayores: residentes, cuidados, planes de atención,
personal, turnos de mañana/tarde/noche, asistencia y usuarios del sistema. Además incluye una
pestaña de **Matemáticas** que analiza la cobertura de turnos y el reparto de horas del personal.

Proyecto del grupo 7 "Los Olvidados" – Ingeniería de Sistemas e Innovación Digital,
Universidad Privada Franz Tamayo, La Paz.

##  Cómo se usa

### 1.Login
Se pide usuario y contraseña. La contraseña se guarda en la base el programa encripta lo que escribe el usuario de la misma forma y
compara. Si el usuario está inactivo no puede entrar.

### Pestañas
Al entrar aparece una ventana con estas pestañas:

| Pestaña | Para qué sirve |
|---|---|
| **Residentes** | CI, nombres, apellidos, fecha de nacimiento y número de habitación. |
| **Cuidados** | Cuidados de cada residente (se busca por CI) con descripción y horario. El responsable queda registrado automáticamente: es la persona que inició sesión. |
| **Plan de atención** | Planes de atención de un residente, con fecha de inicio y fecha de fin opcional (vacía = plan vigente). |
| **Personal** | Nombres, apellidos, teléfono y cargo. |
| **Turnos** | Fecha, hora de inicio, hora de fin y persona asignada. |
| **Asistencia** | Hora de ingreso y de salida (opcional) de un turno. |
| **Usuarios** | Nombre de usuario, contraseña, estado, rol y persona del personal. |
| **Matemáticas** | Análisis de la semana (ver sección 6). |

En las siete pestañas de datos hay los mismos botones:

- **Registrar**: guarda un registro nuevo con lo escrito en el formulario.
- **Modificar**: primero se elige una fila de la tabla (sus datos pasan al formulario), se cambian y se pulsa Modificar.
- **Eliminar**: borra la fila elegida, pidiendo confirmación.
- **Mostrar**: vuelve a cargar la tabla desde la base de datos.
- **Limpiar**: vacía el formulario.

Encima de cada tabla hay un cuadro **Buscar**: filtra las filas mientras se escribe, en cualquier columna.
Las listas desplegables (cargo, residente, personal, turno, rol, estado) se actualizan cada vez que se
entra a la pestaña. En **Usuarios**, al modificar, si la contraseña se deja vacía se conserva la actual.

## 2. Validaciones y restricciones

El programa revisa los datos **antes** de enviarlos, con las mismas reglas que los `CHECK`, `UNIQUE`
y llaves foráneas del script SQL. Así el usuario recibe un mensaje claro en lugar de un error de la base.

| Dato | Regla |
|---|---|
| CI del residente | 6 a 8 números y, opcionalmente, hasta 3 caracteres de extensión (ej. `1234567A`). No se repite. |
| Nombres / apellidos | Mínimo 3 caracteres; máximo 40 / 30. |
| Fecha de nacimiento | Formato `AAAA-MM-DD` y anterior al `2000-01-01`. |
| Habitación | Número entre 1 y 300 que exista en la tabla `habitacion`. |
| Descripción del cuidado | Entre 10 y 250 caracteres. Horario en formato `HH:MM`. |
| Descripción del plan | Entre 5 y 200 caracteres. La fecha de fin no puede ser anterior a la de inicio. |
| Teléfono | 8 dígitos y empieza con 6 o 7. |
| Turno | Fecha `AAAA-MM-DD`, horas `HH:MM`, y la hora de inicio debe ser distinta de la de fin. Una persona no puede tener dos turnos que empiecen el mismo día a la misma hora. |
| Asistencia | Cada turno tiene como máximo una asistencia. La hora de salida puede quedar vacía. |
| Usuario | 4 a 15 caracteres, único; contraseña de mínimo 8 caracteres; estado `activo` o `inactivo`. Cada persona del personal tiene un solo usuario. |

Si aun así la base rechaza algo, `mostrar_error()` traduce los errores más comunes: dato duplicado (1062),
no se puede eliminar porque tiene registros relacionados (1451), registro relacionado que no existe (1452)
y dato que no cumple un CHECK (3819).

## 3.Pestaña Matemáticas

Se escribe **una fecha cualquiera** (por defecto la de hoy) y las **personas requeridas por turno**
(por defecto 1), y se pulsa **Calcular**. El programa toma la semana de lunes a domingo a la que
pertenece esa fecha, lee los turnos de la tabla `turno` y muestra:

1. **Porcentajes.** Residentes por grupo de edad (menos de 65, 65 a 79, 80 o más), calculados con
   `parte ÷ total × 100`, y el porcentaje de cobertura de la semana (turnos completos de los 21).
2. **Matrices de turnos** (3 horarios × 7 días = 21 turnos):
   - **B**: cobertura requerida (la misma cantidad en cada turno).
   - **D**: personas realmente asignadas según la tabla `turno`.
   - **A = D − B**: un `0` es turno completo y un número negativo indica cuántas personas faltan.
     Debajo se listan los turnos con falta de personal, con su fecha.
   - **T**: personal × días, con 1 si la persona trabaja ese día y 0 si descansa.
3. **Horas, promedio y derivada.**
   - **H**: horas trabajadas por persona y día.
   - **Promedio** = total de horas ÷ cantidad de personas.
   - **f(h) = (h − promedio)²** mide qué tan lejos está cada persona del promedio;
     **f′(h) = 2·(h − promedio)** y f′(h) = 0 cuando h = promedio (el mínimo, el reparto más justo).
   - Reparto más justo de turnos: por ejemplo, 21 turnos entre 6 personas son 3 personas con 4 turnos y 3 con 3.

Cómo se relaciona con el SQL:

- La tabla `turno` no guarda "mañana/tarde/noche". Se deduce de `hora_inicio`:
  mañana 06:00–13:59, tarde 14:00–21:59, noche 22:00–05:59.
- Las horas se calculan con `hora_inicio` y `hora_fin`. Si la hora de fin es menor que la de inicio,
  el turno cruza la medianoche y se suman 24 horas. Un turno nocturno cuenta en el día en que empieza.
- Las matrices T y H incluyen solo al personal que tiene al menos un turno esa semana.
- Esta pestaña **solo lee** datos, no modifica nada en la base.

## 4. Estructura del código

| Parte | Qué hace |
|---|---|
| `conectar()`, `ejecutar()`, `mostrar_error()` | Conexión a MySQL (se abre y cierra por consulta), ejecución de SQL y mensajes de error. |
| `validar_*()` | Una función por módulo que devuelve el texto del error o `None` si todo está bien. |
| `crear_pestana()`, `llenar_tabla()`, `activar_busqueda()` | Piezas de la interfaz: formulario, tabla y búsqueda. |
| `crear_modulo()` | Pestaña genérica con los 5 botones. La usan Plan de atención, Personal, Turnos, Asistencia y Usuarios; cada una solo indica sus campos y su SQL. |
| `abrir_principal()` | Ventana principal. Residentes y Cuidados están escritos aparte porque buscan por número de habitación y por CI, y arman cada pestaña. |
| `franja_de()`, `horas_de()`, `calcular_semana()`, `armar_reporte()` | Cálculos de la pestaña Matemáticas. `armar_reporte()` no usa la interfaz ni la base: recibe los datos y devuelve el texto, por lo que se puede probar sola. |
| Ventana de login (al final) | Pantalla de inicio de sesión. |

## 5. Base de datos

10 tablas: `rol`, `cargo`, `habitacion`, `personal`, `usuario`, `residente`, `plan_atencion`,
`cuidado`, `turno` y `asistencia`. `cargo`, `rol` y `habitacion` son tablas aparte (normalización);
`usuario` se relaciona 1 a 1 con `personal`, y `asistencia` 1 a 1 con `turno`.
Los detalles de cada restricción están como comentarios en `sql_corregido`.

## 6. Comandos utilizados

### En la terminal

| Comando | Para qué |
|---|---|
| `pip install mysql-connector-python` | Instala la librería que conecta Python con MySQL. |
| `python programa_completo.py` | Ejecuta el programa. |

### SQL del script `sql_corregido` (crear la base)

| Comando | Para qué |
|---|---|
| `USE` | Elige la base de datos con la que se trabaja. |
| `DROP TABLE IF EXISTS` | Borra una tabla si existe, para poder volver a ejecutar el script (se borran primero las que dependen de otras). |
| `CREATE TABLE` | Crea cada una de las 10 tablas. |
| `PRIMARY KEY AUTO_INCREMENT` | Identificador único que se numera solo (`id_residente`, `id_turno`, etc.). |
| `NOT NULL` / `NULL` | Dato obligatorio / dato que puede quedar vacío (`fecha_fin`, `hora_salida`). |
| `UNIQUE` | Evita repetidos (CI, nombre de usuario, habitación, y la combinación persona + fecha + hora de inicio del turno). |
| `FOREIGN KEY ... REFERENCES` | Une una tabla con otra (por ejemplo `residente` con `habitacion`). |
| `CONSTRAINT ... CHECK` | Reglas que debe cumplir el dato (largo mínimo, rangos, formato). |
| `CHAR_LENGTH(TRIM(...))` | Cuenta los caracteres sin contar espacios de los extremos. |
| `REGEXP` | Comprueba un formato, como el teléfono `^[67][0-9]{7}$` o el CI. |
| `IN (...)` | Limita los valores permitidos (`estado` solo `'activo'` o `'inactivo'`). |
| `INSERT INTO ... VALUES` | Inserta los datos iniciales (rol, cargo, habitaciones, personal y usuario `admin`). |
| `SHA2(texto, 256)` | Encripta la contraseña. |
| `SELECT * FROM` | Consultas de prueba al final del script. |

### SQL dentro del programa (`programa_completo.py`)

| Comando | Dónde se usa |
|---|---|
| `SELECT ... FROM ... WHERE` | Login, búsqueda de residente por CI y de habitación por número, y lectura de turnos de la semana. |
| `JOIN ... ON` | Une tablas para mostrar nombres en vez de números (cuidado + residente + personal, turno + personal, etc.). |
| `INSERT INTO` | Botón **Registrar**. |
| `UPDATE ... SET ... WHERE` | Botón **Modificar**. |
| `DELETE FROM ... WHERE` | Botón **Eliminar**. |
| `ORDER BY` | Ordena las tablas (por ejemplo, turnos por fecha). |
| `BETWEEN` | Turnos entre el lunes y el domingo de la semana elegida (pestaña Matemáticas). |
| `CONCAT(...)` | Junta nombres y apellidos en un solo texto. |
| `TIME_FORMAT(hora, '%H:%i')` | Muestra las horas como `08:30`. |
| `IFNULL(valor, '')` | Muestra vacío cuando el dato es `NULL` (fecha de fin, hora de salida). |
| `TIME_TO_SEC(hora)` | Convierte una hora a segundos para calcular la duración de los turnos. |

Los datos se envían con parámetros (`%s`), no pegados al texto de la consulta, para evitar errores de comillas y la inyección SQL.

### Python

| Comando / librería | Para qué |
|---|---|
| `mysql.connector.connect()`, `cursor()`, `execute()`, `fetchall()`, `commit()`, `close()` | Conectar, ejecutar consultas, leer resultados, guardar cambios y cerrar la conexión. |
| `hashlib.sha256(...).hexdigest()` | Encriptar la contraseña igual que `SHA2(...,256)` en SQL. |
| `re.fullmatch()` | Validar formatos (CI y teléfono) con expresiones regulares. |
| `datetime.strptime()`, `timedelta` | Validar fechas y horas, y calcular la semana (lunes a domingo). |
| `tkinter`: `Tk`, `Frame`, `Label`, `Entry`, `Button`, `Text`, `messagebox` | Ventanas, formularios, botones, cuadro de resultados y mensajes. |
| `tkinter.ttk`: `Notebook`, `Treeview`, `Combobox`, `Scrollbar` | Pestañas, tablas, listas desplegables y barra de desplazamiento. |

## 7. Limitaciones

- Los datos de personal, turnos y asistencia del documento matemático son ejemplos inventados.
- La base de datos gratuita puede tardar o fallar; si no conecta, el login muestra "No se pudo conectar".
- Los horarios de las franjas (06:00, 14:00, 22:00) están definidos en `franja_de()`; si el albergue
  usa otros, se cambian ahí.
