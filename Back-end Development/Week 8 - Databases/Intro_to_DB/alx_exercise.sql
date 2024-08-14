-- Create the database 'alx_exercise'
CREATE DATABASE IF NOT EXISTS alx_exercise;

-- Use the 'alx_exercise' database
USE alx_exercise;

-- Table structure for table `Employee`
CREATE TABLE IF NOT EXISTS `Employee` (
  `EmployeeID` int NOT NULL UNIQUE,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `Department` varchar(50) NOT NULL,
  `HireDate` date DEFAULT NULL,
  PRIMARY KEY (`EmployeeID`)
);

-- Insert data into the `Employee` table
INSERT INTO `Employee` (`EmployeeID`, `FirstName`, `LastName`, `Department`, `HireDate`) VALUES
(1, 'Alvin', 'Zoro', 'IT', '2024-03-31'),
(2, 'RYAN', 'RURI', 'Marketer', '2024-08-14'),
(3, 'ASHLEY', 'WANJI', 'Influencer', '2024-06-12'),
(4, 'LIZ', 'KYLA', 'Manager', '2024-07-14'),
(5, 'FEZ', 'LYN', 'Accounts', '2024-01-01'),
(6, 'NEOM', 'MESS', 'Designer', '2024-04-01');

-- Table structure for table `Orders`

DROP TABLE IF EXISTS `Orders`;
CREATE TABLE `Orders` (
  `OrderID` int NOT NULL,
  `CustomerID` int DEFAULT NULL,
  `OrderDate` date DEFAULT NULL,
  `Total` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  FOREIGN KEY (`CustomerID`) REFERENCES `Students` (`StudentID`)
);

-- Insert data into the `Orders` table
INSERT INTO `Orders` (`OrderID`, `CustomerID`, `OrderDate`, `Total`) VALUES
(2, 2, '2024-08-01', 1500.00),
(3, 3, '2024-08-02', 9000.00);

-- Table structure for table Students
DROP TABLE IF EXISTS `Students`;

CREATE TABLE `Students` (
  `StudentID` int NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `EnrollmentDate` date DEFAULT NULL,
  PRIMARY KEY (`StudentID`),
  UNIQUE KEY `Email` (`Email`)
);

-- Insert data into the `Students` table
INSERT INTO `Students` (`StudentID`, `FirstName`, `LastName`, `Email`, `EnrollmentDate`) VALUES
(1, 'Liam', 'Njogu', 'liamnjogu@123', '2023-05-01'),
(2, 'Zari', 'Alma', 'almazari@123', '2023-09-01'),
(3, 'Lushan', 'Hassan', 'lushanhassan@123', '2023-01-01');