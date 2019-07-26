#!/usr/bin/env python
# 处理数据

import requests
import re
from lxml import etree

# 总页数
PAGES = 3

# API KEY (100次/日)
KEY_LIST = [
    "AIzaSyDti_06GjeOV6trMz0ixATpXC6pTuJhAt4",
    "AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0",
]


def requests_to_google(request):
    '''向 Google API 发送请求, 并返回数据'''
    # https://www.googleapis.com/customsearch/v1?
    # q=python&cx=007606540339251262492:fq_p2g_s5pa&num=10&start=1&
    # key=AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0

    client_msg = request.GET.get('q')  # 获取查询字符
    page = request.GET.get('page', 1)  # 获取页码
    location = request.GET.get('location', 'off')  # 地理位置开关
    ip = None
    address = None

    if location == 'on':
        ip = get_client_ip(request)  # 获取用户 IP
        address = get_ip_address(ip)  # 获取用户地理位置

    for key in KEY_LIST:
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
                content['page'] = int(page)
                content['pages'] = list(range(1, PAGES + 1))
                content['ip'] = ip
                content['address'] = address
                content['location'] = location
                content['title'], content['text'] = requests_to_wikipedia(client_msg)
                return content

    # 所有请求均失败, 返回 403
    return 403


def requests_to_wikipedia(client_msg):
    '''向维基百科查询词条信息'''  # TODO: 需要改进逻辑

    url = "https://zh.wikipedia.org/zh-cn/{}".format(client_msg)
    response = requests.get(url)
    text = response.content.decode('utf-8')
    html = etree.HTML(text)

    try:
        content_exist_text = html.xpath('//*[@id="mw-content-text"]/div/p[1]/text()')[0].strip()  # 获取 p[1] 文本
    except:
        title, content = None, None
        return title, content

    if content_exist_text:  # 如果存在 p[1] 的文本
        content = html.xpath('//*[@id="mw-content-text"]/div/p[1]')[0].xpath('string(.)')  # 获取文本
        content_exist_list = re.match('.+? 可以指：', content)  # 词条存在多义
        content_exist_info = re.match('.*?为准。', content.strip())  # 获取说明信息
        if content_exist_info:  # 如果 p[1] 为说明信息
            content = html.xpath('//*[@id="mw-content-text"]/div/p[2]')[0].xpath('string(.)')  # 获取 p[2]
    else:
        content_exist_list = None  # 词条不存在多义
        content = html.xpath('//*[@id="mw-content-text"]/div/p[2]')[0].xpath('string(.)')  # 获取 p[2] 文本

    if content_exist_list:  # 如果词条存在多义
        title, content = None, None
    else:
        title = html.xpath('//*[@id="firstHeading"]/text()')[0]  # 获取标题
        content = re.sub('(\[.+?\]|（.*?）)', '', content)  # 将文本中的 [] 与 () 舍弃

    return title, content


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
        ip = request.META.get('REMOTE_ADDR', "")  # 在本地测试环境获取 Client IP

    return ip


def get_ip_address(ip):
    '''获取用户地理位置'''

    url = "https://freeapi.ipip.net/{0}".format(ip)  # 获取地理位置
    res = requests.get(url).json()
    address = res[0] + ' ' + res[1] + ' ' + res[2] + ' ' + res[4]

    return address


def get_api_data(q, page, key):
    '''直接返回 Google API 接口的结果'''

    if key == None:
        key = KEY_LIST[0]

    url = "https://www.googleapis.com/customsearch/v1?" \
          "q={0}&cx=007606540339251262492:fq_p2g_s5pa&num=10&start={1}&" \
          "key={2}".format(q, page, key)

    with requests.get(url) as r:
        server_msg = r.text
        return server_msg
