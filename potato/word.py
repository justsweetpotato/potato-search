#!/usr/bin/env python
from random import choice


def word():
    word_list = [
        "人人生而平等",
        "站在巨人的肩膀上",
        "耐心是一切聪明才智的基础",
        "The measure of a man is what he does with power."
    ]
    msg = choice(word_list)
    return msg


if __name__ == '__main__':
    print(word())
