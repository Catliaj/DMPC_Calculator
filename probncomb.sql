-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 07, 2024 at 02:48 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `probncomb`
--

-- --------------------------------------------------------

--
-- Table structure for table `combinatronics_history`
--

CREATE TABLE `combinatronics_history` (
  `Comb_HistoryID` int(11) NOT NULL,
  `(n)` int(11) DEFAULT NULL,
  `(r)` int(11) DEFAULT NULL,
  `Factorial_R` double DEFAULT NULL,
  `Permutation_R` double DEFAULT NULL,
  `Combination_R` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `combinatronics_history`
--

INSERT INTO `combinatronics_history` (`Comb_HistoryID`, `(n)`, `(r)`, `Factorial_R`, `Permutation_R`, `Combination_R`) VALUES
(1, 12, 5, 69, 44, 80),
(2, 12, 3, 32, 56, 71),
(3, 12, 10, 23, 12, 19);

-- --------------------------------------------------------

--
-- Table structure for table `probability_history`
--

CREATE TABLE `probability_history` (
  `Prob_HistoryID` int(11) NOT NULL,
  `n(S)` int(11) DEFAULT NULL,
  `n(A)` int(11) DEFAULT NULL,
  `n(B)` int(11) DEFAULT NULL,
  `Simple_P` double DEFAULT NULL,
  `Complementary_P` double DEFAULT NULL,
  `Conditional_P` double DEFAULT NULL,
  `Addition_R` double DEFAULT NULL,
  `Multiplication_R` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `probability_history`
--

INSERT INTO `probability_history` (`Prob_HistoryID`, `n(S)`, `n(A)`, `n(B)`, `Simple_P`, `Complementary_P`, `Conditional_P`, `Addition_R`, `Multiplication_R`) VALUES
(1, 12, 45, 9, 404, 404, 404, 404, 404),
(2, 23, 14, 69, 404, 404, 404, 404, 404),
(3, 13, 3, 5, 69, 69, 69, 69, 69);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `combinatronics_history`
--
ALTER TABLE `combinatronics_history`
  ADD PRIMARY KEY (`Comb_HistoryID`);

--
-- Indexes for table `probability_history`
--
ALTER TABLE `probability_history`
  ADD PRIMARY KEY (`Prob_HistoryID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `combinatronics_history`
--
ALTER TABLE `combinatronics_history`
  MODIFY `Comb_HistoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `probability_history`
--
ALTER TABLE `probability_history`
  MODIFY `Prob_HistoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
