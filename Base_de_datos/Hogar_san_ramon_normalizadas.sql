-- =====================================================
-- Base de datos: Hogar San Ramón
-- Script con las 10 tablas del diagrama E-R normalizado
-- =====================================================

drop database if exists hogar_san_ramon;
create database hogar_san_ramon;
use hogar_san_ramon;

-- primero se crean las tablas que no dependen de otras
-- y despues las que tienen llaves foraneas (foreign key)

-- ----------------- TABLA 1: rol -----------------
create table rol (
id_rol int primary key auto_increment,
nombre_rol varchar (25) not null unique
);
-- - - 25 en nombre_rol porque los nombres de los roles son cortos (admin, enfermeria, cuidador)

-- ----------------- TABLA 2: cargo -----------------
create table cargo (
id_cargo int primary key auto_increment,
nombre_cargo varchar (25) not null unique
);
-- - - 25 en nombre_cargo porque los cargos no tienen nombres muy largos

-- ----------------- TABLA 3: habitacion -----------------
create table habitacion (
id_habitacion int primary key auto_increment,
numero int not null unique,
CONSTRAINT chk_habitacion_numero
CHECK (numero > 0)
);
-- - - el numero de habitacion es unico, no puede haber dos habitaciones con el mismo número y debe ser mayor a cero

-- ----------------- TABLA 4: personal -----------------
create table personal (
id_personal int primary key auto_increment,
nombres varchar (40) not null,
apellidos varchar (30) not null,
telefono varchar (10) not null,
id_cargo int not null,
foreign key (id_cargo) references cargo (id_cargo)
);
-- - - 40 en nombres porque algunos tienen hasta 3 nombres, 30 en apellidos y 10 en telefono
-- - - el cargo ya no esta dentro de personal, ahora es una tabla aparte (normalizacion)

-- ----------------- TABLA 5: usuario -----------------
create table usuario (
id_usuario int primary key auto_increment,
nombre_usuario varchar (30) not null unique,
contrasena varchar (64) not null,
estado varchar (10) not null,
id_rol int not null,
id_personal int not null unique,
foreign key (id_rol) references rol (id_rol),
foreign key (id_personal) references personal (id_personal), 
CONSTRAINT chk_usuario_estado
CHECK (estado IN ('activo', 
'inactivo'))
);
-- - - 64 en contrasena porque se guarda encriptada con sha2 (la encriptacion ocupa 64 caracteres)
-- - - estado es "activo" o "inactivo", por eso 10
-- - - id_personal es unico: cada persona del personal tiene un solo usuario (relacion 1 a 1)

-- ----------------- TABLA 6: residente -----------------
create table residente (
id_residente int primary key auto_increment,
ci_residente varchar (11) not null unique,
nombres varchar (40) not null,
apellidos varchar (30) not null,
fecha_nac date not null,
id_habitacion int not null,
foreign key (id_habitacion) references habitacion (id_habitacion)
);
-- - - 11 en ci porque algunos carnets tienen extension, y el carnet no se puede repetir
-- - - la habitacion y el plan de atencion ahora son tablas aparte (normalizacion)

-- ----------------- TABLA 7: plan_atencion -----------------
create table plan_atencion (
id_plan int primary key auto_increment,
descripcion varchar (200) not null,
fecha_inicio date not null,
fecha_fin date null,
id_residente int not null,
foreign key (id_residente) references residente (id_residente),
CONSTRAINT chk_fechas_plan
CHECK (fecha_fin IS NULL OR fecha_fin 
>= fecha_inicio)
);
-- - - un residente puede tener varios planes de atencion con el tiempo (relacion 1 a muchos)
-- - - fecha_fin puede quedar vacia si el plan todavia sigue vigente
-- - - si se registra una fecha de finalizacion, no puede ser anterior a la fecha de inicio

-- ----------------- TABLA 8: cuidado -----------------
create table cuidado (
id_cuidado int primary key auto_increment,
descripcion varchar (250) not null,
horario time not null,
id_residente int not null,
id_personal int not null,
foreign key (id_residente) references residente (id_residente),
foreign key (id_personal) references personal (id_personal)
);
-- - - 250 en descripcion para poder escribir bien que cuidado se le aplica al residente
-- - - y que persona del personal es la responsable de aplicarlo

-- ----------------- TABLA 9: turno -----------------
create table turno (
id_turno int primary key auto_increment,
fecha date not null,
hora_inicio time not null,
hora_fin time not null,
id_personal int not null,
foreign key (id_personal) references personal (id_personal),
unique (id_personal, fecha, hora_inicio), 
CONSTRAINT chk_horas_turno
CHECK (hora_inicio <> hora_fin)
);
-- - - la misma persona no puede tener dos turnos que empiecen el mismo dia a la misma hora y la hora de inicio debe ser diferente de la hora de finalizacion

-- ----------------- TABLA 10: asistencia -----------------
create table asistencia (
id_asistencia int primary key auto_increment,
hora_ingreso time not null,
hora_salida time null,
id_turno int not null unique,
foreign key (id_turno) references turno (id_turno)
);
-- - - cada asistencia pertenece a un turno (relacion 1 a 1)
-- - - hora_salida puede quedar vacia hasta que la persona termine su turno

select * from cuidado;
select * from asistencia;
select * from residente;
select * from habitacion;
