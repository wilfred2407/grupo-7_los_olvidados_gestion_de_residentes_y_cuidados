-- =====================================================
-- Base de datos: Hogar San Ramón
-- Script con las 10 tablas del diagrama E-R normalizado
-- Cambio: turno es un catálogo (Mañana, Tarde, Noche) y
-- muchos del personal tienen un mismo turno (muchos a uno)
-- =====================================================

CREATE DATABASE IF NOT EXISTS hogar_san_ramon;
USE hogar_san_ramon;

SET GLOBAL tidb_enable_check_constraint = ON;

-- ----------------- BORRAR TABLAS (para poder volver a ejecutar el script) -----------------
-- se desactiva la revision de llaves foraneas solo para poder borrar en cualquier orden
-- CUIDADO: esto borra todos los datos de las tablas
SET FOREIGN_KEY_CHECKS = 0;
drop table if exists asistencia;
drop table if exists cuidado;
drop table if exists plan_atencion;
drop table if exists residente;
drop table if exists usuario;
drop table if exists personal;
drop table if exists turno;
drop table if exists habitacion;
drop table if exists cargo;
drop table if exists rol;
SET FOREIGN_KEY_CHECKS = 1;

-- primero se crean las tablas que no dependen de otras
-- y despues las que tienen llaves foraneas (foreign key)

-- ----------------- TABLA 1: rol -----------------
create table rol (
id_rol int primary key auto_increment,
nombre_rol varchar (15) not null unique,
CONSTRAINT chk_rol_nombre_largo CHECK (CHAR_LENGTH(TRIM(nombre_rol)) >= 7)
);
-- 15 en nombre_rol porque los nombres de los roles son cortos (administración, enfermeria, cuidador)

-- ----------------- TABLA 2: cargo -----------------
create table cargo (
id_cargo int primary key auto_increment,
nombre_cargo varchar (25) not null unique,
CONSTRAINT chk_cargo_nombre_largo CHECK (CHAR_LENGTH(TRIM(nombre_cargo)) >= 5)
);
-- 25 en nombre_cargo porque los cargos no tienen nombres muy largos

-- ----------------- TABLA 3: habitacion -----------------
create table habitacion (
id_habitacion int primary key auto_increment,
numero int not null unique,
CONSTRAINT chk_habitacion_numero CHECK (numero > 0 AND numero <= 300)
);
-- el numero de habitacion es unico, no puede haber dos habitaciones con el mismo número
-- y debe estar entre 1 y 300

-- ----------------- TABLA 4: turno -----------------
create table turno (
id_turno int primary key auto_increment,
nombre_turno varchar (15) not null unique,
hora_inicio time not null,
hora_fin time not null,
CONSTRAINT chk_turno_nombre_largo CHECK (CHAR_LENGTH(TRIM(nombre_turno)) >= 4),
CONSTRAINT chk_turno_horas CHECK (hora_inicio <> hora_fin)
);
-- el turno es un horario fijo (Mañana, Tarde, Noche) que comparten varias personas
-- la hora de inicio debe ser diferente de la hora de finalizacion
-- (el turno de noche termina al dia siguiente, por eso no se compara que fin sea mayor que inicio)

-- ----------------- TABLA 5: personal -----------------
create table personal (
id_personal int primary key auto_increment,
nombres varchar (40) not null,
apellidos varchar (30) not null,
telefono varchar (8) not null,
id_cargo int not null,
id_turno int not null,
foreign key (id_cargo) references cargo (id_cargo),
foreign key (id_turno) references turno (id_turno),
CONSTRAINT chk_personal_nombres_largo CHECK (CHAR_LENGTH(TRIM(nombres)) >= 3),
CONSTRAINT chk_personal_apellidos_largo CHECK (CHAR_LENGTH(TRIM(apellidos)) >= 3),
CONSTRAINT chk_personal_telefono CHECK (telefono REGEXP '^[67][0-9]{7}$')
);
-- 40 en nombres porque algunos tienen hasta 3 nombres, 30 en apellidos y 8 en telefono
-- el cargo y el turno son tablas aparte (normalizacion)
-- muchas personas del personal pueden tener el mismo turno (relacion muchos a uno)

-- ----------------- TABLA 6: usuario -----------------
create table usuario (
id_usuario int primary key auto_increment,
nombre_usuario varchar (15) not null unique,
contrasena varchar (64) not null,
estado varchar (10) not null,
id_rol int not null,
id_personal int not null unique,
foreign key (id_rol) references rol (id_rol),
foreign key (id_personal) references personal (id_personal),
CONSTRAINT chk_usuario_nombre_largo CHECK (CHAR_LENGTH(TRIM(nombre_usuario)) >= 4),
CONSTRAINT chk_usuario_contrasena_largo CHECK (CHAR_LENGTH(TRIM(contrasena)) >= 8),
CONSTRAINT chk_usuario_estado CHECK (estado IN ('activo', 'inactivo'))
);
-- 64 en contrasena porque se guarda encriptada con sha2 (la encriptacion ocupa 64 caracteres)
-- estado es "activo" o "inactivo", por eso 10
-- id_personal es unico: cada persona del personal tiene un solo usuario (relacion 1 a 1)

