drop database if exists hogar_san_ramon;
create database hogar_san_ramon;
use hogar_san_ramon;
 -- - -la creacion de las 6 tablas- - - -- 
create table usuarios (
id_usuario int primary key auto_increment,
nombre_usuario varchar (30) not null unique,
contrasena varchar(40) not null,
rol varchar (25) not null,
estado varchar (10) not null
);
-- - - - -se puso 40 en contrasena y por que aveces suelen tener contrasenas largas 
-- - - -se puso 30 en el nombre del usuario por que aveces algunos nombres- - - - - - - - - 
-- - - -son muy largos, asi 25 en el rol por que no todos los nombres de los - - - - - - - 
-- - - - -roles son largos como por ejemplo: “enfermera” y en estado 25 por que - - - - - 
-- - - - -simplemente es activo o inactivo. - - - - - - - - -
create table personal (
id_personal int primary key auto_increment,
nombre varchar (40) not null,
apellidos varchar (30) not null,
cargo varchar (25) not null,
telefono varchar (10) not null,
id_usuario int not null,
foreign key (id_usuario) references usuarios (id_usuario)
);
-- - - de la misma aqui se puso valores de 40 al nombre por que algunos   - - - - - 
-- - - - -del personal pueden llegar a tener hasta 3 nombres , 30 en apellidos porque- - - - 
-- - - simplemente tienen 2 apellidos pero algunos son largos otros nos , 25 - - - - - - 
-- - - en cargo ya que el nombre de los cargos no es muy largo y 10 en telf - - - - - 
-- - - - - ya que  usualmente los teléfonos tienen 8 números.- - - - - 
create table residente ( 
id_residente int primary key auto_increment,
ci_residente varchar (11) not null unique,
nombre varchar (40) not null,
fecha_nac date not null,
num_habitacion int not null,
estado_salud varchar (100) not null,
plan_atencion varchar (200) not null
);
 -- - - aquí también pusimos en c.i. 11 por que usualmente algunos numeros - - - - 
 -- - - -de c.i tienen extensiones y así, en nombre 40 como decía anteriormente- - - - - -
 -- - - algunos cuentan con 3 nombres, en estado de salud 100 para poder describir- - - - -
 -- - - en qué situación se encuentra el residente y por último el plan de atención- - - - 
 -- - de la misma manera para poder organizar los cuidados y demás que el- - - - - -
 -- - - - residente llegara a necesitar.- - - - - - - - -
create table cuidados (
id_cuidado int primary key auto_increment,
descripcion varchar (250) not null,
horario time not null,
id_personal int not null,
foreign key (id_personal) references personal (id_personal),
id_residente int not null,
foreign key (id_residente) references residente (id_residente)
);
-- - - aquí podemos decir que pusimos el valor de 250 en descripción para poder- - - 
-- - - saber cual son los cuidados de los residentes relacionándolos con los- - - - - 
-- - - - -  residentes y así el personal tenga que aplicar los cuidados correspondientes.- - - - - 
create table turno (
id_turno int primary key auto_increment,
fecha_hora datetime not null,
id_personal int not null,
foreign key (id_personal) references personal (id_personal)
);

create table asistencia (
id_asistencia int primary key auto_increment,
fecha date not null,
hora_ingreso time not null,
hora_salida time null, 
id_personal int not null,
foreign key (id_personal) references personal (id_personal),
id_turno int not null,
foreign key (id_turno) references turno (id_turno)
);



