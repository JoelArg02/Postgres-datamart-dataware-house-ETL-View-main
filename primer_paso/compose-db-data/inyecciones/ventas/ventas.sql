USE ventas;

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    direccion VARCHAR(255),
    correo VARCHAR(255),
    telefono VARCHAR(30),
    facturado boolean
);

CREATE TABLE ventas (
    id_venta INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT,
    id_cliente INT,
    fecha_venta DATE,
    total_venta DECIMAL(10, 2),
    FOREIGN key (id_cliente) REFERENCES clientes (id_cliente)
);
