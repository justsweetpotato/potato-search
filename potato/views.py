from django.shortcuts import render

from .forms import BookForm
from .word import word
from .data import requests_to_google


# Create your views here.
def test(request):
    '''测试页面, 使用 google 提供的 javascript 代码生成搜索框'''

    s_msg = word()
    content = {"msg": s_msg}
    return render(request, 'test.html', content)


def index(request):
    '''展示主页, 将用户输入发送至谷歌处理, 处理返回结果后填充至网页'''

    s_msg = word()
    content = {"msg": s_msg}

    # GET 请求则返回主页
    if request.method != 'POST':
        return render(request, 'index.html', content)

    # 生成表单(用于验证用户输入)
    form = BookForm(request.POST)

    if form.is_valid():  # 验证表单数据
        c_msg = form.cleaned_data['text']  # 获取验证后的表单数据
        content = requests_to_google(c_msg)  # 向 Google API 请求, 并处理返回结果

        if content:
            return render(request, 'detail.html', content)
        # 没有数据, 返回错误信息
        return render(request, 'error.html', status=403)

    # 验证失败(没有输入 or 输入字符长度大于 100)返回主页
    return render(request, 'index.html', content)
