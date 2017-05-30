--sys
--fans id 表
create table bilibili_fansid(
id number(20) PRIMARY KEY,
userid number(20),
username varchar2(20),
fansnumber number(20, 2),
fansid varchar2(4000)
);
comment on table bilibili_fansid is '粉丝id表';
comment on column bilibili_fansid.id is '主键';
comment on column bilibili_fansid.userid is '用户id';
comment on column bilibili_fansid.username is '用户名';
comment on column bilibili_fansid.fansnumber is '粉丝数量';
comment on column bilibili_fansid.fansid is '粉丝id';

--粉丝id表自增序列
create sequence fansid_seq increment by 1 start with 1
minvalue 1 maxvalue 9999999999999 nocache
order;

