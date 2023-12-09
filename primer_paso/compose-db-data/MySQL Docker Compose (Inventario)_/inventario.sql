CREATE DATABASE inventario;

USE inventario;

CREATE TABLE productos (
    id_producto INT PRIMARY KEY,
    nombre_producto VARCHAR(255),
    categoria VARCHAR(255),
    stock_actual INT,
    stock_minimo INT
);

CREATE TABLE proveedores (
    id_proveedor INT PRIMARY KEY,
    nombre_proveedor VARCHAR(255),
    direccion VARCHAR(255),
    contacto VARCHAR(255)
);

CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY,
    id_producto INT,
    id_proveedor INT,
    cantidad INT,
    fecha_pedido DATE
);
