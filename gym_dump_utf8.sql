-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: gym
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `amenity`
--

DROP TABLE IF EXISTS `amenity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `amenity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `price_per_day` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `amenity`
--

LOCK TABLES `amenity` WRITE;
/*!40000 ALTER TABLE `amenity` DISABLE KEYS */;
INSERT INTO `amenity` VALUES (1,'Elite Locker Access',10),(2,'Steam & Sauna Protocol',25),(3,'Personal Trainer Assistance',100),(4,'Supplement Bar Credits',40),(5,'VIP Shower Lounge',15);
/*!40000 ALTER TABLE `amenity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int DEFAULT NULL,
  `trainer_id` int DEFAULT NULL,
  `check_in` datetime DEFAULT NULL,
  `check_out` datetime DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  KEY `trainer_id` (`trainer_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`),
  CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`trainer_id`) REFERENCES `trainer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (6,NULL,2,'2026-03-03 19:42:23','2026-03-03 19:45:31','2026-03-03'),(9,NULL,2,'2026-03-04 09:32:59','2026-03-04 09:33:18','2026-03-04'),(11,NULL,2,'2026-03-04 09:33:33','2026-03-04 09:33:45','2026-03-04'),(13,NULL,2,'2026-03-05 20:47:11','2026-03-05 20:47:19','2026-03-05'),(14,NULL,2,'2026-03-09 22:16:00','2026-03-10 00:00:00','2026-03-09'),(15,NULL,2,'2026-03-14 23:07:04','2026-03-14 23:07:20','2026-03-14'),(16,2,NULL,'2026-03-14 23:07:10','2026-03-14 23:07:14','2026-03-14'),(17,NULL,2,'2026-03-14 23:09:29','2026-03-14 23:18:15','2026-03-14'),(18,NULL,2,'2026-03-15 12:06:08','2026-03-16 00:00:00','2026-03-15'),(19,NULL,2,'2026-03-16 09:58:48','2026-03-16 10:32:18','2026-03-16'),(20,NULL,2,'2026-03-16 10:32:29','2026-03-16 11:49:17','2026-03-16'),(21,NULL,2,'2026-03-16 13:50:54',NULL,'2026-03-16'),(22,2,NULL,'2026-03-27 10:01:45',NULL,'2026-03-27');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `trainer_id` int DEFAULT NULL,
  `equipment_id` int DEFAULT NULL,
  `booking_date` date NOT NULL,
  `booking_time_from` time NOT NULL,
  `booking_time_to` time NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_by_role` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  KEY `trainer_id` (`trainer_id`),
  KEY `equipment_id` (`equipment_id`),
  CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`),
  CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`trainer_id`) REFERENCES `trainer` (`id`),
  CONSTRAINT `booking_ibfk_3` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (13,2,2,2,'2026-03-14','21:40:00','22:00:00','Confirmed','user','2026-03-14 21:36:55'),(15,2,2,2,'2026-03-16','12:00:00','13:00:00','Confirmed','user','2026-03-16 10:01:31'),(16,2,2,2,'2026-03-16','13:00:00','15:00:00','Confirmed','user','2026-03-16 13:48:40'),(18,3,NULL,8,'2026-03-27','12:00:00','13:00:00','Cancelled','user','2026-03-27 09:59:20');
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custom_plan`
--

DROP TABLE IF EXISTS `custom_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `custom_plan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `selected_days` varchar(200) DEFAULT NULL,
  `amenities` text,
  `total_price` float NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `custom_plan_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custom_plan`
--

LOCK TABLES `custom_plan` WRITE;
/*!40000 ALTER TABLE `custom_plan` DISABLE KEYS */;
INSERT INTO `custom_plan` VALUES (1,2,'Monday, Tuesday','[\"Elite Locker Access\", \"Steam & Sauna Protocol\"]',680,'Approved','2026-03-14 15:19:26'),(2,2,'Monday','[\"Elite Locker Access\", \"Steam & Sauna Protocol\"]',140,'Approved','2026-03-14 15:38:00');
/*!40000 ALTER TABLE `custom_plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `diet_plan`
--

DROP TABLE IF EXISTS `diet_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diet_plan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `trainer_id` int NOT NULL,
  `plan_name` varchar(100) NOT NULL,
  `description` text,
  `breakfast` text,
  `lunch` text,
  `dinner` text,
  `snacks` text,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  KEY `trainer_id` (`trainer_id`),
  CONSTRAINT `diet_plan_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`),
  CONSTRAINT `diet_plan_ibfk_2` FOREIGN KEY (`trainer_id`) REFERENCES `trainer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diet_plan`
--

LOCK TABLES `diet_plan` WRITE;
/*!40000 ALTER TABLE `diet_plan` DISABLE KEYS */;
INSERT INTO `diet_plan` VALUES (3,2,2,'push up x 10','hhhh','hh','hh','hh','hh','2026-03-16 09:27:41');
/*!40000 ALTER TABLE `diet_plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `quantity` int DEFAULT NULL,
  `broken_quantity` int DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `image_file` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `gym_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment`
--

LOCK TABLES `equipment` WRITE;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
INSERT INTO `equipment` VALUES (2,'TRADE MILL','GOOD FOR LEG MUSCLES',4,0,'Working','equip_1772603259.360922_Screenshot_2026-03-04_111714.png','2026-03-04 11:17:39','1234'),(3,'Treadmill X-500','High-end treadmill with heart rate monitoring and incline control.',1,0,'Working','equipment_default.png','2026-03-14 21:29:00','1234'),(4,'Olympic Barbell','Standard 20kg barbell for heavy lifting.',1,0,'Working','equipment_default.png','2026-03-14 21:29:00','1234'),(5,'Dumbbell Set (5kg-50kg)','Complete set of rubber-coated dumbbells.',2,1,'Working','equipment_default.png','2026-03-14 21:29:00','1234'),(6,'Leg Press Machine','Heavy-duty leg press machine. Currently awaiting cable replacement.',1,0,'Maintenance','equipment_default.png','2026-03-14 21:29:00','1234'),(7,'Power Rack','Versatile power rack for squats, bench press, and pull-ups.',1,0,'Working','equipment_default.png','2026-03-14 21:29:00','1234'),(8,'TRADE MILL','waliiking',2,0,'Working','equipment_default.png','2026-03-27 09:50:39','7777');
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_usage`
--

DROP TABLE IF EXISTS `equipment_usage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_usage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `equipment_id` int NOT NULL,
  `member_id` int NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `equipment_id` (`equipment_id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `equipment_usage_ibfk_1` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`id`),
  CONSTRAINT `equipment_usage_ibfk_2` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_usage`
--

LOCK TABLES `equipment_usage` WRITE;
/*!40000 ALTER TABLE `equipment_usage` DISABLE KEYS */;
/*!40000 ALTER TABLE `equipment_usage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `export_log`
--

DROP TABLE IF EXISTS `export_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `export_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `report_type` varchar(50) NOT NULL,
  `performed_at` datetime DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `total_amount` float DEFAULT NULL,
  `performed_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `export_log`
--

LOCK TABLES `export_log` WRITE;
/*!40000 ALTER TABLE `export_log` DISABLE KEYS */;
INSERT INTO `export_log` VALUES (9,'Revenue','2026-03-14 21:34:05','2026-03-14','2026-03-14',870,'admin'),(10,'Revenue','2026-03-16 09:57:11','2026-03-01','2026-03-16',10789.7,'admin'),(11,'Revenue','2026-03-16 10:30:40','2026-03-01','2026-03-16',10789.7,'admin');
/*!40000 ALTER TABLE `export_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `height` float DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `membership_type` varchar(50) DEFAULT NULL,
  `plan_id` int DEFAULT NULL,
  `pending_plan_id` int DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT NULL,
  `workout_days` varchar(255) DEFAULT NULL,
  `expiry_date` datetime DEFAULT NULL,
  `date_approved` datetime DEFAULT NULL,
  `gym_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `plan_id` (`plan_id`),
  KEY `pending_plan_id` (`pending_plan_id`),
  CONSTRAINT `member_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `member_ibfk_2` FOREIGN KEY (`plan_id`) REFERENCES `membership_plan` (`id`),
  CONSTRAINT `member_ibfk_3` FOREIGN KEY (`pending_plan_id`) REFERENCES `membership_plan` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (2,13,'Kuttan','8606891602',NULL,160,62.2,NULL,1,NULL,'Expired',1,'Monday','2026-03-17 09:55:33','2026-03-14 12:55:48','1234'),(3,15,'user7','1111111111',NULL,159,80,NULL,3,1,'Active',1,'Tue, Wed, Thu, Fri','2026-04-26 09:40:33','2026-03-27 09:40:33','7777');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membership_plan`
--

DROP TABLE IF EXISTS `membership_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `membership_plan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `price` float NOT NULL,
  `duration_days` int DEFAULT NULL,
  `features` text,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membership_plan`
--

LOCK TABLES `membership_plan` WRITE;
/*!40000 ALTER TABLE `membership_plan` DISABLE KEYS */;
INSERT INTO `membership_plan` VALUES (1,'Base Plan',50,1,'Limited Facility Access, Gym Floor Access','2026-02-25 05:32:56'),(2,'Premium',1699,30,'Full Facility Access, General Trainer Support, Group Classes','2026-02-25 05:32:56'),(3,'Premium Elite',6969.69,30,'Full Access, Personal Trainer, Personalised Workouts, Nutritionist Support, Diet Plans','2026-02-25 05:32:56');
/*!40000 ALTER TABLE `membership_plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `amount` float NOT NULL,
  `payment_date` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `gym_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (2,2,680,'2026-03-14 15:19:49','Paid','1234'),(3,2,140,'2026-03-14 15:38:19','Paid','1234'),(4,2,50,'2026-03-14 16:11:44','Paid','1234'),(8,2,200,'2026-03-16 09:55:33','Paid','1234'),(9,3,6969.69,'2026-03-27 09:40:33','Paid','7777');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trainer`
--

DROP TABLE IF EXISTS `trainer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trainer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `experience` int DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `is_approved` tinyint(1) DEFAULT NULL,
  `gym_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `trainer_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trainer`
--

LOCK TABLES `trainer` WRITE;
/*!40000 ALTER TABLE `trainer` DISABLE KEYS */;
INSERT INTO `trainer` VALUES (2,8,'trainer','',5,'9999999999',1,'1234');
/*!40000 ALTER TABLE `trainer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(20) DEFAULT NULL,
  `profile_pic` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `deletion_requested` tinyint(1) DEFAULT NULL,
  `login_count` int DEFAULT NULL,
  `otp` varchar(6) DEFAULT NULL,
  `otp_expiry` datetime DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gym_id` varchar(50) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (6,'admin','nikeshnpai3@gmail.com','admin123','admin','default.png','1111111111','2026-02-24 15:34:10',0,50,NULL,NULL,NULL,'1234',NULL,NULL),(8,'trainer','nikeshnpai225@gmail.com','111','trainer','default.png','9999999999','2026-02-25 04:16:19',0,15,NULL,NULL,NULL,'1234',NULL,NULL),(13,'Kuttan','nikeshnpai5@gmail.com','1234','user','default.png','8606891602','2026-03-14 12:54:43',0,28,NULL,NULL,NULL,'1234',NULL,NULL),(14,'admin7','malavikamohan778@gmail.com','karinchund@69','admin','default.png','6282144432','2026-03-27 09:34:32',0,4,NULL,'2026-03-27 09:40:56',NULL,'7777',19,NULL),(15,'user7','malavikamohanan015@gmail.com','123','user','default.png','1111111111','2026-03-27 09:39:18',0,2,NULL,NULL,'2004-07-14','7777',21,'male');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weight_log`
--

DROP TABLE IF EXISTS `weight_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weight_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `weight` float NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `weight_log_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weight_log`
--

LOCK TABLES `weight_log` WRITE;
/*!40000 ALTER TABLE `weight_log` DISABLE KEYS */;
INSERT INTO `weight_log` VALUES (1,2,69,'2026-03-15 12:17:58'),(2,2,50.3,'2026-03-15 12:20:22'),(3,2,62.2,'2026-03-15 12:21:45');
/*!40000 ALTER TABLE `weight_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workout_plan`
--

DROP TABLE IF EXISTS `workout_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workout_plan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `trainer_id` int NOT NULL,
  `plan_name` varchar(100) DEFAULT NULL,
  `exercises` text,
  `day` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  KEY `trainer_id` (`trainer_id`),
  CONSTRAINT `workout_plan_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`),
  CONSTRAINT `workout_plan_ibfk_2` FOREIGN KEY (`trainer_id`) REFERENCES `trainer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workout_plan`
--

LOCK TABLES `workout_plan` WRITE;
/*!40000 ALTER TABLE `workout_plan` DISABLE KEYS */;
INSERT INTO `workout_plan` VALUES (1,2,2,'hhh','hyfghj','Monday','2026-03-16 09:59:16');
/*!40000 ALTER TABLE `workout_plan` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-28 13:10:09
