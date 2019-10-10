#!/usr/bin/env python
# 处理数据

import requests
import re
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from lxml import etree
from threading import Thread

# 总页数
PAGES = 3

# API KEY (100次/日)
KEY_LIST = [
    "AIzaSyDti_06GjeOV6trMz0ixATpXC6pTuJhAt4",
    "AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0",
    'AIzaSyAdolxu5TWJhArM00hTqTUwOTDHK00806s'
]

# (名称, 网址, 状态)
WEB = (
    ('WebProxy A', 'https://proxy.littlepotato.cf/', ''),  # 通用代理要放第一个后面会根据索引获取
    ('WebProxy B', 'https://bot-go-2.herokuapp.com/', ''),
    ('You2Php', 'https://bot-yt-1.herokuapp.com/', ''),
)

APP = {
    "search": "007606540339251262492:smmy8xt1wrw",
    "book": "007606540339251262492:fq_p2g_s5pa"
}

LANGUAGE_LIST = ['lang_en', 'lang_zh-CN', 'lang_zh-TW']


class MyThread(Thread):
    '''一个能保存子线程结果的自定义线程类'''

    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        return self.result


def requests_to_google(request):
    '''向 Google API 发送请求, 并返回数据'''
    # https://www.googleapis.com/customsearch/v1?q=python&cx=007606540339251262492:smmy8xt1wrw&num=10&start=1&key=AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0
    language = request.GET.get('lang', 'lang_zh-CN')  # 获取语言
    action = request.GET.get('action', "search")  # TODO: 将前端此参数改为 search or book, 后端返回此参数供前端判断
    language, action, app_id = check_value(language, action)  # 检查参数合法性不正确重置为默认值
    client_msg = request.GET.get('q')  # 获取查询字符
    page = int(request.GET.get('page', 1))  # 获取页码
    location = request.GET.get('location', 'off')  # 地理位置开关
    ip = None  # IP 地址
    address = None  # 地理位置
    title = None  # 百科词条标题
    q_text = None  # 百科词条内容

    # TODO:耗时操作, 可用异步请求新特性
    if page == 1:
        thread_wiki = MyThread(func=requests_to_wikipedia, args=(client_msg, language))  # 获取维基百科词条的简介
        thread_wiki.start()

    # TODO:耗时操作, 可用异步请求新特性
    if location == 'on':
        thread_local = MyThread(func=get_ip_and_address, args=(request,))  # 获取 IP 和 address
        thread_local.start()

    for key in KEY_LIST:
        url = "https://www.googleapis.com/customsearch/v1?" \
              "q={0}&cx={1}&num=10&start={2}&" \
              "key={3}&lr={4}".format(client_msg, app_id, page, key, language)

        # 使用 with 语句可以确保连接被关闭
        with requests.get(url) as r:
            # Google API 配额用尽时会返回 403 错误
            if r.status_code != 403:
                server_msg = r.json()  # 直接处理 json 返回 字典
                content = handle_data(server_msg)

                if action == 'book':
                    content["book"] = True

                if page == 1:
                    thread_wiki.join()
                    title, q_text = thread_wiki.get_result()

                if location == 'on':
                    thread_local.join()
                    ip, address = thread_local.get_result()

                content['q'] = client_msg
                content['page'] = page
                content['pages'] = list(range(1, PAGES + 1))
                content['ip'] = ip
                content['address'] = address
                content['location'] = location
                content['title'] = title
                content['text'] = q_text
                content['proxy'] = WEB[0][1] + "-----"  # 网页代理的 URL 格式
                content['lang'] = language
                content['action'] = action

                return content

    # 所有请求均失败, 返回 403
    return 403


