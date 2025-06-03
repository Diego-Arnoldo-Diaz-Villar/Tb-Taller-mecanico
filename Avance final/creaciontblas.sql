DROP DATABASE IF EXISTS TallerMecanico;
CREATE DATABASE TallerMecanico
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE TallerMecanico;

-- Tabla de Usuarios
CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ap_paterno VARCHAR(100) NOT NULL,
    ap_materno VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    contraseña VARCHAR(100) NOT NULL,
    rol ENUM('Administrador', 'Mecanico', 'Recepcionista') NOT NULL,
    telefono VARCHAR(20),
    fecha_contratacion DATE,
    salario DECIMAL(10, 2)
);

-- Tabla de Clientes
CREATE TABLE Clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ap_paterno VARCHAR(100) NOT NULL,
    ap_materno VARCHAR(100),
    direccion VARCHAR(255),
    telefono VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100)
);

-- Tabla de Vehículos
CREATE TABLE Vehiculos (
  id_vehiculo INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente   INT,
  marca        VARCHAR(50) NOT NULL,
  modelo       VARCHAR(50) NOT NULL,
  anio         INT NOT NULL,
  color        VARCHAR(30),
  placas       VARCHAR(20) UNIQUE NOT NULL,
  CHECK (anio >= 1900),
  FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
);


-- Tabla de Servicios
CREATE TABLE Servicios (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    descripcion TEXT,
    costo       DECIMAL(10,2) NOT NULL,
    duracion    INT NOT NULL  -- duración en minutos
);

-- Tabla de Inventario
CREATE TABLE Inventario (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    cantidad INT NOT NULL CHECK (cantidad >= 0),
    precio DECIMAL(10,2) NOT NULL
);

-- Tabla de Proveedores
CREATE TABLE Proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    direccion VARCHAR(255)
);

-- Tabla de Vehículos de Empresa
CREATE TABLE Vehiculos_Empresa (
    id_vehiculo_empresa INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    placas VARCHAR(20) UNIQUE NOT NULL,
    estado ENUM('Disponible', 'En mantenimiento') NOT NULL DEFAULT 'Disponible'
);

-- Tabla de Citas
CREATE TABLE Citas (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_vehiculo INT,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('Pendiente', 'Completado', 'Cancelado') DEFAULT 'Pendiente',
    observaciones TEXT,
    FOREIGN KEY (id_vehiculo) REFERENCES Vehiculos(id_vehiculo)
);

-- Tabla de Órdenes de Trabajo
CREATE TABLE Ordenes_Trabajo (
    id_orden       INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente     INT NOT NULL,
    id_vehiculo    INT NOT NULL,
    id_servicio    INT NOT NULL,
    descripcion    TEXT,
    estado         ENUM('Pendiente','En Proceso','Completada') NOT NULL DEFAULT 'Pendiente',
    fecha_registro DATE NOT NULL,
    fecha_fin      DATE,
    FOREIGN KEY (id_cliente)   REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_vehiculo)  REFERENCES Vehiculos(id_vehiculo),
    FOREIGN KEY (id_servicio)  REFERENCES Servicios(id_servicio)
);

-- Tabla de relación entre Órdenes y Usuarios (empleados)
CREATE TABLE Ordenes_Empleados (
    id_orden   INT NOT NULL,
    id_usuario INT NOT NULL,
    PRIMARY KEY (id_orden, id_usuario),
    FOREIGN KEY (id_orden)   REFERENCES Ordenes_Trabajo(id_orden),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

CREATE USER 'dios'@'localhost' IDENTIFIED BY 'pass123';
GRANT ALL PRIVILEGES ON TallerMecanico.* TO 'dios'@'localhost';
FLUSH PRIVILEGES;

--DATOS DE PRUEBA
INSERT INTO Usuarios (nombre, ap_paterno, ap_materno, email, contraseña, rol, telefono, fecha_contratacion, salario) VALUES
('Carlos', 'Ramírez', 'López', 'admin@taller.com', '1234', 'Administrador', '5551234567', '2023-01-10', 15000.00),
('Pedro', 'Martínez', 'Gómez', 'meca@taller.com', '1234', 'Mecanico', '5557654321', '2023-03-12', 10000.00),
('Laura', 'Pérez', 'Torres', 'recep@taller.com', '1234', 'Recepcionista', '5556789012', '2024-02-20', 9000.00);

INSERT INTO Clientes (nombre, ap_paterno, ap_materno, direccion, telefono, email) VALUES
('Luis', 'Hernández', 'Ríos', 'Av. Siempre Viva 123', '5550001111', 'luis@mail.com'),
('Marta', 'Díaz', 'García', 'Calle Luna 45', '5552223333', 'marta@mail.com');

INSERT INTO Vehiculos (id_cliente, marca, modelo, anio, color, placas) VALUES
(1, 'Toyota', 'Corolla', 2018, 'Rojo', 'ABC-123-D'),
(2, 'Nissan', 'Versa', 2020, 'Gris', 'XYZ-456-E');

INSERT INTO Servicios (nombre, descripcion, costo, duracion) VALUES
('Cambio de aceite', 'Cambio de aceite y filtro de motor', 800.00, 30),
('Alineación y balanceo', 'Servicio de alineación y balanceo de llantas', 600.00, 45);


INSERT INTO Inventario (nombre, descripcion, cantidad, precio) VALUES
('Filtro de aceite', 'Filtro compatible con vehículos compactos', 50, 150.00),
('Aceite sintético 5W30', 'Aceite premium para motor', 30, 250.00);

INSERT INTO Proveedores (nombre, contacto, telefono, direccion) VALUES
('Autopartes MX', 'José Salgado', '5557778899', 'Blvd. Reforma 456'),
('Lubricantes S.A.', 'Ana Rivas', '5554443322', 'Calle del Taller 23');

INSERT INTO Citas (id_vehiculo, fecha, hora, estado, observaciones) VALUES
(1, '2025-06-05', '09:00:00', 'Pendiente', 'Revisión general'),
(2, '2025-06-06', '11:30:00', 'Pendiente', 'Cambio de aceite');

INSERT INTO Ordenes_Trabajo (descripcion, estado, fecha_inicio) VALUES
('Revisión de motor y frenos', 'En Proceso', '2025-06-01'),
('Servicio completo de alineación', 'Pendiente', '2025-06-02');

INSERT INTO Ordenes_Empleados (id_orden, id_usuario) VALUES
(1, 2),  -- Pedro (Mecánico) asignado a la orden 1
(2, 2);  -- Pedro (Mecánico) asignado a la orden 2





