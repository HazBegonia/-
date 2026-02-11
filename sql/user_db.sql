use book_db;

create table if not exists `user_info` (
	`id` int auto_increment primary key,
    `user_name` varchar(20) not null unique comment '用户名',
	`password` varchar(255) not null comment '密码',
    `create_time` timestamp default current_timestamp comment '注册时间'
) engine = InnoDB default charset = utf8mb4, comment '用户信息表';