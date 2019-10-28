from django.shortcuts import render
from .data import print_in_line, print_in_line_reverse


def obelisk(request):
    if request.method != 'POST':
        row = request.GET.get('row', 5)
        location = request.GET.get('location', 'off')
        language = request.GET.get('lang', 'lang_zh-CN')

        content = {
            'row': row,
            'style': ' ',
            'reverse': '0',
            'cn_lang': '',
            'location': location,
            'lang': language
        }

        return render(request, 'obelisk.html', content)

    else:
        row = request.POST.get('row', 5)
        try:
            row = int(row)
        except:
            row = 5
        if row < 1:
            row = 1
        elif row > 10:
            row = 10

        msg_pc = request.POST.get('msg_pc', '')
        msg_mobile = request.POST.get('msg_mobile', '')
        location = request.GET.get('location', 'off')
        language = request.GET.get('lang', 'lang_zh-CN')

        if msg_pc:
            msg = msg_pc
            type = 'pc'
        elif msg_mobile:
            type = 'mobile'
            msg = msg_mobile
        else:
            type = ''
            msg = ''

        style = request.POST.get('style', ' ')
        reverse = request.POST.get('reverse', '0')
        cn_lang = request.POST.get('cn_lang', '')

        if reverse == '0':
            content = print_in_line(row, msg, style, cn_lang)
        else:
            content = print_in_line_reverse(row, msg, style, cn_lang)

        content = {
            'content': content,
            'row': row,
            'msg': msg,
            'style': style,
            'reverse': reverse,
            'type': type,
            'cn_lang': cn_lang,
            'location': location,
            'lang': language
        }

        return render(request, 'obelisk.html', content)


def obelisk_beta(request):
    import re

    if request.method != 'POST':
        location = request.GET.get('location', 'off')
        language = request.GET.get('lang', 'lang_zh-CN')

        content = {
            'location': location,
            'lang': language
        }

        return render(request, 'obelisk_beta.html', content)

    else:
        msg_pc = request.POST.get('msg_pc', '')
        msg_mobile = request.POST.get('msg_mobile', '')
        location = request.GET.get('location', 'off')
        language = request.GET.get('lang', 'lang_zh-CN')

        if msg_pc:
            msg = msg_pc
            type = 'pc'
        elif msg_mobile:
            type = 'mobile'
            msg = msg_mobile
        else:
            type = ''
            msg = ''

        obelisk_msg = re.sub('\\r', '', msg)
        obelisk_msg = re.sub('\\n', '<br>', obelisk_msg)

        content = {
            'msg': msg,
            'type': type,
            'obelisk_msg': obelisk_msg,
            'location': location,
            'lang': language
        }

        return render(request, 'obelisk_beta.html', content)


def site_index(request):
    return render(request, 'site_index.html')
