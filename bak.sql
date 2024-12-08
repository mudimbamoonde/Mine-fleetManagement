-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: fleetmgr
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `drill_blast`
--

DROP TABLE IF EXISTS `drill_blast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `drill_blast` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `blastedVolume` int(100) NOT NULL,
  `numberOfDaysRequired` int(100) NOT NULL,
  `actual_volumeMovedPayDay` int(100) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `modified_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drill_blast`
--

LOCK TABLES `drill_blast` WRITE;
/*!40000 ALTER TABLE `drill_blast` DISABLE KEYS */;
INSERT INTO `drill_blast` VALUES (1,2000,1,1,'2024-12-07 22:53:44','2024-12-08 22:53:44');
/*!40000 ALTER TABLE `drill_blast` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER numberOfDaysRequired_to_deplete_material BEFORE INSERT ON drill_blast
FOR EACH ROW SET @bl = NEW.blastedVolume / 20*(SELECT quantity FROM mobile_epq WHERE equipment='Tiper') */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `equipment` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `equipment` varchar(250) NOT NULL,
  `lastDayOfService` varchar(250) NOT NULL,
  `lastOfService` varchar(250) NOT NULL,
  `NextDue` varchar(250) NOT NULL,
  `meID` varchar(10) NOT NULL,
  `Status` enum('Down','Ready','Shift Change') DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment`
--

LOCK TABLES `equipment` WRITE;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
INSERT INTO `equipment` VALUES (1,'Dozer','2024-12-08','1550','2000','BBC2011','Ready'),(2,'Dozer','2024-12-10','2000','5000','BBC2010','Down'),(3,'Dozer','2024-12-08','8000','9500','BCC2012','Shift Change'),(4,'Tiper','2024-12-08','5800','6200','TY109','Down'),(5,'Dozer','2024-12-08','8994','9250','ABG1092','Ready'),(6,'Tiper','2024-12-04','101198','105198','ABG1093','Down'),(7,'Tiper','2024-12-08','59844','62045','ABC 2819','Ready'),(8,'Crusher','2024-12-08','2555','7555','BAH1029','Ready'),(9,'Drilling Machine','2024-12-08','0','0','ZK10','Ready');
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hourly_ore`
--

DROP TABLE IF EXISTS `hourly_ore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hourly_ore` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `actual_hour_from` time NOT NULL,
  `actual_hour_to` time NOT NULL,
  `actual_volume` varchar(250) NOT NULL,
  `ShiftName` varchar(250) NOT NULL,
  `shifID` int(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `modified_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shifID` (`shifID`),
  CONSTRAINT `hourly_ore_ibfk_1` FOREIGN KEY (`shifID`) REFERENCES `shifts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hourly_ore`
--

LOCK TABLES `hourly_ore` WRITE;
/*!40000 ALTER TABLE `hourly_ore` DISABLE KEYS */;
INSERT INTO `hourly_ore` VALUES (1,'07:00:00','08:00:00','230','Morning',1,'2024-12-08 16:56:45','2024-12-04 16:56:45'),(2,'08:00:00','09:00:00','300','Morning',1,'2024-12-08 20:03:40','2024-12-08 20:03:40'),(3,'09:00:00','10:00:00','230','Morning',1,'2024-12-08  20:05:49','2024-12-08  20:05:49'),(4,'07:00:00','08:00:00','250','Morning',1,'2024-12-08  23:08:40','2024-12-08  23:08:40'),(5,'08:00:00','09:00:00','302','Morning',1,'2024-12-08 12:21:05','2024-12-08 13:38:21');
/*!40000 ALTER TABLE `hourly_ore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hourly_waste`
--

DROP TABLE IF EXISTS `hourly_waste`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hourly_waste` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `actual_hour_from` time NOT NULL,
  `actual_hour_to` time NOT NULL,
  `actual_volume` varchar(250) NOT NULL,
  `ShiftName` varchar(250) NOT NULL,
  `shifID` int(20) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `modified_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `shifID` (`shifID`),
  CONSTRAINT `hourly_waste_ibfk_1` FOREIGN KEY (`shifID`) REFERENCES `shifts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hourly_waste`
--

LOCK TABLES `hourly_waste` WRITE;
/*!40000 ALTER TABLE `hourly_waste` DISABLE KEYS */;
INSERT INTO `hourly_waste` VALUES (1,'07:00:00','08:00:00','200','Morning',1,'2024-12-04 23:10:36','2024-12-04 23:10:36'),(2,'08:00:00','09:00:00','350','Morning',1,'2024-12-04 23:40:44','2024-12-04 23:40:44'),(3,'07:00:00','07:00:00','200','Morning',1,'2024-12-08 12:21:35','2024-12-08 12:21:35');
/*!40000 ALTER TABLE `hourly_waste` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inputoutput`
--

DROP TABLE IF EXISTS `inputoutput`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inputoutput` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `SectionName` varchar(250) NOT NULL,
  `plannedInput` varchar(250) NOT NULL,
  `actualinputs` varchar(250) NOT NULL,
  `Utilisation` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inputoutput`
--

LOCK TABLES `inputoutput` WRITE;
/*!40000 ALTER TABLE `inputoutput` DISABLE KEYS */;
/*!40000 ALTER TABLE `inputoutput` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mobile_epq`
--

DROP TABLE IF EXISTS `mobile_epq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mobile_epq` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `equipment` varchar(250) NOT NULL,
  `model` varchar(250) NOT NULL,
  `specification` varchar(250) NOT NULL,
  `quantity` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mobile_epq`
--

LOCK TABLES `mobile_epq` WRITE;
/*!40000 ALTER TABLE `mobile_epq` DISABLE KEYS */;
INSERT INTO `mobile_epq` VALUES (1,'Tiper','Howo','20 tonne',10),(2,'Dozer','Kumasu','4 m3',1),(3,'Crusher','Jaw Crusher','PEW',350),(4,'Drilling Machine','Panterra','152 mm',1);
/*!40000 ALTER TABLE `mobile_epq` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shifts`
--

DROP TABLE IF EXISTS `shifts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shifts` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `Morning` varchar(250) NOT NULL,
  `Afternoon` varchar(250) NOT NULL,
  `Target` varchar(250) NOT NULL,
  `Total` varchar(250) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `modified_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shifts`
--

LOCK TABLES `shifts` WRITE;
/*!40000 ALTER TABLE `shifts` DISABLE KEYS */;
INSERT INTO `shifts` VALUES (1,'2100','2100','4200','4200','2024-12-04 16:01:30','2024-12-08 12:14:25');
/*!40000 ALTER TABLE `shifts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle_data`
--

DROP TABLE IF EXISTS `vehicle_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicle_data` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `vehicle_id` int(100) NOT NULL,
  `location` text NOT NULL,
  `speed` decimal(10,0) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_data`
--

LOCK TABLES `vehicle_data` WRITE;
/*!40000 ALTER TABLE `vehicle_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `vehicle_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicles`
--

DROP TABLE IF EXISTS `vehicles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehicles` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `make` text NOT NULL,
  `model` text NOT NULL,
  `year` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicles`
--

LOCK TABLES `vehicles` WRITE;
/*!40000 ALTER TABLE `vehicles` DISABLE KEYS */;
/*!40000 ALTER TABLE `vehicles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-08 15:23:44
