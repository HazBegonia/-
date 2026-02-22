USE book_db;

CREATE TABLE IF NOT EXISTS `book_collection` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username_id` INT NOT NULL COMMENT '指向 user_info 的 ID',
    `book_upc` VARCHAR(50) NOT NULL COMMENT '书名编号',
    `book_name` VARCHAR(50) NOT NULL COMMENT '书名',
    `collect_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT `fk_book_collection_user` FOREIGN KEY (`username_id`) REFERENCES `user_info` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;