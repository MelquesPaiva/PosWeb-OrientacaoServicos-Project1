CREATE DATABASE IF NOT EXISTS payment_processor;

use payment_processor;

CREATE TABLE IF NOT EXISTS `payments` (
    `id` INT (11) PRIMARY KEY AUTO_INCREMENT,
    `status` ENUM("pe", "co", "ca") NOT NULL,
    `amount` float NOT NULL,
    `customer_email` VARCHAR(255) NOT NULL,
    `customer_name` VARCHAR(255),
    `country_abbr` VARCHAR (2),
    `currency_code` VARCHAR (3),
    `created_at` DATETIME NOT NULL,
    `confirmed_at` DATETIME,
    `cancelled_at` DATETIME
) Engine=InnoDB CHARACTER SET utf8;
