--sys
--fans id 表
create table bilibili_userfans(
id number(20) PRIMARY KEY,
userid number(20),
username varchar2(50),
fansnumber number(20),
fansuserid varchar2(4000)
);
comment on table bilibili_userfans is '粉丝id表';
comment on column bilibili_userfans.id is '主键';
comment on column bilibili_userfans.userid is '用户id';
comment on column bilibili_userfans.username is '用户名';
comment on column bilibili_userfans.fansnumber is '粉丝数量';
comment on column bilibili_userfans.fansuserid is '粉丝id';

--粉丝id表自增序列
create sequence userfans_seq increment by 1 start with 1
minvalue 1 maxvalue 9999999999999 nocache
order;

