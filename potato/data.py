#!/usr/bin/env python
# 处理数据

import requests


def requests_to_google(client_msg, page, ip):
    '''向 Google API 发送请求, 并返回数据'''
    # https://www.googleapis.com/customsearch/v1?
    # q=python&cx=007606540339251262492:fq_p2g_s5pa&num=10&start=1&
    # key=AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0

    # 总页数
    pages = 3

    # API KEY (100次/日)
    key_list = [
        "AIzaSyDti_06GjeOV6trMz0ixATpXC6pTuJhAt4",
        "AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0",
    ]

    for key in key_list:

        url = "https://www.googleapis.com/customsearch/v1?" \
              "q={0}&cx=007606540339251262492:fq_p2g_s5pa&num=10&start={1}&" \
              "key={2}".format(client_msg, page, key)

        # 使用 with 语句可以确保连接被关闭
        with requests.get(url) as r:
            # Google API 配额用尽时会返回 403 错误
            if r.status_code != 403:
                server_msg = r.json()  # 直接处理 json 返回 字典
                content = handle_data(server_msg)
                content['q'] = client_msg
                content['page'] = page
                content['pages'] = list(range(1, pages + 1))
                content['address'] = get_ip_address(ip)
                content['ip'] = ip
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


def get_client_ip(request):
    '''获取用户 IP'''

    ip = request.META.get("HTTP_X_FORWARDED_FOR", "")  # 在使用反向代理的服务器上获取 Client IP
    if not ip:
        ip = request.META.get('REMOTE_ADDR', "")

    return ip


def get_ip_address(ip):
    '''获取 IP 的地理位置'''

    url = "https://freeapi.ipip.net/{0}".format(ip)
    res = requests.get(url).json()
    ip_address = res[0] + ' ' + res[1] + ' ' + res[2] + ' ' + res[4]

    return ip_address


def get_api_data(q, page, key):
    '''直接返回 Google API 接口的结果'''

    if key == None:
        key = "AIzaSyDti_06GjeOV6trMz0ixATpXC6pTuJhAt4"

    url = "https://www.googleapis.com/customsearch/v1?" \
          "q={0}&cx=007606540339251262492:fq_p2g_s5pa&num=10&start={1}&" \
          "key={2}".format(q, page, key)

    with requests.get(url) as r:
        server_msg = r.text
        return server_msg
