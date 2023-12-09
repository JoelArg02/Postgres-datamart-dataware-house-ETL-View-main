CREATE DATABASE ventas;

USE ventas;

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(255),
    direccion VARCHAR(255),
    correo VARCHAR(255),
    telefono VARCHAR(20)
);

CREATE TABLE productos (
    id_producto INT PRIMARY KEY,
    nombre_producto VARCHAR(255),
    precio DECIMAL(10, 2),
    stock INT
);

CREATE TABLE ventas (
    id_venta INT PRIMARY KEY,
    id_cliente INT,
    fecha_venta DATE,
    total_venta DECIMAL(10, 2)
);
