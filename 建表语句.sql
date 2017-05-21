--建表SQL语句
CREATE TABLE `danmu` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
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