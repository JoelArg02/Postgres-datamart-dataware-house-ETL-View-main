CREATE TABLE dimension_usuarios (
    id_usuario INT PRIMARY KEY,
    nombre_usuario VARCHAR(255),
    correo VARCHAR(255)
);

CREATE TABLE dimension_hechospublicaciones (
    id_publicacion INT PRIMARY KEY,
    id_usuario INT,
    contenido TEXT,
    fecha_publicacion TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES dimension_usuarios (id_usuario)
);

CREATE TABLE dimension_comentarios (
    id_comentario SERIAL PRIMARY KEY,
    id_publicacion INT,
    texto TEXT,
    fecha_comentario TIMESTAMP,
    FOREIGN KEY (id_publicacion) REFERENCES dimension_hechospublicaciones (id_publicacion)
);

CREATE TABLE dimension_publicacion (
    id_publicacion INT,
    id_usuario INT,
    PRIMARY KEY (id_publicacion, id_usuario),
    FOREIGN KEY (id_publicacion) REFERENCES dimension_hechospublicaciones (id_publicacion),
    FOREIGN KEY (id_usuario) REFERENCES dimension_usuarios (id_usuario)
);
