--建表SQL语句
CREATE TABLE `danmu` (
	`id` BIGINT(20) NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
	`av_id` INT(12) NULL COMMENT 'av号',
	`av_title` VARCHAR(1000) NULL DEFAULT '0' COMMENT 'av标题',
	`color` VARCHAR(100) NULL COMMENT '弹幕颜色',
	`post_time` DATETIME NULL COMMENT '弹幕发送时间',
	`show_time` FLOAT NULL COMMENT '弹幕显示时间',
	`font_size` INT(10) NULL COMMENT '字号',
	`locate` INT(11) NULL COMMENT '弹幕坐标',
	`direc` INT(10) NULL COMMENT '弹幕方向',
	`style` INT(10) NULL COMMENT '弹幕样式',
	`danmu_id` INT(15) NULL DEFAULT NULL COMMENT '弹幕id',
	`content` VARCHAR(5000) NULL COMMENT '弹幕内容',
	PRIMARY KEY (`id`)
)
COMMENT='全部弹幕内容'
DEFAULT CHARSET='utf8'
ENGINE=InnoDB


create table bilibili_user
(`id` BIGINT(20) NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
`uid` INT(20) NULL COMMENT '用户id',
`username` varchar(20) NULL COMMENT '用户名',
`regdate` datetime NULL COMMENT '注册日期',
`birthday` varchar(10) NULL COMMENT '生日',
`geo` varchar(20) NULL COMMENT '地区',
`videonumber` FLOAT NULL COMMENT '投稿视频数',
`gznumber` FLOAT NULL COMMENT '关注数',
`fansnumber` FLOAT NULL COMMENT '粉丝数',
`bfnumber` FLOAT NULL COMMENT '播放数'
)
COMMENT='用户信息'
DEFAULT CHARSET='utf8'
ENGINE=InnoDB
