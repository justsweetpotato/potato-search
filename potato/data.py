#!/usr/bin/env python
# 处理数据

import requests


def requests_to_google(client_msg):
    '''向 Google API 发送请求'''

    # 主要 API (100次/日)
    url1 = "https://www.googleapis.com/customsearch/v1?" \
           "q={}&cx=007606540339251262492:fq_p2g_s5pa&num=10&start=1&" \
           "key=AIzaSyDti_06GjeOV6trMz0ixATpXC6pTuJhAt4".format(client_msg)

    # 备用 API
    url2 = "https://www.googleapis.com/customsearch/v1?" \
           "q={}&cx=007606540339251262492:fq_p2g_s5pa&num=10&start=1&" \
           "key=AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0".format(client_msg)

    # 使用 with 语句可以确保连接被关闭
    with requests.get(url1) as r:
        # Google API 配额用尽时会返回 403 错误
        if r.status_code != 403:
            server_msg = r.json()  # 直接处理 json 返回 字典
            content = handle_data(server_msg)
            return content

    # url1 响应返回 403 则调用备用 API
    with requests.get(url2) as r:
        if r.status_code != 403:
            server_msg = r.json()
            content = handle_data(server_msg)
            return content

    return None


def handle_data(server_msg):
    '''提取 Google API 返回的数据(只需要 标题 and 连接 and 简介)'''

    title_list = []
    link_list = []
    snippet_list = []

    # 如果不存在 items 表示没有搜索结果
    if server_msg.get("items"):
        for data_dict in server_msg["items"]:
            title_list.append(data_dict["title"])
            link_list.append(data_dict["link"])
            snippet_list.append(data_dict["snippet"])

        data_tuple = zip(title_list, link_list, snippet_list)
        content = {"content": data_tuple}
    else:
        content = None

    return content
