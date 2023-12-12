
USE gestion_proyectos;

CREATE TABLE proyectos (
    id_proyecto INT PRIMARY KEY AUTO_INCREMENT,
    nombre_proyecto VARCHAR(255),
    fecha_inicio DATE,
    fecha_fin DATE,
    estado VARCHAR(50)
);

CREATE TABLE tareas (
    id_tarea INT PRIMARY KEY AUTO_INCREMENT,
    id_proyecto INT,
    descripcion TEXT,
    fecha_limite DATE,
    estado_tarea VARCHAR(50),
    FOREIGN KEY (id_proyecto) REFERENCES proyectos (id_proyecto)
);

CREATE TABLE miembros_equipo (
    id_miembro INT PRIMARY KEY AUTO_INCREMENT,
    id_proyecto INT,
    id_empleado INT,
    rol VARCHAR(50),
    FOREIGN KEY (id_proyecto) REFERENCES proyectos (id_proyecto)
);
