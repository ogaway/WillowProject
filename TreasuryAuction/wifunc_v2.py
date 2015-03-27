# -*- coding: utf-8 -*-
from willow.willow import *

def numset():
    add("<p id='numset'>参加人数を入力してください。<br />"
    "<input id='plnum' type='text' />"
    "<input id='go' type='submit'></p>")


def get_num():
    return int(peek("#plnum"))


def numset_end(plnum):
    hide("#numset")
    add("<p id='numset_end'>実験人数：<span id='num'></span>人</p>")
    add(plnum, "#num")


def goodsset():
    add("<p id='goodsset'>財の数を入力してください。<br />"
    "<input id='goodsnum' type='text' />"
    "<input id='go' type='submit'></p>")


def get_goods():
    return int(peek("#goodsnum"))


def goodsset_end(goodsnum):
    hide("#goodsset")
    add("<p id='goodsset_end'>財の数：<span id='goods'></span>個</p>")
    add(goodsnum, "#goods")


def table_css():
    add("<style type='text/css'>table {border-collapse: collapse;}</style>")
    add("<style type='text/css'>td {border: solid 1px;padding: 0.5em;}</style>")


def wait(a, b=0):
    add("<p id='wait%s'>しばらくお待ちください。</p>" % str(a+b*10000))


def waithide(a, b=0):
    hide("#wait%s" % str(a+b*10000))


def wiput(a, b):
    for i in range(a):
        put(b)

def witake(a, b):
    for i in range(a):
        take(b)

def ready():
    add("<p id='ready'>実験の内容について理解し、"
    "準備が整いましたらボタンを押してください。<br />"
    "<input id='go' type='submit'></p>")


def start():
    add("<p id='start'>被験者の準備が整いました。<br />"
    "ボタンを押すと実験が始まります。<br />"
    "<input id='go' type='submit'></p>")


def DApriceset(a):
    # a = plnum
    add("<p id='priceset'>私的価値を入力してください。<br />"
    "買い手<br /><span id='buypr'></span>"
    "売り手<br /><span id='sellpr'></span>"
    "<input id='go' type='submit'></p>")
    if a % 2 == 0:
        for i in range(a/2):
            add("<input id='pr%s' type='text' /><br />" % i, "#buypr")
        for i in range(a/2, a):
            add("<input id='pr%s' type='text' /><br />" % i, "#sellpr")
    else:
        for i in range((a-1)/2):
            add("<input id='pr%s' type='text' /><br />" % i, "#buypr")
        for i in range((a-1)/2, a):
            add("<input id='pr%s' type='text' /><br />" % i, "#sellpr")


def DApriceset_end(a, b, c):
    # a = plnum
    # b = buylist
    # c = selllist
    hide("priceset")
    add("<p id='priceset_end'>"
    "買い手<br /><span id='buypr_end'></span><br />"
    "売り手<br /><span id='sellpr_end'></span></p>")
    if a % 2 == 0:
        for i in range(a/2):
            b.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#buypr_end")
        for i in range(a/2, a):
            c.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#sellpr_end")
    else:
        for i in range((a-1)/2):
            b.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#buypr_end")
        for i in range((a-1)/2, a):
            c.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#sellpr_end")


def AFCpriceset(a):
    # a = plnum
    add("<p id='priceset'>私的価値を入力してください。<br />"
    "I-type1<br /><span id='ipr1'></span><br />"
    "I-type2<br /><span id='ipr2'></span><br />"
    "J-type<br /><span id='jpr'></span><br />"
    "<input id='go' type='submit'></p>")
    if a % 3 == 0:
        for i in range(a/3):
            add("<input id='pr%s' type='text' /><br />" % i, "#ipr1")
        for i in range(a/3, 2*a/3):
            add("<input id='pr%s' type='text' /><br />" % i, "#ipr2")
        for i in range(2*a/3, a):
            add("<input id='pr%s' type='text' /><br />" % i, "#jpr")
    elif a % 3 == 1:
        for i in range((a-1)/3 + 1):
            add("<input id='pr%s' type='text' /><br />" % i, "#ipr1")
        for i in range((a-1)/3 + 1, 2*(a-1)/3 + 1):
            add("<input id='pr%s' type='text' /><br />" % i, "#ipr2")
        for i in range(2*(a-1)/3 + 1, a):
            add("<input id='pr%s' type='text' /><br />" % i, "#jpr")
    else:
        for i in range((a-2)/3 + 1):
            add("<input id='pr%s' type='text' /><br />" % i, "#ipr1")
        for i in range((a-2)/3 + 1, 2*(a-2)/3 + 2):
            add("<input id='pr%s' type='text' /><br />" % i, "#ipr2")
        for i in range(2*(a-2)/3 + 2, a):
            add("<input id='pr%s' type='text' /><br />" % i, "#jpr")


def AFCpriceset_end(a, b, c, d):
    # a = plnum
    # b = itype1list
    # c = itype2list
    # d = jtypelist
    hide("#priceset")
    add("<p id='priceset_end'>"
    "I-type1<br /><span id='ipr1_end'></span><br />"
    "I-type2<br /><span id='ipr2_end'></span><br />"
    "J-type<br /><span id='jpr_end'></span></p>")
    if a % 3 == 0:
        for i in range(a/3):
            b.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#ipr1_end")
        for i in range(a/3, 2*a/3):
            c.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#ipr2_end")
        for i in range(2*a/3, a):
            d.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#jpr_end")
    elif a % 3 == 1:
        for i in range((a-1)/3 + 1):
            b.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#ipr1_end")
        for i in range((a-1)/3 + 1, 2*(a-1)/3 + 1):
            c.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#ipr2_end")
        for i in range(2*(a-1)/3 + 1, a):
            d.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#jpr_end")
    else:
        for i in range((a-2)/3 + 1):
            b.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#ipr1_end")
        for i in range((a-2)/3 + 1, 2*(a-2)/3 + 2):
            c.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#ipr2_end")
        for i in range(2*(a-2)/3 + 2, a):
            d.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#jpr_end")
