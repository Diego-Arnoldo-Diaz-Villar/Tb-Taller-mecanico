-- MySQL dump 10.13  Distrib 9.2.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: TallerMecanico
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Citas`
--

DROP TABLE IF EXISTS `Citas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Citas` (
  `id_cita` int NOT NULL AUTO_INCREMENT,
  `id_vehiculo` int DEFAULT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `estado` enum('Pendiente','Completado','Cancelado') DEFAULT 'Pendiente',
  `observaciones` text,
  PRIMARY KEY (`id_cita`),
  KEY `id_vehiculo` (`id_vehiculo`),
  CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`id_vehiculo`) REFERENCES `Vehiculos` (`id_vehiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Citas`
--

LOCK TABLES `Citas` WRITE;
/*!40000 ALTER TABLE `Citas` DISABLE KEYS */;
/*!40000 ALTER TABLE `Citas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Clientes`
--

DROP TABLE IF EXISTS `Clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `ap_paterno` varchar(100) NOT NULL,
  `ap_materno` varchar(100) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `telefono` (`telefono`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Clientes`
--

LOCK TABLES `Clientes` WRITE;
/*!40000 ALTER TABLE `Clientes` DISABLE KEYS */;
INSERT INTO `Clientes` VALUES (2,'Alvaro','Holguin','Herrera','Av tecnologico #29','6463738','alvaro@gmail.com');
/*!40000 ALTER TABLE `Clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Inventario`
--

DROP TABLE IF EXISTS `Inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Inventario` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `cantidad` int NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_producto`),
  CONSTRAINT `inventario_chk_1` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Inventario`
--

LOCK TABLES `Inventario` WRITE;
/*!40000 ALTER TABLE `Inventario` DISABLE KEYS */;
/*!40000 ALTER TABLE `Inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ordenes_Empleados`
--

DROP TABLE IF EXISTS `Ordenes_Empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ordenes_Empleados` (
  `id_orden` int NOT NULL,
  `id_usuario` int NOT NULL,
  PRIMARY KEY (`id_orden`,`id_usuario`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `ordenes_empleados_ibfk_1` FOREIGN KEY (`id_orden`) REFERENCES `Ordenes_Trabajo` (`id_orden`),
  CONSTRAINT `ordenes_empleados_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ordenes_Empleados`
--

LOCK TABLES `Ordenes_Empleados` WRITE;
/*!40000 ALTER TABLE `Ordenes_Empleados` DISABLE KEYS */;
INSERT INTO `Ordenes_Empleados` VALUES (1,2);
/*!40000 ALTER TABLE `Ordenes_Empleados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ordenes_Trabajo`
--

DROP TABLE IF EXISTS `Ordenes_Trabajo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ordenes_Trabajo` (
  `id_orden` int NOT NULL AUTO_INCREMENT,
  `descripcion` text,
  `estado` enum('Pendiente','En Proceso','Completada') NOT NULL DEFAULT 'Pendiente',
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  PRIMARY KEY (`id_orden`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ordenes_Trabajo`
--

LOCK TABLES `Ordenes_Trabajo` WRITE;
/*!40000 ALTER TABLE `Ordenes_Trabajo` DISABLE KEYS */;
INSERT INTO `Ordenes_Trabajo` VALUES (1,'Cambio de aceite','Pendiente','2025-05-07',NULL);
/*!40000 ALTER TABLE `Ordenes_Trabajo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Proveedores`
--

DROP TABLE IF EXISTS `Proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Proveedores` (
  `id_proveedor` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `contacto` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_proveedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Proveedores`
--

LOCK TABLES `Proveedores` WRITE;
/*!40000 ALTER TABLE `Proveedores` DISABLE KEYS */;
/*!40000 ALTER TABLE `Proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Servicios`
--

DROP TABLE IF EXISTS `Servicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Servicios` (
  `id_servicio` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `costo` decimal(10,2) NOT NULL,
  `duracion` int DEFAULT NULL,
  PRIMARY KEY (`id_servicio`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Servicios`
--

LOCK TABLES `Servicios` WRITE;
/*!40000 ALTER TABLE `Servicios` DISABLE KEYS */;
INSERT INTO `Servicios` VALUES (1,'Cambio de aceite','Se realizara un cambio de aceite de motor',150.00,40);
/*!40000 ALTER TABLE `Servicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuarios`
--

DROP TABLE IF EXISTS `Usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `ap_paterno` varchar(100) NOT NULL,
  `ap_materno` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `contraseña` varchar(100) NOT NULL,
  `rol` enum('Administrador','Mecanico','Recepcionista') NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `fecha_contratacion` date DEFAULT NULL,
  `salario` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuarios`
--

LOCK TABLES `Usuarios` WRITE;
/*!40000 ALTER TABLE `Usuarios` DISABLE KEYS */;
INSERT INTO `Usuarios` VALUES (1,'admin','Perez','Lopez','admin@example.com','admin123','Administrador',NULL,NULL,NULL),(2,'mecanico1','Gomez','Ramirez','mecanico1@example.com','meca123','Mecanico',NULL,NULL,NULL),(4,'Edson','Talamantes','Chavez','edsontchflo@gmail.com','edson9911','Administrador',NULL,NULL,NULL),(5,'recepcion','Sanchez','Diaz','recepcion@example.com','recep123','Recepcionista',NULL,NULL,NULL);
/*!40000 ALTER TABLE `Usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Vehiculos`
--

DROP TABLE IF EXISTS `Vehiculos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Vehiculos` (
  `id_vehiculo` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int DEFAULT NULL,
  `marca` varchar(50) NOT NULL,
  `modelo` varchar(50) NOT NULL,
  `año` int DEFAULT NULL,
  `color` varchar(30) DEFAULT NULL,
  `placas` varchar(20) NOT NULL,
  PRIMARY KEY (`id_vehiculo`),
  UNIQUE KEY `placas` (`placas`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `vehiculos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `Clientes` (`id_cliente`),
  CONSTRAINT `vehiculos_chk_1` CHECK ((`año` >= 1900))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Vehiculos`
--

LOCK TABLES `Vehiculos` WRITE;
/*!40000 ALTER TABLE `Vehiculos` DISABLE KEYS */;
/*!40000 ALTER TABLE `Vehiculos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Vehiculos_Empresa`
--

DROP TABLE IF EXISTS `Vehiculos_Empresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Vehiculos_Empresa` (
  `id_vehiculo_empresa` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(50) NOT NULL,
  `marca` varchar(50) DEFAULT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `placas` varchar(20) NOT NULL,
  `estado` enum('Disponible','En mantenimiento') NOT NULL DEFAULT 'Disponible',
  PRIMARY KEY (`id_vehiculo_empresa`),
  UNIQUE KEY `placas` (`placas`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Vehiculos_Empresa`
--

LOCK TABLES `Vehiculos_Empresa` WRITE;
/*!40000 ALTER TABLE `Vehiculos_Empresa` DISABLE KEYS */;
/*!40000 ALTER TABLE `Vehiculos_Empresa` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-07 20:56:38
