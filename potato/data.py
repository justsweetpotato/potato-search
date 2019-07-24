#!/usr/bin/env python
# 处理数据

import requests


def requests_to_google(client_msg, page):
    '''向 Google API 发送请求'''

    # 总页数
    pages = 3

    # 主要 API (100次/日)
    url1 = "https://www.googleapis.com/customsearch/v1?" \
           "q={0}&cx=007606540339251262492:fq_p2g_s5pa&num=10&start={1}&" \
           "key=AIzaSyDti_06GjeOV6trMz0ixATpXC6pTuJhAt4".format(client_msg, page)

    # 备用 API
    url2 = "https://www.googleapis.com/customsearch/v1?" \
           "q={0}&cx=007606540339251262492:fq_p2g_s5pa&num=10&start={1}&" \
           "key=AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0".format(client_msg, page)

    # 使用 with 语句可以确保连接被关闭
    with requests.get(url1) as r:
        # Google API 配额用尽时会返回 403 错误
        if r.status_code != 403:
            server_msg = r.json()  # 直接处理 json 返回 字典
            content = handle_data(server_msg)
            content['q'] = client_msg
            content['page'] = page
            content['pages'] = list(range(1, pages + 1))
            print(content['q'])
            print(content['page'])
            print(content['pages'])
            return content

    # url1 响应返回 403 则调用备用 API
    with requests.get(url2) as r:
        if r.status_code != 403:
            server_msg = r.json()
            content = handle_data(server_msg)
            content['q'] = client_msg
            content['page'] = page
            content['pages'] = list(range(1, pages + 1))
            return content

    # 所有请求均失败, 返回 403
    return 403


def handle_data(server_msg):
    '''提取 Google API 返回的数据(只需要 标题 and 连接 and 简介)'''

    title_list = []
    link_list = []
    snippet_list = []
    content = {}

    # 如果不存在 items 表示没有搜索结果
    if server_msg.get("items"):
        for data_dict in server_msg["items"]:
            title_list.append(data_dict["title"])
            link_list.append(data_dict["link"])
            snippet_list.append(data_dict["htmlSnippet"])

        data_tuple = zip(title_list, link_list, snippet_list)
        content = {"content": data_tuple}
        content["empty"] = False
    else:
        content["empty"] = True

    return content

# https://www.googleapis.com/customsearch/v1?q={}&cx=007606540339251262492:fq_p2g_s5pa&num=10&start=1&key=AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0
