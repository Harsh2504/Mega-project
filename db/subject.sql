-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 17, 2023 at 09:45 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `systemdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `subject`
--

CREATE TABLE `subject` (
  `id` int(11) NOT NULL,
  `dept_id` int(11) NOT NULL,
  `cd_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `name_s` varchar(15) NOT NULL,
  `sem` int(11) NOT NULL,
  `sub_code` int(11) NOT NULL,
  `th` varchar(10) NOT NULL,
  `pr` varchar(10) NOT NULL,
  `tu` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `subject`
--

INSERT INTO `subject` (`id`, `dept_id`, `cd_id`, `name`, `name_s`, `sem`, `sub_code`, `th`, `pr`, `tu`) VALUES
(72, 4, 5, 'Digital Techniques', 'DTE', 3, 22320, 'y', 'y', 'n'),
(73, 4, 5, 'Applied Electronics', 'AEL', 3, 22329, 'y', 'y', 'n'),
(74, 4, 5, 'Electric circuit & Networks', 'ECN', 3, 22330, 'y', 'y', 'y'),
(75, 4, 5, 'Electronic Measurements & Instrumentation', 'EMI', 3, 22333, 'y', 'y', 'n'),
(76, 4, 5, 'Principles of Electronic Communication', 'PEC', 3, 22334, 'y', 'y', 'n'),
(77, 4, 6, 'Environmental Studies', 'EST', 5, 22447, 'y', 'n', 'n'),
(78, 4, 6, 'Microwave and RADAR', 'MAR', 5, 22535, 'y', 'y', 'n'),
(79, 4, 6, 'Control System and PLC', 'CSP', 5, 22531, 'y', 'y', 'n'),
(80, 4, 6, 'Mobile and wireless Communication', 'MWC', 5, 22533, 'y', 'y', 'n'),
(81, 4, 6, 'Embedded Systems', 'ESY', 5, 22532, 'y', 'y', 'n'),
(82, 4, 6, 'Capstone Project Planning', 'CPP', 5, 22058, 'n', 'y', 'n'),
(83, 5, 5, 'ELECTRICAL CIRCUITS', 'ECI', 3, 22324, 'y', 'y', 'y'),
(84, 5, 5, 'ELECTRICAL & ELECTRONICS MEASUREMENT', 'EEM', 3, 22325, 'y', 'y', 'n'),
(85, 5, 5, 'FUNDAMENTAL OF POWER ELECTRONICS', 'FPE', 3, 22326, 'y', 'y', 'n'),
(86, 5, 5, 'ELECTRICAL POWER GENERATION', 'EPG', 3, 22327, 'y', 'y', 'n'),
(87, 5, 5, 'ELECTRICAL MATERIALS & WIRING PRACTICES', 'EMW', 3, 22328, 'y', 'y', 'n'),
(88, 5, 6, 'MANAGEMENT', 'MAN', 5, 22509, 'y', 'n', 'n'),
(89, 5, 6, 'INDUSTRIAL AC MACHINE', 'IAM', 5, 22523, 'y', 'y', 'n'),
(90, 5, 6, 'SWITHGEAR & PROTECTION', 'SAP', 5, 22524, 'y', 'y', 'n'),
(91, 5, 6, 'ENERGY CONSERVATION & AUDIT', 'ECA', 5, 22525, 'y', 'y', 'n'),
(92, 5, 6, 'ILLUMINATION & ELECTRIFICATION OF BUILDINGS', 'IEB', 5, 22530, 'y', 'y', 'n'),
(93, 5, 6, 'ENTERPRENURESHIP DEVELOPMENT', 'EDE', 5, 22032, 'y', 'y', 'n'),
(94, 5, 6, 'CAPSTONE PROJECT PLANING', 'CPP', 5, 22058, 'n', 'y', 'n'),
(95, 2, 5, 'OBJECT ORIENTED PROGRAMMING USING C++', 'OOP', 3, 22316, 'y', 'y', 'y'),
(96, 2, 5, 'DATA STRUCTURES USING C', 'DSU', 3, 22317, 'y', 'y', 'n'),
(97, 2, 5, 'COMPUTER GRAPHICS', 'CGR', 3, 22318, 'y', 'y', 'n'),
(98, 2, 5, 'DATABASE MANAGEMENT SYSTEM', 'DMS', 3, 22319, 'y', 'y', 'y'),
(99, 2, 5, 'DIGITAL TECHNIQUES', 'DTE', 3, 22320, 'y', 'y', 'n'),
(100, 2, 6, 'ENVIRONMNETAL STUDIES', 'EST', 5, 22447, 'y', 'n', 'n'),
(101, 2, 6, 'OPERATING SYSTEMS', 'OSY', 5, 22516, 'y', 'y', 'n'),
(102, 2, 6, 'ADVANCE JAVA PROGRAMMING', 'AJP', 5, 22517, 'y', 'y', 'n'),
(103, 2, 6, 'SOFTWARE TESTING', 'STE', 5, 22518, 'y', 'y', 'n'),
(104, 2, 6, 'CLIENT SIDE SCRIPTING LANGUAGE', 'CSS', 5, 22519, 'y', 'y', 'n'),
(105, 6, 5, 'STRENGTH OF MATERIALS', 'SOM', 3, 22306, 'y', 'y', 'y'),
(106, 6, 5, 'BASIC ELECTRICAL & ELECTRONICS ENGINEERING', 'BEE', 3, 22310, 'y', 'y', 'n'),
(107, 6, 5, 'THERMAL ENGINEERING', 'TEN', 3, 22337, 'y', 'y', 'n'),
(108, 6, 5, 'MECHANICAL WORKING DRAWING', 'MWM', 3, 22341, 'y', 'y', 'n'),
(109, 6, 5, 'ENGINEERING METROLOGY', 'EME', 3, 22342, 'y', 'y', 'n'),
(110, 6, 5, 'MECHANICAL ENGINEERING MATERIAL', 'MEM', 3, 22343, 'y', 'y', 'n'),
(111, 6, 6, 'MANAGEMENT', 'MAN', 4, 22509, 'y', 'n', 'n'),
(112, 6, 6, 'POWER ENGINEERING AND REFRIGERATION', 'PER', 4, 22562, 'y', 'y', 'n'),
(113, 6, 6, 'ADVANCED MANUFACTURING PROCESSES', 'AMP', 4, 22563, 'y', 'y', 'n'),
(114, 6, 6, 'ELEMENTS OF MACHINE DESIGN', 'EMD', 4, 22564, 'y', 'y', 'n'),
(115, 6, 6, 'POWER PLANT ENGINEERING', 'PPE', 4, 22566, 'y', 'y', 'n'),
(116, 6, 6, 'SOLID MODELING AND ADDITIVE MANUFACTURING', 'SMA', 4, 22053, 'n', 'y', 'n'),
(117, 6, 6, 'CAPSTONE PROJECT PLANNING', 'CPP', 4, 22050, 'n', 'y', 'n'),
(118, 3, 5, 'ADVANCED SURVEYING', 'ASU', 3, 22301, 'y', 'y', 'n'),
(119, 3, 5, 'HIGHWAY ENGINEERING', 'HEN', 3, 22302, 'y', 'y', 'n'),
(120, 3, 5, 'MATERIALS OF STRUCTURE', 'MOS', 3, 22303, 'y', 'y', 'y'),
(121, 3, 5, 'BUILDING CONSTRUCTION ', 'BCO', 3, 22304, 'y', 'y', 'n'),
(122, 3, 5, 'CONCRETE TECHNOLOGY', 'CTE', 3, 22305, 'y', 'y', 'n'),
(123, 3, 5, 'COMPUTER AIDED DRAWING', 'CAD', 3, 22022, 'n', 'y', 'n'),
(124, 3, 6, 'WATER RESOURSE ENGINEERING', 'WRE', 4, 22501, 'y', 'y', 'n'),
(125, 3, 6, 'DESIGN OF STEEL & RCC STRUCTURE', 'DSR', 4, 22502, 'y', 'y', 'y'),
(126, 3, 6, 'ESTIMATING & COSTING', 'EAC', 4, 22503, 'y', 'y', 'n'),
(127, 3, 6, 'PUBLIC HEALTH ENGINERING', 'PHE', 4, 22504, 'y', 'y', 'n'),
(128, 3, 6, 'RURAL DEVELOPMENT', 'RDE', 4, 22505, 'y', 'y', 'n'),
(129, 3, 6, 'CAPSTONE PROJECT PLANNING', 'CPP', 4, 22058, 'n', 'y', 'n'),
(130, 3, 5, 'MECHANICS OF STRUCTURE', 'MOS', 3, 22303, 'y', 'y', 'y'),
(131, 1, 4, 'ENGLISH', 'ENG', 1, 22101, 'y', 'y', 'n'),
(132, 1, 4, 'BASIC PHYSICS', 'PHY', 1, 22102, 'y', 'y', 'n'),
(133, 1, 4, 'BASIC CHEMISTRY ', 'CHE', 1, 22102, 'y', 'y', 'n'),
(134, 1, 4, 'BASIC MATHEMATICS', 'BMS', 1, 22103, 'y', 'n', 'y'),
(135, 1, 4, 'FUNDAMENTALS OF ICT', 'ICT', 1, 22001, 'y', 'y', 'n'),
(136, 1, 4, 'ENGINEERING GRAPHICS ', 'EGM', 1, 22002, 'y', 'y', 'n'),
(137, 1, 4, 'ENGINEERING GRAPHICS', 'EGE', 1, 22003, 'y', 'y', 'n');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `subject`
--
ALTER TABLE `subject`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dept_id` (`dept_id`),
  ADD KEY `cd_id` (`cd_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `subject`
--
ALTER TABLE `subject`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=138;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `subject`
--
ALTER TABLE `subject`
  ADD CONSTRAINT `subject_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `department` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `subject_ibfk_2` FOREIGN KEY (`cd_id`) REFERENCES `class` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