def requests_to_wikipedia(client_msg, language='lang_zh-CN'):
    '''向维基百科查询词条信息'''
    # TODO: 逻辑可以改进
    if language == 'lang_en':
        # url = "https://en.wikipedia.org/wiki/{}".format(client_msg)
        return None, None  # TODO: 英语匹配的正则待改进
    elif language == 'lang_zh-TW':
        url = "https://zh.wikipedia.org/zh-tw/{}".format(client_msg)
    else:
        url = "https://zh.wikipedia.org/zh-cn/{}".format(client_msg)
    try:
        response = requests.get(url)
    except:
        return None, None
    if response.status_code != 200:
        return None, None
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
            content_exist_info = re.match('.*?(为准|為準)。', content.strip(), flags=re.S)  # 获取说明信息
            if content_exist_info:  # 如果 p[?] 为说明信息
                continue
            break
        else:
            continue

    if content:
        content_exist_list = re.match('.*?[^。(\n|\[\d+\])]$', content, flags=re.S)  # 词条是否存在多义
        if content_exist_list:  # 如果存在多义, 则取有用的信息
            content_exist_list_use = re.sub('。.*?：', '。\n', content_exist_list.group())
            if content_exist_list_use.endswith('。\n'):  # 如果结尾不为。表示无用信息
                content = content_exist_list_use
            else:
                return None, None

        title = html.xpath('//*[@id="firstHeading"]/text()')[0]  # 获取标题
        content = re.sub('\[.*?\](:\d+)?|（.*?）|((中国互联网|中國網際網路).*。)', '', content, flags=re.S)  # 将文本中的 [] 与 () 舍弃
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
            url = data_dict["link"]
            link_list.append(url)
            snippet_list.append(data_dict["htmlSnippet"])

        data_zip = zip(title_list, link_list, snippet_list)
        content = {"content": data_zip}
        content['results'] = server_msg.get("searchInformation")["formattedTotalResults"]
        content['time'] = server_msg.get("searchInformation")["formattedSearchTime"]
        content["empty"] = False
    else:
        content["empty"] = True

    return content


def get_ip_and_address(request):
    '''获取用户 IP 与 地址'''

    ip = request.META.get("HTTP_X_FORWARDED_FOR", "")  # 在使用反向代理的服务器上获取 Client IP
    if not ip:
        ip = request.META.get('REMOTE_ADDR', "")  # 在本地测试环境获取 Client IP
    url = "https://freeapi.ipip.net/{0}".format(ip)  # 获取地理位置
    try:
        res = requests.get(url).json()
    except:
        return None, None
    else:
        address = res[0] + ' ' + res[1] + ' ' + res[2] + ' ' + res[4]

    return ip, address


def get_api_data(q, page, key, type=0):
    '''直接返回 Google API 接口的结果'''

    if key == None:
        key = KEY_LIST[0]

    if type == 1:
        type_value = APP["search"]
    else:
        type_value = APP["book"]

    url = "https://www.googleapis.com/customsearch/v1?" \
          "q={0}&cx={1}&num=10&start={2}&" \
          "key={3}".format(q, type_value, page, key)

    with requests.get(url) as r:
        server_msg = r.text
        return server_msg


def check_web(status):
    '''检查网站可用性 & 激活 herokuapp'''
    # TODO: 可用异步请求新特性
    if status == '1':
        title_list = []
        url_list = []
        checked = []
        thread_list = []

        for title, url, _ in WEB:
            title_list.append(title)
            url_list.append(url)
            t = MyThread(func=requests_status, args=(url,))
            thread_list.append(t)

        for t in thread_list:
            t.start()

        for t in thread_list:
            t.join()
            checked.append(t.get_result())

        content = {'content': zip(title_list, url_list, checked)}
        content['status'] = '1'
    else:
        content = {'content': WEB}

    return content


def requests_status(url):
    '''请求网站, 返回状态码'''

    try:
        r = requests.get(url)
    except:
        return 0
    else:
        if r.status_code == 200:
            return 1
        return 0


def error_403():
    '''获取 API 调用最大次数和重置时间'''

    api_request_count = len(KEY_LIST) * 100
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)  # UTC 时间
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))  # UTC+8 (北京时间)

    reset_time_hour = 15 - bj_dt.hour  # API 次数在北京时间 15时(太平洋时间 0时) 重置
    if reset_time_hour < 0:
        reset_time_hour += 24
    reset_time_minute = 0 - bj_dt.minute
    if reset_time_minute < 0:
        reset_time_minute += 60
        reset_time_hour -= 1

    content = {'count': api_request_count, 'hour': reset_time_hour, 'minute': reset_time_minute}
    return content


def check_value(language='lang_zh-CN', action='search'):
    '''参数错误则重置为默认值并额外返回 app_id'''

    if language not in LANGUAGE_LIST:
        language = 'lang_zh-CN'

    if action in ['Library', '搜书', '找書', 'book']:
        action = 'book'
    else:
        action = 'search'

    app_id = APP[action]
    return language, action, app_id


def choice_template(language, name):
    '''根据语言与名称选择模板'''

    template = '{}/{}.html'.format(language, name)
    return template


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
    print(requests_to_wikipedia('hi'))
    print(requests_to_wikipedia('ewae'))
    print(requests_to_wikipedia('百度'))
    print(requests_to_wikipedia('分号'))
    print(requests_to_wikipedia('华盛顿'))
    print(requests_to_wikipedia('亚马逊雨林'))

    # print(error_403())
