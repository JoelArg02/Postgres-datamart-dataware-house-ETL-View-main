
USE gestion_facturacion;

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre_cliente VARCHAR(255),
    direccion VARCHAR(255),
    correo VARCHAR(255),
    telefono VARCHAR(20)
);

CREATE TABLE facturas (
    id_factura INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    fecha_factura DATE,
    total_factura DECIMAL(10, 2),
    FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
);

CREATE TABLE detalles_factura (
    id_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_factura INT,
    id_producto INT,
    cantidad INT,
    precio_unitario DECIMAL(10, 2)
    FOREIGN KEY (id_factura) REFERENCES facturas (id_factura)    
);

