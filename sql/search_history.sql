use book_db;

create table if not exists `search_history` (
	`id` int auto_increment primary key,
    `user_name` varchar(20) not null comment '对应 user_info 表的 id',
	`browse_books` varchar(255) not null comment '用户浏览的书籍',
    `search_time` timestamp default current_timestamp comment '搜索时间',
    constraint `fk_user_history` foreign key (`user_name`) references `user_info` (`user_name`) on delete cascade
) engine = InnoDB default charset = utf8mb4 comment '用户搜索历史记录表';