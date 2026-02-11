use book_db;

create table if not exists `book_info` (
	`id` int auto_increment primary key,
    `book_name` varchar(255) not null comment '书名',
    `price` decimal(10, 2) not null comment '价格',
	`subject` varchar(255) not null comment '类型',
    `stock` int default 0 comment '库存数量',
    `reviewers` int default 0 comment '评论数量',
    `UPC` varchar(50) not null comment '唯一标识码',
    `description` text comment '书籍简介',
    `rating` int default 0 comment '评分',
    `image` varchar(500) comment '图片URL地址',
    `created_at` timestamp default current_timestamp comment '抓取时间'
) engine = InnoDB default charset = utf8mb4, comment '书籍信息表';
