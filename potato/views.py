from django.shortcuts import render
import requests

from .word import Word
from .forms import BookForm
from .data import handle_data


# Create your views here.
def index(request):
    s_msg = Word()
    content = {"msg": s_msg}
    return render(request, 'index.html', content)


def test(request):
    s_msg = Word()
    content = {"msg": s_msg}

    if request.method != 'POST':
        return render(request, 'index2.html', content)
    else:
        form = BookForm(request.POST)
        if form.is_valid():  # 验证表单数据
            c_msg = form.cleaned_data['text']  # 获取验证后的表单数据
            url = "https://www.googleapis.com/customsearch/v1?q={}&cx=007606540339251262492:fq_p2g_s5pa&num=10&start=1&key=AIzaSyDti_06GjeOV6trMz0ixATpXC6pTuJhAt4".format(
                c_msg)
            url2 = "https://www.googleapis.com/customsearch/v1?q={}&cx=007606540339251262492:fq_p2g_s5pa&num=10&start=1&key=AIzaSyCDw49epd-yMaZ1yfIwi7koM1AyZu8XzZ0".format(
                c_msg)  # 备用api一个api一天调用100次
            r = requests.get(url)
            if r.status_code != 403:  # 表示第一个api 可用
                # s_msg = r.content.decode("utf-8")  返回 json
                s_msg = r.json()  # 返回 python对象
                content = handle_data(s_msg)
                return render(request, 'detail.html', content)
                # return HttpResponse(s_msg)
            else:
                r = requests.get(url2)
                s_msg = r.json()  # 返回 python对象
                content = handle_data(s_msg)
                return render(request, 'detail.html', content)
        else:
            return render(request, 'index2.html', content)
