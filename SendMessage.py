#-*- coding=utf-8 -*-
# 采集数据到一定程度自动推送消息

from wxpy import *

def sendMessage(replay_user, replay_content):
    bot = Bot(cache_path=True)  #设置登录缓存，不必每次运行都扫码

    # replay_user = u'Clannad'  # 在这里写要回复的人
    # replay_content = u''  # 在这里写要回复的内容
    my_friend = ensure_one(bot.search(replay_user))
    my_friend.send(replay_content)

def main():
    pass


if __name__=='__main__':
    main()