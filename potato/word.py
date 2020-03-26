#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 用于处理与文字相关的逻辑

from random import choice


def word(language):
    '''从文字列表中随机选择一条并返回'''

    word_list_zh_cn = [
        "站在巨人的肩膀上",
    ]

    word_list_en = [
        "Stand on the shoulders of giants",
    ]

    word_list_zh_tw = [
        "站在巨人的肩膀上",
    ]

    if language == 'en':
        msg = choice(word_list_en)
    elif language == 'zh-TW':
        msg = choice(word_list_zh_tw)
    else:
        msg = choice(word_list_zh_cn)

    return msg
