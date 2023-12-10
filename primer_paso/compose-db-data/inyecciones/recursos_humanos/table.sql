-- Crear la base de datos
-- Seleccionar la base de datos
USE recursos_humanos;

-- Crear la tabla de empleados
CREATE TABLE empleados (
    id_empleado INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    edad INT,
    puesto VARCHAR(255),
    salario DECIMAL(10, 2)
);

-- Crear la tabla de departamentos
CREATE TABLE departamentos (
    id_departamento INT PRIMARY KEY AUTO_INCREMENT,
    nombre_departamento VARCHAR(255)
);

-- Crear la tabla de historial de salarios
CREATE TABLE historial_salarios (
    id_historial INT PRIMARY KEY AUTO_INCREMENT,
    id_empleado INT,
    salario_anterior DECIMAL(10, 2),
    salario_nuevo DECIMAL(10, 2),
    fecha_modificacion DATE
);
