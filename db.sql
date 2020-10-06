SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `resultats` (
  `IP` varchar(16) NOT NULL,
  `PORT` int(5) NOT NULL,
  `ETAT` varchar(20) NOT NULL,
  `SERVICE` varchar(20) NOT NULL,
  `RANGE_IP` varchar(40) NOT NULL,
  `DNS` varchar(100) NOT NULL,
  `URL_RIPE` varchar(10000) NOT NULL,
  `VERIFICATION` varchar(20) NOT NULL,
  `PAYS` varchar(30) NOT NULL,
  `VERSION` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `resultats`
  ADD PRIMARY KEY (`IP`,`PORT`);
COMMIT;