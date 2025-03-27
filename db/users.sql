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
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `pre` varchar(10) NOT NULL,
  `name` varchar(30) NOT NULL,
  `dept_id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `number` varchar(10) NOT NULL,
  `password` varchar(50) NOT NULL DEFAULT 'SGP5001',
  `post` varchar(20) NOT NULL,
  `status` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `pre`, `name`, `dept_id`, `email`, `number`, `password`, `post`, `status`) VALUES
(4, 'Mr.', 'Naresh Kamble', 0, 'naresh.kamble@sgipolytechnic.in', '9890455842', '123456', 'Admin', 'active'),
(8, 'Mr.', 'Deepak Kamble', 4, 'deepak.kamble@sgipolytechnic.in', '9420584185', '9420584185', 'Sub-Admin', 'active'),
(9, 'Mr.', 'Vishal Teli', 6, 'vishal.teli@sgipolytechnic.in', '9766020784', '9766020784', 'Sub-Admin', 'active'),
(10, 'Mr.', 'Chandrasen Rajemahadik', 3, 'chandrasen.rajemahadik@sgipolytechnic.in', '9527116536', '9527116536', 'Sub-Admin', 'active'),
(11, 'Ms.', 'Manali Thorushe', 5, 'manali.thorushe@sgipolytechnic.in', '7843089631', '7843089631', 'Sub-Admin', 'active'),
(12, 'Mr.', 'XYZ', 2, 'xyz@gmail.com', '7028025842', '12345', 'Sub-Admin', 'active'),
(13, 'Ms.', 'Apurva Patil', 1, 'apurva.patil@sgipolytechnic.in', '8308989800', '8308989800', 'Sub-Admin', 'active'),
(14, 'Mr.', 'Harsh Patil ', 0, 'harsh2504patil@gmail.com', '7249236027', '123456', 'Admin', 'active');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `dept_id` (`dept_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
