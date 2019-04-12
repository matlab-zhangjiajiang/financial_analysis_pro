# -*- coding:utf-8 -*-
import re

def replace_line_terminator(x):
    """替换行终止符"""
    try:
        x = re.sub(r'\r\n', '\n', x)
    except TypeError:
        pass
    return x

def replace_special_character(context):
    return context.replace('\n','').replace(' ','').replace('<br>','').replace('<p>','').replace('</p>','').replace('<br/>','')

def replace_spicial_symbol(context):
    return context.replace('，','').replace('。','')\
        .replace('【','').replace('】','').replace('、','').replace('（','')\
        .replace('）','').replace('：','').replace('…','')