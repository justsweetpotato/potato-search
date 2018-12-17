#!/usr/bin/env python
from random import choice

def Word():
    word_list = [
        "人人生而平等", "站在巨人的肩膀上", "一种东西发生蜕变并挣脱束缚, 原先的形体必将立即死亡",
        "未经反思自省的人生没有意义", "耐心是一切聪明才智的基础", "不知道自己的无知，乃是双倍的无知",
        "孩子怕黑暗情有可原，人生真正的悲剧是成人怕光明", "和一个人玩一个小时对他的了解,胜过于一年的对谈",
        "The measure of a man is what he does with power.", "任何问题都有两个方面"
    ]
    msg = choice(word_list)
    return msg


if __name__ == '__main__':
    print(Word())
