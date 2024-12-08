-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 08, 2024 at 11:01 AM
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
(5, 600, 5, 1e65, 76471542014400, 637262850120),
(6, 5, 2, 120, 20, 10),
(7, 8, 4, 40320, 1680, 70),
(8, 10, 2, 3628800, 90, 45),
(9, 3, 2, 6, 6, 3);

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
(16, 32, 10, 4, 0.3125, 0.6875, 2.5, 0.4375, 0.0390625),
(17, 10, 5, 4, 0.5, 0.5, 1.25, 0.9, 0.2),
(18, 30, 15, 5, 0.5, 0.5, 3, 0.6666666666666666, 0.08333333333333333),
(19, 26, 10, 8, 0.38461538461538464, 0.6153846153846154, 1.25, 0.6923076923076923, 0.1183431952662722),
(20, 80, 80, 8, 1, 0, 10, 1.1, 0.1),
(21, 100, 80, 0, 0.8, 0.19999999999999996, 0, 0.8, 0),
(22, 6, 1, 0, 0.16666666666666666, 0.8333333333333334, 0, 0.16666666666666666, 0);

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
  MODIFY `Comb_HistoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `probability_history`
--
ALTER TABLE `probability_history`
  MODIFY `Prob_HistoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
