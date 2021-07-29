-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: variant_db
-- ------------------------------------------------------
-- Server version	8.0.25

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
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `staff` tinyint(1) NOT NULL,
  `specialist` tinyint(1) NOT NULL,
  `counselor` tinyint(1) NOT NULL,
  `scientist` tinyint(1) NOT NULL,
  `admin` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$260000$K2pDIvvqY7LUYOxGQ9Nly8$wtBdZOHNLt0ATCbX2SmMn/XmFWgkst3fWjdO7D7546M=',NULL,1,'admin','irene.chae@uhn.ca',1,1,1,1,1,1,1),(2,'pbkdf2_sha256$260000$dQJ1SEF3xpeN6T8bSCoNlJ$nlmEKr7k/ehxTIrhxGIdOlgvYxpcVRU4C+Fm9xDeudA=',NULL,0,'scientist','scientist@uhn.ca',1,1,1,1,1,1,0),(3,'pbkdf2_sha256$260000$5sFIBxf6Pt0fz6iYo7aYpq$GoJPJAvBOCCNAURd/P4hkcw1cQ1+5/EbUb055M759SI=',NULL,0,'counselor','counselor@uhn.ca',1,1,1,1,1,0,0),(4,'pbkdf2_sha256$260000$rQ79Jm20o3QqoyGsWNPSCH$xpS9zUI9dwsbeRyi6nGRE7mypKXdMNRfSYjjs5UUdSI=',NULL,0,'specialist','specialist@uhn.ca',1,1,1,1,0,0,0),(5,'pbkdf2_sha256$260000$WRMdFxOAgif7at5dDkrPcB$8RRCp+ZOIO21CixrlBRMm1LoQnUoGX+XeILzMXANA1E=',NULL,0,'staff','staff@uhn.ca',1,1,1,0,0,0,0);
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_cancerhotspot`
--

DROP TABLE IF EXISTS `api_cancerhotspot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_cancerhotspot` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hotspot` varchar(70) NOT NULL,
  `count` int NOT NULL,
  `variant_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_cancerhotspot_variant_id_cf7da97d_fk_api_variant_id` (`variant_id`),
  CONSTRAINT `api_cancerhotspot_variant_id_cf7da97d_fk_api_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `api_variant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_cancerhotspot`
--

LOCK TABLES `api_cancerhotspot` WRITE;
/*!40000 ALTER TABLE `api_cancerhotspot` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_cancerhotspot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_disease`
--

