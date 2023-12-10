-- Seleccionar la base de datos
USE gestion_proyectos;

-- Crear la tabla de proyectos
CREATE TABLE proyectos (
    id_proyecto INT PRIMARY KEY AUTO_INCREMENT,
    nombre_proyecto VARCHAR(255),
    fecha_inicio DATE,
    fecha_fin DATE,
    estado VARCHAR(50)
);

-- Crear la tabla de tareas
CREATE TABLE tareas (
    id_tarea INT PRIMARY KEY AUTO_INCREMENT,
    id_proyecto INT,
    descripcion TEXT,
    fecha_limite DATE,
    estado_tarea VARCHAR(50)
);

-- Crear la tabla de miembros de equipo
CREATE TABLE miembros_equipo (
    id_miembro INT PRIMARY KEY AUTO_INCREMENT,
    id_proyecto INT,
    id_empleado INT,
    rol VARCHAR(50)
);
