USE book_db;

CREATE TABLE `search_history` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL COMMENT '由 Django ForeignKey(user_info) 生成',
    `username` VARCHAR(20) DEFAULT NULL COMMENT '存储冗余用户名',
    `browse_books` VARCHAR(255) NOT NULL,
    `search_time` DATETIME(6) NOT NULL,
    -- 建立物理外键关联到 user_info 的 id
    CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;