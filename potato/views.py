from django.shortcuts import render

from .word import Word
# Create your views here.
def index(request):
    msg = Word()
    content = {'msg': msg}
    return render(request, 'book.html', content)
