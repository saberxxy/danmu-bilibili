--sys
create tablespace bilibili
datafile 'G:/app/datafile/bilibili.dbf' size 100M 
autoextend on;

create user bilibili identified by 123456
default tablespace bilibili

grant dba to bilibili;
grant connect to bilibili;
grant resource to bilibili;
grant create table to bilibili;

--bilibili
--弹幕表
CREATE TABLE bilibili_danmu (
	id number(20) primary key,
	av_id number(12),
	av_title VARCHAR2(1000),
	color VARCHAR2(100),
	post_time DATE,
	show_time number(20),
	font_size number(10),
	locate number(11),
	direc number(10),
	style number(10),
	danmu_id number(15),
	content VARCHAR2(3000)
);
comment on table bilibili_danmu is '弹幕内容表';
comment on column bilibili_danmu.id is '主键';
comment on column bilibili_danmu.av_id is 'av号';
comment on column bilibili_danmu.av_title is 'av标题';
comment on column bilibili_danmu.color is '弹幕颜色';
comment on column bilibili_danmu.post_time is '弹幕发送时间';
comment on column bilibili_danmu.show_time is '弹幕显示时间';
comment on column bilibili_danmu.font_size is '字号';
comment on column bilibili_danmu.locate is '弹幕坐标';
comment on column bilibili_danmu.direc is '弹幕方向';
comment on column bilibili_danmu.style is '弹幕样式';
comment on column bilibili_danmu.danmu_id is '弹幕id';
comment on column bilibili_danmu.content is '弹幕内容';

--自增序列
create sequence danmu_seq increment by 1 start with 1 
minvalue 1 maxvalue 9999999999999 nocache 
order;


--用户信息表
create table bilibili_user
(id number(20) PRIMARY KEY,
userid number(20),
username varchar2(20),
regdate DATE,
birthday varchar2(10),
geo varchar2(50),
videonumber number(20, 2),
gznumber number(20, 2),
fansnumber number(20, 2),
bfnumber number(20, 2)
);
comment on table bilibili_user is '用户信息表';
comment on column bilibili_user.id is '主键';
comment on column bilibili_user.userid is '用户id';
comment on column bilibili_user.username is '用户名';
comment on column bilibili_user.regdate is '注册日期';
comment on column bilibili_user.birthday is '生日';
comment on column bilibili_user.geo is '地区';
comment on column bilibili_user.videonumber is '投稿视频数';
comment on column bilibili_user.gznumber is '关注数';
comment on column bilibili_user.fansnumber is '粉丝数';
comment on column bilibili_user.bfnumber is '播放数';

--自增序列
create sequence user_seq increment by 1 start with 1 
minvalue 1 maxvalue 9999999999999 nocache 
order;

