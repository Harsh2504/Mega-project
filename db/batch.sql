-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 17, 2023 at 09:42 AM
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
-- Table structure for table `batch`
--

CREATE TABLE `batch` (
  `id` int(11) NOT NULL,
  `dept_id` int(11) NOT NULL,
  `cd_id` int(11) NOT NULL,
  `batch` varchar(20) NOT NULL,
  `div_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `batch`
--

INSERT INTO `batch` (`id`, `dept_id`, `cd_id`, `batch`, `div_id`) VALUES
(26, 1, 4, 'A1', 10),
(27, 1, 4, 'A2', 10),
(28, 1, 4, 'A3', 10),
(29, 4, 5, 'E1', 17),
(30, 4, 5, 'E2', 17),
(31, 4, 5, 'E3', 17),
(32, 4, 6, 'E1', 18),
(33, 5, 5, 'B1', 0),
(34, 5, 5, 'B2', 0),
(35, 5, 5, 'B3', 0),
(36, 5, 6, 'B1', 0),
(37, 2, 5, 'S1', 0),
(38, 2, 5, 'S2', 0),
(39, 2, 5, 'S3', 0),
(40, 2, 6, 'T1', 0),
(41, 2, 6, 'T2', 0),
(42, 2, 6, 'T3', 0),
(43, 1, 4, 'B1', 11),
(45, 1, 4, 'B2', 11),
(46, 1, 4, 'C1', 12),
(47, 1, 4, 'C2', 12),
(48, 1, 4, 'C3', 12),
(49, 1, 4, 'D1', 13),
(50, 1, 4, 'D2', 13),
(51, 1, 4, 'E1', 14),
(52, 1, 4, 'E2', 14),
(53, 1, 4, 'E3', 14),
(54, 1, 4, 'F1', 15),
(55, 1, 4, 'F2', 15),
(56, 1, 4, 'F3', 15),
(57, 1, 4, 'G1', 16),
(58, 1, 4, 'G2', 16),
(59, 1, 4, 'G3', 16),
(60, 6, 5, 'A1', 19),
(61, 6, 5, 'A2', 19),
(62, 6, 5, 'B1', 20),
(63, 6, 5, 'B2', 20),
(64, 6, 6, 'T1', 21),
(65, 6, 6, 'T2', 21),
(66, 3, 5, 'A1', 22),
(67, 3, 5, 'A2', 22),
(68, 3, 5, 'A3', 22),
(69, 3, 6, 'A1', 23),
(70, 3, 6, 'A2', 23);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `batch`
--
ALTER TABLE `batch`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dept_id` (`dept_id`),
  ADD KEY `cd_id` (`cd_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `batch`
--
ALTER TABLE `batch`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `batch`
--
ALTER TABLE `batch`
  ADD CONSTRAINT `batch_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `department` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `batch_ibfk_2` FOREIGN KEY (`cd_id`) REFERENCES `class` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