DROP TABLE IF EXISTS `api_disease`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_disease` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `branch` varchar(2) NOT NULL,
  `func_sig` varchar(20) DEFAULT NULL,
  `others` varchar(20) DEFAULT NULL,
  `report` longtext NOT NULL,
  `reviewed` varchar(1) NOT NULL,
  `reviewed_date` datetime(6) DEFAULT NULL,
  `meta_reviewed_date` datetime(6) DEFAULT NULL,
  `approved_date` datetime(6) DEFAULT NULL,
  `curation_notes` longtext NOT NULL,
  `approve_user_id` int DEFAULT NULL,
  `meta_review_user_id` int DEFAULT NULL,
  `review_user_id` int DEFAULT NULL,
  `variant_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_disease_variant_id_81f53161_fk_api_variant_id` (`variant_id`),
  KEY `api_disease_approve_user_id_d3cfd6c1_fk_accounts_user_id` (`approve_user_id`),
  KEY `api_disease_meta_review_user_id_4a3401af_fk_accounts_user_id` (`meta_review_user_id`),
  KEY `api_disease_review_user_id_138a07a6_fk_accounts_user_id` (`review_user_id`),
  CONSTRAINT `api_disease_approve_user_id_d3cfd6c1_fk_accounts_user_id` FOREIGN KEY (`approve_user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `api_disease_meta_review_user_id_4a3401af_fk_accounts_user_id` FOREIGN KEY (`meta_review_user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `api_disease_review_user_id_138a07a6_fk_accounts_user_id` FOREIGN KEY (`review_user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `api_disease_variant_id_81f53161_fk_api_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `api_variant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_disease`
--

LOCK TABLES `api_disease` WRITE;
/*!40000 ALTER TABLE `api_disease` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_disease` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_evidence`
--

DROP TABLE IF EXISTS `api_evidence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_evidence` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item` varchar(75) NOT NULL,
  `source_type` varchar(2) NOT NULL,
  `source_id` varchar(20) NOT NULL,
  `statement` longtext,
  `evid_sig` varchar(4) DEFAULT NULL,
  `level` varchar(1) DEFAULT NULL,
  `evid_dir` tinyint(1) DEFAULT NULL,
  `clin_sig` varchar(25) DEFAULT NULL,
  `drug_class` longtext,
  `evid_rating` int DEFAULT NULL,
  `disease_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_evidence_disease_id_0f0c81a5_fk_api_disease_id` (`disease_id`),
  CONSTRAINT `api_evidence_disease_id_0f0c81a5_fk_api_disease_id` FOREIGN KEY (`disease_id`) REFERENCES `api_disease` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_evidence`
--

LOCK TABLES `api_evidence` WRITE;
/*!40000 ALTER TABLE `api_evidence` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_evidence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_gene`
--

DROP TABLE IF EXISTS `api_gene`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_gene` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `content` longtext,
  `germline_content` longtext,

  `actionable` varchar(50),
  `not_actionable` varchar(50),
  `mut_type` varchar(50),
  `region` varchar(50),
  `reviewed_date` datetime(6),
  `gene_curation_notes` longtext NOT NULL,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_gene`
--

LOCK TABLES `api_gene` WRITE;
/*!40000 ALTER TABLE `api_gene` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_gene` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_history`
--

DROP TABLE IF EXISTS `api_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` longtext,
  `timestamp` datetime(6) NOT NULL,
  `object_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `variant_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_history_object_id_33723063_fk_api_evidence_id` (`object_id`),
  KEY `api_history_user_id_b67a8aac_fk_accounts_user_id` (`user_id`),
  KEY `api_history_variant_id_9b04b65b_fk_api_variant_id` (`variant_id`),
  CONSTRAINT `api_history_object_id_33723063_fk_api_evidence_id` FOREIGN KEY (`object_id`) REFERENCES `api_evidence` (`id`),
  CONSTRAINT `api_history_user_id_b67a8aac_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `api_history_variant_id_9b04b65b_fk_api_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `api_variant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_history`
--

LOCK TABLES `api_history` WRITE;
/*!40000 ALTER TABLE `api_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_predpmid`
--

DROP TABLE IF EXISTS `api_predpmid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_predpmid` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `value` varchar(40) NOT NULL,
  `pmids` varchar(50) NOT NULL,
  `variant_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_predpmid_variant_id_e36ab1c0_fk_api_variant_id` (`variant_id`),
  CONSTRAINT `api_predpmid_variant_id_e36ab1c0_fk_api_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `api_variant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_predpmid`
--

LOCK TABLES `api_predpmid` WRITE;
/*!40000 ALTER TABLE `api_predpmid` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_predpmid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_report`
--

DROP TABLE IF EXISTS `api_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_report` (
  `id` int NOT NULL AUTO_INCREMENT,
  `report_name` varchar(40) NOT NULL,
  `content` longtext,
  `disease_id` int DEFAULT NULL,
  `gene_id` int DEFAULT NULL,
  `variant_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_report_disease_id_7b991380_fk_api_disease_id` (`disease_id`),
  KEY `api_report_gene_id_0bb37a9a_fk_api_gene_id` (`gene_id`),
  KEY `api_report_variant_id_43721d97_fk_api_variant_id` (`variant_id`),
  CONSTRAINT `api_report_disease_id_7b991380_fk_api_disease_id` FOREIGN KEY (`disease_id`) REFERENCES `api_disease` (`id`),
  CONSTRAINT `api_report_gene_id_0bb37a9a_fk_api_gene_id` FOREIGN KEY (`gene_id`) REFERENCES `api_gene` (`id`),
  CONSTRAINT `api_report_variant_id_43721d97_fk_api_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `api_variant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_report`
--

LOCK TABLES `api_report` WRITE;
/*!40000 ALTER TABLE `api_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_report` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `api_review`
--

DROP TABLE IF EXISTS `api_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_review` (
  `id` int NOT NULL AUTO_INCREMENT,
  `review` varchar(1) NOT NULL,
  `date` datetime(6) NOT NULL,
  `disease_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_review_disease_id_79f427e0_fk_api_disease_id` (`disease_id`),
  KEY `api_review_user_id_8bf97ad4_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `api_review_disease_id_79f427e0_fk_api_disease_id` FOREIGN KEY (`disease_id`) REFERENCES `api_disease` (`id`),
  CONSTRAINT `api_review_user_id_8bf97ad4_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_review`
--

LOCK TABLES `api_review` WRITE;
/*!40000 ALTER TABLE `api_review` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_score`
--

DROP TABLE IF EXISTS `api_score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_score` (
  `id` int NOT NULL AUTO_INCREMENT,
  `for_score` varchar(20) NOT NULL,
  `against_score` varchar(20) NOT NULL,
  `content` varchar(100) NOT NULL,
  `disease_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `disease_id` (`disease_id`),
  CONSTRAINT `api_score_disease_id_36796f93_fk_api_disease_id` FOREIGN KEY (`disease_id`) REFERENCES `api_disease` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_score`
--

LOCK TABLES `api_score` WRITE;
/*!40000 ALTER TABLE `api_score` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_variant`
--

DROP TABLE IF EXISTS `api_variant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_variant` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cdna` varchar(60) NOT NULL,
  `protein` varchar(60) NOT NULL,
  `chr` varchar(6) NOT NULL,
  `transcript` varchar(20) NOT NULL,
  `start` varchar(10) NOT NULL,
  `end` varchar(10) NOT NULL,
  `ref` varchar(100) NOT NULL,
  `alt` varchar(100) NOT NULL,
  `content` longtext NOT NULL,
  `germline_content` longtext NOT NULL,
  `gene_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `api_variant_gene_id_5263a79c_fk_api_gene_id` (`gene_id`),
  CONSTRAINT `api_variant_gene_id_5263a79c_fk_api_gene_id` FOREIGN KEY (`gene_id`) REFERENCES `api_gene` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_variant`
--

LOCK TABLES `api_variant` WRITE;
/*!40000 ALTER TABLE `api_variant` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_variant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_variantfield`
--

DROP TABLE IF EXISTS `api_variantfield`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_variantfield` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `value` varchar(500) NOT NULL,
  `variant_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_variantfield_variant_id_1906d223_fk_api_variant_id` (`variant_id`),
  CONSTRAINT `api_variantfield_variant_id_1906d223_fk_api_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `api_variant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_variantfield`
--

LOCK TABLES `api_variantfield` WRITE;
/*!40000 ALTER TABLE `api_variantfield` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_variantfield` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add disease',1,'add_disease'),(2,'Can change disease',1,'change_disease'),(3,'Can delete disease',1,'delete_disease'),(4,'Can view disease',1,'view_disease'),(5,'Can add evidence',2,'add_evidence'),(6,'Can change evidence',2,'change_evidence'),(7,'Can delete evidence',2,'delete_evidence'),(8,'Can view evidence',2,'view_evidence'),(9,'Can add gene',3,'add_gene'),(10,'Can change gene',3,'change_gene'),(11,'Can delete gene',3,'delete_gene'),(12,'Can view gene',3,'view_gene'),(13,'Can add variant',4,'add_variant'),(14,'Can change variant',4,'change_variant'),(15,'Can delete variant',4,'delete_variant'),(16,'Can view variant',4,'view_variant'),(17,'Can add variant field',5,'add_variantfield'),(18,'Can change variant field',5,'change_variantfield'),(19,'Can delete variant field',5,'delete_variantfield'),(20,'Can view variant field',5,'view_variantfield'),(21,'Can add score',6,'add_score'),(22,'Can change score',6,'change_score'),(23,'Can delete score',6,'delete_score'),(24,'Can view score',6,'view_score'),(25,'Can add report',7,'add_report'),(26,'Can change report',7,'change_report'),(27,'Can delete report',7,'delete_report'),(28,'Can view report',7,'view_report'),(29,'Can add pred pmid',8,'add_predpmid'),(30,'Can change pred pmid',8,'change_predpmid'),(31,'Can delete pred pmid',8,'delete_predpmid'),(32,'Can view pred pmid',8,'view_predpmid'),(33,'Can add history',9,'add_history'),(34,'Can change history',9,'change_history'),(35,'Can delete history',9,'delete_history'),(36,'Can view history',9,'view_history'),(37,'Can add cancer hotspot',10,'add_cancerhotspot'),(38,'Can change cancer hotspot',10,'change_cancerhotspot'),(39,'Can delete cancer hotspot',10,'delete_cancerhotspot'),(40,'Can view cancer hotspot',10,'view_cancerhotspot'),(41,'Can add user',11,'add_user'),(42,'Can change user',11,'change_user'),(43,'Can delete user',11,'delete_user'),(44,'Can view user',11,'view_user'),(45,'Can add log entry',12,'add_logentry'),(46,'Can change log entry',12,'change_logentry'),(47,'Can delete log entry',12,'delete_logentry'),(48,'Can view log entry',12,'view_logentry'),(49,'Can add permission',13,'add_permission'),(50,'Can change permission',13,'change_permission'),(51,'Can delete permission',13,'delete_permission'),(52,'Can view permission',13,'view_permission'),(53,'Can add group',14,'add_group'),(54,'Can change group',14,'change_group'),(55,'Can delete group',14,'delete_group'),(56,'Can view group',14,'view_group'),(57,'Can add content type',15,'add_contenttype'),(58,'Can change content type',15,'change_contenttype'),(59,'Can delete content type',15,'delete_contenttype'),(60,'Can view content type',15,'view_contenttype'),(61,'Can add session',16,'add_session'),(62,'Can change session',16,'change_session'),(63,'Can delete session',16,'delete_session'),(64,'Can view session',16,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (11,'accounts','user'),(12,'admin','logentry'),(10,'api','cancerhotspot'),(1,'api','disease'),(2,'api','evidence'),(3,'api','gene'),(9,'api','history'),(8,'api','predpmid'),(7,'api','report'),(6,'api','score'),(4,'api','variant'),(5,'api','variantfield'),(14,'auth','group'),(13,'auth','permission'),(15,'contenttypes','contenttype'),(16,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-06-03 12:49:09.123890'),(2,'contenttypes','0002_remove_content_type_name','2021-06-03 12:49:09.225865'),(3,'auth','0001_initial','2021-06-03 12:49:09.558889'),(4,'auth','0002_alter_permission_name_max_length','2021-06-03 12:49:09.628858'),(5,'auth','0003_alter_user_email_max_length','2021-06-03 12:49:09.636856'),(6,'auth','0004_alter_user_username_opts','2021-06-03 12:49:09.643854'),(7,'auth','0005_alter_user_last_login_null','2021-06-03 12:49:09.651889'),(8,'auth','0006_require_contenttypes_0002','2021-06-03 12:49:09.654857'),(9,'auth','0007_alter_validators_add_error_messages','2021-06-03 12:49:09.661857'),(10,'auth','0008_alter_user_username_max_length','2021-06-03 12:49:09.693888'),(11,'auth','0009_alter_user_last_name_max_length','2021-06-03 12:49:09.702869'),(12,'auth','0010_alter_group_name_max_length','2021-06-03 12:49:09.720858'),(13,'auth','0011_update_proxy_permissions','2021-06-03 12:49:09.728870'),(14,'auth','0012_alter_user_first_name_max_length','2021-06-03 12:49:09.735857'),(15,'accounts','0001_initial','2021-06-03 12:49:10.893106'),(16,'admin','0001_initial','2021-06-03 12:49:11.152104'),(17,'admin','0002_logentry_remove_auto_add','2021-06-03 12:49:11.163105'),(18,'admin','0003_logentry_add_action_flag_choices','2021-06-03 12:49:11.178105'),(19,'api','0001_initial','2021-06-03 12:49:12.857101'),(20,'sessions','0001_initial','2021-06-03 12:49:12.909103');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-03 22:58:20