-- ----------------- TABLA 7: residente -----------------
create table residente (
id_residente int primary key auto_increment,
ci_residente varchar (11) not null unique,
nombres varchar (40) not null,
apellidos varchar (30) not null,
fecha_nac date not null,
id_habitacion int not null unique,
foreign key (id_habitacion) references habitacion (id_habitacion),
CONSTRAINT chk_residente_ci CHECK (ci_residente REGEXP '^[0-9]{6,8}[A-Za-z0-9]{0,3}$'),
CONSTRAINT chk_residente_nombres_largo CHECK (CHAR_LENGTH(TRIM(nombres)) >= 3),
CONSTRAINT chk_residente_apellidos_largo CHECK (CHAR_LENGTH(TRIM(apellidos)) >= 3),
CONSTRAINT chk_residente_fecha_nac CHECK (fecha_nac < '2000-01-01')
);
-- 11 en ci porque algunos carnets tienen extension, y el carnet no se puede repetir
-- la habitacion ahora es una tabla aparte (normalizacion)
-- id_habitacion es unico: dos residentes no pueden ocupar la misma habitacion

-- ----------------- TABLA 8: plan_atencion -----------------
create table plan_atencion (
id_plan int primary key auto_increment,
descripcion varchar (200) not null,
fecha_inicio date not null,
fecha_fin date null,
id_residente int not null,
foreign key (id_residente) references residente (id_residente),
CONSTRAINT chk_plan_descripcion_largo CHECK (CHAR_LENGTH(TRIM(descripcion)) >= 5),
CONSTRAINT chk_plan_fecha_inicio CHECK (fecha_inicio BETWEEN '2020-01-01' AND '2030-12-31'),
CONSTRAINT chk_plan_fechas CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio)
);
-- un residente puede tener varios planes de atencion con el tiempo (relacion 1 a muchos)
-- la fecha de inicio tiene un limite: debe estar entre 2020-01-01 y 2030-12-31
-- fecha_fin puede quedar vacia si el plan todavia sigue vigente
-- si se registra una fecha de finalizacion, no puede ser anterior a la fecha de inicio

-- ----------------- TABLA 9: cuidado -----------------
create table cuidado (
id_cuidado int primary key auto_increment,
descripcion varchar (250) not null,
horario time not null,
id_residente int not null,
id_personal int not null,
foreign key (id_residente) references residente (id_residente),
foreign key (id_personal) references personal (id_personal),
CONSTRAINT chk_cuidado_descripcion_largo CHECK (CHAR_LENGTH(TRIM(descripcion)) >= 10)
);
-- 250 en descripcion para poder escribir bien que cuidado se le aplica al residente
-- y que persona del personal es la responsable de aplicarlo

-- ----------------- TABLA 10: asistencia -----------------
create table asistencia (
id_asistencia int primary key auto_increment,
fecha date not null,
hora_ingreso time not null,
hora_salida time null,
id_personal int not null,
foreign key (id_personal) references personal (id_personal),
unique (id_personal, fecha),
CONSTRAINT chk_asistencia_horas CHECK (hora_salida IS NULL OR hora_ingreso <> hora_salida)
);
-- la asistencia ahora se guarda por persona y por fecha (antes dependia del turno)
-- una persona solo puede tener una asistencia por dia
-- hora_salida puede quedar vacia hasta que la persona termine su turno
-- si se registra la hora de salida, no puede ser igual a la hora de ingreso

-- ----------------- DATOS INICIALES -----------------
insert into rol (nombre_rol) values ('administrador/a'),('doctor/a'),('enfermero/a'),('cuidador/a'),('limpieza/a');
insert into cargo (nombre_cargo) values ('Administrador/a'),('Doctor/a'),('Enfermero/a'),('Cuidador/a'),('Limpieza/a');
insert into habitacion (numero) values (1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
insert into turno (nombre_turno, hora_inicio, hora_fin)
values ('Mañana', '06:00:00', '14:00:00'),('Tarde', '14:00:00', '22:00:00'),('Noche', '22:00:00', '06:00:00');
insert into personal (nombres, apellidos, telefono, id_cargo, id_turno)
values ('Admin', 'Sistema', '63124608', 1, 1);
insert into usuario (nombre_usuario, contrasena, estado, id_rol, id_personal)
values ('admin', sha2('admin1234', 256), 'activo', 1, 1);

-- ----------------- CONSULTAS DE PRUEBA -----------------
select * from turno;
select * from personal;
select * from asistencia;
select * from habitacion;
