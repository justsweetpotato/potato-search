from django.shortcuts import render, HttpResponseRedirect, reverse

from .forms import BookForm
from .word import word
from .data import requests_to_google, get_ip_address


def search(request):
    '''将用户输入发送至谷歌处理, 处理返回结果后填充至网页'''

    # 生成表单(用于验证用户输入)
    form = BookForm(request.GET)

    if form.is_valid():  # 验证表单数据
        c_msg = request.GET.get('q')  # 获取验证后的表单数据
        page = request.GET.get('page', 1)
        ip1 = request.META['X-Forwarded-For']
        ip2 = request.headers['X-Forwarded-For']
        ip3 = request.environ['X-Forwarded-For']
        # ip_address = get_ip_address(ip)

        content = requests_to_google(c_msg, int(page), ip1)  # 向 Google API 请求, 并处理返回结果

        if content != 403:
            return render(request, 'detail.html', content)
        # 没有查询到任何结果, 返回错误信息
        return render(request, 'error.html', status=403)

    return HttpResponseRedirect(reverse('potato:index'))


def index(request):
    '''主页'''

    s_msg = word()
    content = {"msg": s_msg}

    return render(request, 'index.html', content)


def test(request):
    '''测试页面, 使用 google 提供的 javascript 代码生成搜索框'''

    s_msg = word()
    content = {"msg": s_msg}
    return render(request, 'test.html', content)
