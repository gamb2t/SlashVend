/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for slashvend
DROP DATABASE IF EXISTS `slashvend`;
CREATE DATABASE IF NOT EXISTS `slashvend` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `slashvend`;

-- Dumping structure for table slashvend.culture
DROP TABLE IF EXISTS `culture`;
CREATE TABLE IF NOT EXISTS `culture` (
  `guild_id` text DEFAULT NULL,
  `token` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table slashvend.panel
DROP TABLE IF EXISTS `panel`;
CREATE TABLE IF NOT EXISTS `panel` (
  `guild_id` text DEFAULT NULL,
  `password` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table slashvend.product
DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `guild_id` text DEFAULT NULL,
  `id` text DEFAULT NULL,
  `name` text DEFAULT NULL,
  `price` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table slashvend.raw
DROP TABLE IF EXISTS `raw`;
CREATE TABLE IF NOT EXISTS `raw` (
  `id` text DEFAULT NULL,
  `value` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table slashvend.role
DROP TABLE IF EXISTS `role`;
CREATE TABLE IF NOT EXISTS `role` (
  `guild_id` text DEFAULT NULL,
  `value` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table slashvend.stock
DROP TABLE IF EXISTS `stock`;
CREATE TABLE IF NOT EXISTS `stock` (
  `guild_id` text DEFAULT NULL,
  `product_id` text DEFAULT NULL,
  `value` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table slashvend.users
DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `guild_id` text DEFAULT NULL,
  `user_id` text DEFAULT NULL,
  `amount` text DEFAULT '0',
  `rank` text DEFAULT 'Normal',
  `ban` text DEFAULT 'false'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table slashvend.webhook
DROP TABLE IF EXISTS `webhook`;
CREATE TABLE IF NOT EXISTS `webhook` (
  `guild_id` text DEFAULT NULL,
  `purlog` text DEFAULT NULL,
  `admlog` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
