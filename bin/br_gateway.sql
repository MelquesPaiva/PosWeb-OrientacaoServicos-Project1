CREATE DATABASE IF NOT EXISTS gateway;

use gateway;

CREATE TABLE IF NOT EXISTS `payments`(
    `id` INT (11) PRIMARY KEY AUTO_INCREMENT,
    `status` ENUM("pending", "confirmed", "cancelled") NOT NULL,
    `amount` float NOT NULL,
    `customer_email` VARCHAR(255) NOT NULL,
    `customer_name` VARCHAR(255),
    `created_at` DATETIME NOT NULL,
    `confirmed_at` DATETIME,
    `cancelled_at` DATETIME
) Engine=InnoDB CHARACTER SET utf8;

CREATE TABLE IF NOT EXISTS `refunds`(
    `id` INT (11) PRIMARY KEY AUTO_INCREMENT,
    `amount`float NOT NULL,
    `payment_id` INT (11) NOT NULL,
    `created_at` DATETIME NOT NULL
) Engine=InnoDB CHARACTER SET utf8;

ALTER TABLE `refunds` INDEX `fk_refunds__payments` FOREIGN KEY (`payment_id`) REFERENCES `payments` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;
