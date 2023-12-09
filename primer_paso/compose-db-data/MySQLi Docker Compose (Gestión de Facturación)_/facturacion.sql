-- Crear la base de datos
CREATE DATABASE gestion_facturacion;

-- Seleccionar la base de datos
USE gestion_facturacion;

-- Crear la tabla de clientes
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nombre_cliente VARCHAR(255),
    direccion VARCHAR(255),
    correo VARCHAR(255),
    telefono VARCHAR(20)
);

-- Crear la tabla de facturas
CREATE TABLE facturas (
    id_factura INT PRIMARY KEY,
    id_cliente INT,
    fecha_factura DATE,
    total_factura DECIMAL(10, 2)
);

-- Crear la tabla de detalles de factura
CREATE TABLE detalles_factura (
    id_detalle INT PRIMARY KEY,
    id_factura INT,
    id_producto INT,
    cantidad INT,
    precio_unitario DECIMAL(10, 2)
);
