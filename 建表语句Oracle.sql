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


--所需的表
--弹幕表，用户信息表，视频信息表，评论表，用户投稿表，用户粉丝表，用户关注表


--bilibili
--弹幕表
CREATE TABLE bilibili_danmu (
	id number(20) primary key,
	av_id number(20),
	av_title VARCHAR2(1000),
	color VARCHAR2(100),
	post_time DATE,
	show_time number(20, 4),
	font_size number(20, 4),
	locate number(20, 4),
	direc number(20, 4),
	style number(20, 4),
	danmu_id number(20, 4),
	content VARCHAR2(4000)
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

--弹幕表自增序列
create sequence danmu_seq increment by 1 start with 1 
minvalue 1 maxvalue 9999999999999 nocache 
order;


--用户信息表
create table bilibili_user
(id number(20) PRIMARY KEY,
userid number(20),
username varchar2(20),
regtime DATE,
birthday DATE,
geo varchar2(50),
sex varchar2(4),
fansnumber number(20, 2),
gznumber number(20, 2),
bfnumber number(20, 2),
videonumber number(20, 2),
approve varchar2(5),
userlevel number(3),
sign varchar2(4000)
);
comment on table bilibili_user is '用户信息表';
comment on column bilibili_user.id is '主键';
comment on column bilibili_user.userid is '用户id';
comment on column bilibili_user.username is '用户名';
comment on column bilibili_user.regtime is '注册日期';
comment on column bilibili_user.birthday is '生日';
comment on column bilibili_user.geo is '地区';
comment on column bilibili_user.sex is '性别';
comment on column bilibili_user.fansnumber is '粉丝数';
comment on column bilibili_user.gznumber is '关注数';
comment on column bilibili_user.bfnumber is '播放数';
comment on column bilibili_user.videonumber is '投稿视频数';
comment on column bilibili_user.approve is '是否认证';
comment on column bilibili_user.userlevel is '用户等级';
comment on column bilibili_user.sign is '用户签名';


--用户信息表自增序列
create sequence user_seq increment by 1 start with 1 
minvalue 1 maxvalue 9999999999999 nocache 
order;


--视频信息表
--av号，up主userid，视频标题，发布时间，大分类，小分类，标签，
--视频描述，点击数，弹幕数，硬币数，收藏数，分享数，评论数，最高日排名
create table bilibili_video
(id number(20) PRIMARY KEY,
av_id number(12),
userid number(20),
av_title varchar2(1000),
uptime date,
bigtype varchar2(100),
smalltype varchar2(100),
tags varchar2(1000),
description varchar2(2000),
djnumber number(20, 2),
dmnumber number(20, 2),
coinnumber number(20, 2),
scnumber number(20, 2),
sharenumber number(20, 2),
commentnumber number(20, 2),
hisrank number(10)
);
comment on table bilibili_video is '视频信息表';
comment on column bilibili_video.id is '主键';
comment on column bilibili_video.av_id is 'av号';
comment on column bilibili_video.userid is 'up主userid';
comment on column bilibili_video.av_title is '视频标题';
comment on column bilibili_video.uptime is '发布时间';
comment on column bilibili_video.bigtype is '大分类';
comment on column bilibili_video.smalltype is '小分类';
comment on column bilibili_video.tags is '标签';
comment on column bilibili_video.description is '视频描述';
comment on column bilibili_video.djnumber is '点击数';
comment on column bilibili_video.dmnumber is '弹幕数';
comment on column bilibili_video.coinnumber is '硬币数';
comment on column bilibili_video.scnumber is '收藏数';
comment on column bilibili_video.sharenumber is '分享数';
comment on column bilibili_video.commentnumber is '评论数';
comment on column bilibili_video.hisrank is '最高日排名';


--视频信息表自增序列
create sequence video_seq increment by 1 start with 1 
minvalue 1 maxvalue 9999999999999 nocache 
order;


--评论表
create table bilibili_comment
(id number(20) PRIMARY KEY,
rpid number(20),
av_id number(12),
userid number(20),
username varchar2(20),
uptime date,
likenumber number(10),
floor number(10),
parent number(20), 
content varchar2(1000)
);
comment on table bilibili_comment is '评论表';
comment on column bilibili_comment.id is '主键';
comment on column bilibili_comment.rpid is '评论编号';
comment on column bilibili_comment.av_id is 'av号';
comment on column bilibili_comment.userid is '用户id';
comment on column bilibili_comment.username is '用户名';
comment on column bilibili_comment.uptime is '发布时间';
comment on column bilibili_comment.likenumber is '点赞数';
comment on column bilibili_comment.floor is '楼层';
comment on column bilibili_comment.parent is '父节点rpid';
comment on column bilibili_comment.content is '评论内容';

--自增序列
create sequence comment_seq increment by 1 start with 1 
minvalue 1 maxvalue 9999999999999 nocache 
order;


--粉丝表
create table bilibili_userfans
(id number(20) PRIMARY KEY,
userid number(20),
username varchar2(50),
fansnumber number(20),
fansuserid varchar2(4000));

comment on table bilibili_userfans is '粉丝表';
comment on column bilibili_userfans.id is '主键';
comment on column bilibili_userfans.userid is '用户id';
comment on column bilibili_userfans.username is '用户名';
comment on column bilibili_userfans.fansnumber is '粉丝数量';
comment on column bilibili_userfans.fansuserid is '粉丝用户id';

--自增序列
create sequence userfans_seq increment by 1 start with 1 
minvalue 1 maxvalue 9999999999999 nocache 
order;


--关注表
create table bilibili_usergz
(id number(20) PRIMARY KEY,
userid number(20),
username varchar2(50),
gznumber number(20),
gzsuserid varchar2(4000));

comment on table bilibili_usergz is '关注表';
comment on column bilibili_usergz.id is '主键';
comment on column bilibili_usergz.userid is '用户id';
comment on column bilibili_usergz.username is '用户名';
comment on column bilibili_usergz.gznumber is '关注数量';
comment on column bilibili_usergz.gzsuserid is '关注用户id';

--自增序列
create sequence usergz_seq increment by 1 start with 1 
minvalue 1 maxvalue 9999999999999 nocache 
order;
