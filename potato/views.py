from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import reverse

from .forms import BookForm
from .word import word
from .data import requests_to_google
from .data import get_api_data
from .data import get_client_ip
from .data import get_ip_address
from .data import requests_to_wikipedia
from .data import check_web


def search(request):
    '''将用户输入发送至谷歌处理, 处理返回结果后填充至网页'''

    # 生成表单(用于验证用户输入)
    form = BookForm(request.GET)

    if form.is_valid():  # 验证表单数据
        content = requests_to_google(request)  # 向 Google API 请求, 并处理返回结果

        if content != 403:
            response = render(request, 'detail.html', content)
            return response
        # 没有查询到任何结果, 返回错误信息
        return render(request, 'error.html', status=403)

    return HttpResponseRedirect(reverse('potato:index'))


def index(request):
    '''主页'''

    location = request.GET.get('location', 'off')
    s_msg = word()
    content = {"msg": s_msg}
    content['location'] = location

    return render(request, 'index.html', content)


def test(request):
    '''测试页面, 使用 Google 提供的 JavaScript 代码生成搜索框'''

    s_msg = word()
    content = {"msg": s_msg}
    return render(request, 'test.html', content)


def doc(request):
    '''文档'''

    web = (
        ('Web 代理', 'https://bot-go-1.herokuapp.com/'),
        ('You2Php', 'https://bot-yt-test.herokuapp.com/')
    )

    content = check_web(web)
    return render(request, 'doc.html', content)


def api_book(request):
    '''书籍查询接口, 返回 json 数据'''

    q = request.GET.get('q')
    page = request.GET.get('page', 1)
    key = request.GET.get('key', None)

    if q and page:
        server_msg = get_api_data(q, page, key)
        return HttpResponse(server_msg, content_type="application/json")

    return HttpResponse("缺少参数<br><a href='/doc/'>查看文档</a>")


def api_ip(request):
    '''用户 IP 地址查询接口'''

    ip = get_client_ip(request)
    address = get_ip_address(ip)
    return HttpResponse("当前 IP: " + ip + " 来自于: " + address)


def api_wiki(request):
    '''维基百科查询接口'''

    q = request.GET.get('q', '')

    if q:
        title, q_text = requests_to_wikipedia(q)
        if title:
            return HttpResponse(title + "<br>" + q_text)
        return HttpResponse("查询不到有关词条")
    return HttpResponse("缺少参数<br><a href='/doc/'>查看文档</a>")
