# -*- coding: utf-8 -*-
from willow.willow import *


def wait(a, b=0):
    add("<p id='wait%s'>しばらくお待ちください。</p>" % str(a+b*10000))


def waithide(a, b=0):
    hide("#wait%s" % str(a+b*10000))


def start():
    add("<p id='start'>ボタンを押すと実験が始まります。<br />"
    "<input id='go' type='submit'></p>")


def priceset(a):
    # a = plnum
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


def pricesetcomp(a, b, c):
    # a = plnum
    # b = buylist
    # c = selllist
    if a % 2 == 0:
        for i in range(a/2):
            b.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#prbuy")
        for i in range(a/2, a):
            c.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#prsell")
    if a % 2 == 1:
        for i in range((a-1)/2):
            b.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#prbuy")
        for i in range((a-1)/2, a):
            c.append(int(peek("#pr%s" % i)))
            add("%s円  " % int(peek("#pr%s" % i)), "#prsell")
