-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 17, 2023 at 09:44 AM
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
-- Table structure for table `que`
--

CREATE TABLE `que` (
  `id` int(11) NOT NULL,
  `ques` varchar(100) NOT NULL,
  `o1` varchar(50) NOT NULL,
  `o2` varchar(50) NOT NULL,
  `o3` varchar(50) NOT NULL,
  `o4` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `que`
--

INSERT INTO `que` (`id`, `ques`, `o1`, `o2`, `o3`, `o4`) VALUES
(1, 'Has the teacher been punctual (regular) to the classes during the semester?', 'Always on time', 'Most of the times', 'Some times', 'Never comes on time'),
(2, 'Do you feel the teacher has followed the lesson plan till this date in the semester?', 'Regularly', 'Frequently', 'Occasionally', 'Never'),
(3, 'Was the teacher always well prepared for the lecture?', 'Always', 'Most of the times', 'Only a few times', 'Never'),
(4, 'How did the teacher explain the subject?', 'Excellent', 'Good', 'Satisfactorily', 'Poor'),
(5, 'How much opportunity did the teacher give for questions & discussions?', 'All the time', 'Occasionally', 'Rarely', 'Never'),
(6, 'How was the continuity maintained from class to class while teaching the subject?', 'Excellent', 'Good', 'Satisfactorily', 'Poor'),
(7, 'Has the teacher motivated you to study the subject in depth?', 'Highly', 'Enough', 'Rarely', 'Never'),
(8, 'How was the language (Clarity of communication) of the teacher?', 'Excellent', 'Good', 'Satisfactory', 'Poor'),
(9, 'Comment on the teacherâ€™s control and command over the class?', 'Maintains good discipline by his/her presence', 'Some order in the class', 'Frequently class is disordered', 'Class is always noisy & disordered'),
(10, 'Has the teacher been helpful outside the classroom to clarify yours doubts?', 'Always', 'Most of the times', 'Only some times', 'Never');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `que`
--
ALTER TABLE `que`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `que`
--
ALTER TABLE `que`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
