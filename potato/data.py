#!/usr/bin/env python
# 处理数据

import requests
import re
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from lxml import etree

# 总页数
PAGES = 3

# API KEY (100次/日)
KEY_LIST = [
    "AIzaSyDti_06GjeOV6trMz0ixATpXC6pTuJhAt4",
    "AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0",
    'AIzaSyAdolxu5TWJhArM00hTqTUwOTDHK00806s'
]


def requests_to_google(request):
    '''向 Google API 发送请求, 并返回数据'''
    # https://www.googleapis.com/customsearch/v1?
    # q=python&cx=007606540339251262492:fq_p2g_s5pa&num=10&start=1&
    # key=AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0

    client_msg = request.GET.get('q')  # 获取查询字符
    page = int(request.GET.get('page', 1))  # 获取页码
    location = request.GET.get('location', 'off')  # 地理位置开关
    ip = None
    address = None
    title = None
    q_text = None

    if page == 1:
        title, q_text = requests_to_wikipedia(client_msg)  # 获取查询字符的简介

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
                content['page'] = page
                content['pages'] = list(range(1, PAGES + 1))
                content['ip'] = ip
                content['address'] = address
                content['location'] = location
                content['title'] = title
                content['text'] = q_text
                return content

    # 所有请求均失败, 返回 403
    return 403


def requests_to_wikipedia(client_msg):
    '''向维基百科查询词条信息'''

    url = "https://zh.wikipedia.org/zh-cn/{}".format(client_msg)
    response = requests.get(url)
    text = response.content.decode('utf-8')
    html = etree.HTML(text)
    content = None

    for i in range(1, 5):
        try:
            content_exist_text = html.xpath('//*[@id="mw-content-text"]/div/p[{0}]/text()'.format(i))[
                0].strip()  # 获取 p[?] 文本
        except:
            return None, None

        if content_exist_text:  # 如果存在 p[?] 的文本
            content = html.xpath('//*[@id="mw-content-text"]/div/p[{0}]'.format(i))[0].xpath('string(.)')  # 获取文本
            content_exist_info = re.match('.*?为准。', content.strip(), flags=re.S)  # 获取说明信息
            if content_exist_info:  # 如果 p[?] 为说明信息
                continue
            break
        else:
            continue

    if content:
        content_exist_list = re.match('.+?[ ，]?可[以能]是?[指是](下列物品)?：', content, flags=re.S)  # 词条存在多义吗
        if content_exist_list:  # 如果词条存在多义
            return None, None

        title = html.xpath('//*[@id="firstHeading"]/text()')[0]  # 获取标题
        content = re.sub('(\[.*?\]|（.*?）)', '', content, flags=re.S)  # 将文本中的 [] 与 () 舍弃
        return title, content
    return None, None


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

        data_zip = zip(title_list, link_list, snippet_list)
        content = {"content": data_zip}
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


def check_web(web):
    '''检查网站可用性 & 激活 herokuapp'''

    title_list = []
    url_list = []
    checked = []

    for title, url, _ in web:
        title_list.append(title)
        url_list.append(url)
        try:
            with requests.get(url) as r:
                if r.status_code == 200:
                    checked.append(1)
                else:
                    checked.append(0)
        except:
            checked.append(0)
    content = {'content': zip(title_list, url_list, checked)}

    return content


def error_403():
    '''获取 API 调用最大次数和重置时间'''

    api_request_count = len(KEY_LIST) * 100
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)  # UTC 时间
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))  # UTC+8 (北京时间)

    reset_time_hour = 15 - bj_dt.hour  # API 次数在北京时间 15时(太平洋时间 0时) 重置
    reset_time_hour += 24 if reset_time_hour < 0 else reset_time_hour
    reset_time_minute = 0 - bj_dt.minute
    if reset_time_minute < 0:
        reset_time_minute += 60
        reset_time_hour -= 1

    content = {'count': api_request_count, 'hour': reset_time_hour, 'minute': reset_time_minute}
    return content


if __name__ == '__main__':
    import socket
    import socks

    addr = "127.0.0.1"
    port = 1984

    socks.set_default_proxy(socks.SOCKS5, addr, port)
    socket.socket = socks.socksocket

    print(requests_to_wikipedia('南京'))
    print(requests_to_wikipedia('广州'))
    print(requests_to_wikipedia('Python'))
    print(requests_to_wikipedia('法国大革命'))
    print(requests_to_wikipedia('六四事件'))
    print(requests_to_wikipedia('ooo'))
    print(requests_to_wikipedia('aeklwhlek239210'))
    print(requests_to_wikipedia('土豆'))
    print(requests_to_wikipedia('西京'))