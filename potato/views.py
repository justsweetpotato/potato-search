#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import reverse
import json

from .forms import BookForm
from .word import word
from .data import requests_to_google
from .data import get_api_data
from .data import get_ip_and_address
from .data import requests_to_wikipedia
from .data import check_web
from .data import error_403
from .data import choice_template
from .data import WEB
from .data import LANGUAGE_LIST


def search(request):
    '''将用户输入发送至谷歌处理, 处理返回结果后填充至网页'''

    # 生成表单(用于验证用户输入)
    form = BookForm(request.GET)

    if form.is_valid():  # 验证表单数据
        content = requests_to_google(request)  # 向 Google API 请求, 并处理返回结果

        if content != 403:
            template = choice_template(content['lang'], 'detail')
            return render(request, template, content)

        # 没有查询到任何结果, 返回错误信息
        content = error_403()
        return render(request, 'error.html', content, status=403)

    return HttpResponseRedirect(reverse('potato:index'))


def index(request):
    '''主页'''

    location = request.GET.get('location', 'off')
    language = request.GET.get('lang', 'zh-CN')
    if language not in LANGUAGE_LIST:
        language = 'zh-CN'

    s_msg = word(language)
    content = {"msg": s_msg}
    content['location'] = location
    content['lang'] = language
    content['proxy'] = WEB[0][1]
    template = choice_template(language, 'index')

    return render(request, template, content)


def test(request):
    '''测试页面, 使用 Google 提供的 JavaScript 代码生成搜索框'''

    language = request.GET.get('lang', 'zh-CN')
    s_msg = word(language)
    content = {"msg": s_msg}
    return render(request, 'test.html', content)


def doc(request):
    '''文档'''

    status = request.GET.get('status', '0')
    location = request.GET.get('location', 'off')
    language = request.GET.get('lang', 'zh-CN')
    content = check_web(status)
    content['location'] = location
    content['lang'] = language

    return render(request, 'doc.html', content)


def api_search(request):
    '''谷歌搜索接口'''

    q = request.GET.get('q')
    page = request.GET.get('page', 1)
    key = request.GET.get('key', None)

    if q and page:
        server_msg = get_api_data(q, page, key, 1)
        return HttpResponse(server_msg, content_type="application/json")

    return HttpResponse("缺少参数<br><a href='/doc/'>查看文档</a>")


def api_book(request):
    '''书籍查询接口, 返回 json 数据'''

    q = request.GET.get('q')
    page = request.GET.get('page', 1)
    key = request.GET.get('key', None)

    if q and page:
        server_msg = get_api_data(q, page, key)
        return HttpResponse(server_msg, content_type="application/json")

    return HttpResponse("缺少参数<br><a href='/doc/'>查看文档</a>")


def api_wiki(request):
    '''维基百科查询接口'''

    q = request.GET.get('q', '')

    if q:
        title, q_text = requests_to_wikipedia(q)
        if title:
            content = {
                'title': title,
                'text': q_text
            }
        else:
            content = {
                'error': {
                    'code': 404,
                    'message': 'Can not find related content.'
                }
            }
        content = json.dumps(content, indent=1, ensure_ascii=False)
        return HttpResponse(content, content_type="application/json")
    return HttpResponse("缺少参数<br><a href='/doc/'>查看文档</a>")


def api_ip(request):
    '''用户 IP 地址查询接口'''

    ip, address = get_ip_and_address(request)
    content = {
        'ip': ip,
        'address': address
    }
    content = json.dumps(content, indent=1, ensure_ascii=False)
    return HttpResponse(content, content_type="application/json")
