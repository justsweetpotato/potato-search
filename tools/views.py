from django.shortcuts import render
from .data import print_in_line, print_in_line_reverse


def obelisk(request):
    if request.method != 'POST':
        row = request.GET.get('row', 5)

        content = {}
        content['row'] = row
        content['style'] = ' '
        content['reverse'] = '0'
        content['lang'] = ''

        return render(request, 'obelisk.html', content)

    else:
        row = request.POST.get('row', 5)
        try:
            row = int(row)
        except:
            row = 5
        if row < 1:
            row = 1
        if row > 10:
            row = 10

        msg_pc = request.POST.get('msg_pc', '')
        msg_mobile = request.POST.get('msg_mobile', '')

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
        lang = request.POST.get('lang', '')

        if reverse == '0':
            content = print_in_line(row, msg, style, lang)
        else:
            content = print_in_line_reverse(row, msg, style, lang)

        content = {
            'content': content,
            'row': row,
            'msg': msg,
            'style': style,
            'reverse': reverse,
            'type': type,
            'lang': lang
        }
        return render(request, 'obelisk.html', content)
