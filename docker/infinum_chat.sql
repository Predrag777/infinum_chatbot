-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 22, 2025 at 02:26 PM
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
-- Database: `infinum_chat`
--

-- --------------------------------------------------------

--
-- Table structure for table `chat`
--

CREATE TABLE `chat` (
  `id` int(11) NOT NULL,
  `title` varchar(224) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chat`
--

INSERT INTO `chat` (`id`, `title`) VALUES
(1, 'Chat1'),
(2, 'Chat1'),
(3, 'Chat70'),
(4, 'Chat36'),
(5, 'Chat77');

-- --------------------------------------------------------

--
-- Table structure for table `prompt`
--

CREATE TABLE `prompt` (
  `id` int(11) NOT NULL,
  `question` varchar(225) NOT NULL,
  `answer` varchar(225) NOT NULL,
  `chat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prompt`
--

INSERT INTO `prompt` (`id`, `question`, `answer`, `chat`) VALUES
(1, 'Pitanje 1', 'Odgovor 1', 1),
(2, 'Pitanje 2', 'Odgovor 2', 1),
(3, 'Question 1', 'Answer 1', 2),
(4, 'Question 2', 'Answer 2', 2),
(5, 'You: proba', 'JurisMind: It seems like you\'ve made a typo in your message, can you please provide more details so I can assist you better?', 3),
(6, 'You: proba', 'JurisMind: Perhaps there was a typo in your question. Can you please provide more details or clarify your question so I can give you the best possible legal advice?', 3),
(7, 'You: Probba', 'JurisMind: It seems like you might have made a typo. Could you please provide more context or clarify your question? I\'d be happy to help with any legal advice you need.', 5),
(8, 'You: Proba', 'JurisMind: I\'m assuming you need some sort of legal advice or information. Could you please provide more context or detail so I can better assist you?', 5),
(9, 'You: Proba', 'JurisMind: It appears that your message was cut off. What legal advice do you need help with? Please provide enough details so I can offer relevant guidance.', 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `chat`
--
ALTER TABLE `chat`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `prompt`
--
ALTER TABLE `prompt`
  ADD PRIMARY KEY (`id`),
  ADD KEY `chat` (`chat`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `chat`
--
ALTER TABLE `chat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `prompt`
--
ALTER TABLE `prompt`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `prompt`
--
ALTER TABLE `prompt`
  ADD CONSTRAINT `chat` FOREIGN KEY (`chat`) REFERENCES `chat` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
