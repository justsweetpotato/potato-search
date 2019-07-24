#!/usr/bin/env python

from django import forms


class BookForm(forms.Form):
    q = forms.CharField(label="内容", required=True, max_length=100)
    page = forms.IntegerField(label="页数", required=False, max_value=99)
