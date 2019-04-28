#!/usr/bin/env python

from django import forms


class BookForm(forms.Form):
    text = forms.CharField(label="内容", required=True, max_length=100)
