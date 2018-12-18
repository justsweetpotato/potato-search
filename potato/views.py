from django.shortcuts import render, HttpResponse
import requests
import json

from .word import Word
from .forms import BookForm


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
            r = requests.get(url)
            s_msg = r.content.decode("utf-8")
            return HttpResponse(s_msg)
        else:
            return render(request, 'index2.html', content)
