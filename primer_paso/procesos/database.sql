-- Estructura para la tabla lectura_sensores
CREATE TABLE lectura_sensores (
    id_dispositivo VARCHAR(255) PRIMARY KEY,
    nombre_dispositivo VARCHAR(255),
    tipo_dispositivo VARCHAR(255),
    ubicacion_dispositivo VARCHAR(255),
    tipo_sensor VARCHAR(255),
    valor_sensor NUMERIC,
    fecha_lectura TIMESTAMP,
    tipo_alerta VARCHAR(255),
    fecha_alerta TIMESTAMP,
    estado_alerta VARCHAR(50)
);

-- Estructura para la tabla redes_data
CREATE TABLE redes_data (
    id_usuario VARCHAR(255) PRIMARY KEY,
    nombre_usuario VARCHAR(255),
    correo_usuario VARCHAR(255),
    amigos_usuario JSONB,
    id_publicacion VARCHAR(255),
    id_usuario_publicacion VARCHAR(255),
    contenido_publicacion TEXT,
    fecha_publicacion TIMESTAMP,
    likes_publicacion JSONB,
    id_comentario VARCHAR(255),
    id_publicacion_comentario VARCHAR(255),
    id_usuario_comentario VARCHAR(255),
    texto_comentario TEXT,
    fecha_comentario TIMESTAMP
);
