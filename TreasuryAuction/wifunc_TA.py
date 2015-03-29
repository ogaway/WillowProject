# -*- coding: utf-8 -*-
from willow.willow import *
import csv

"""
Functions for Treasuru Auction
"""

def board(a):
    add(
    '<div id="board%s">'
    '<h2>入札画面</h2><p>共通価値の予想価格(E)：<span id="estimate%s"></span>円<br />'
    '1単位目の入札価格：<input type="text" id="bid1%s" />円<br />'
    '2単位目の入札価格：<input type="text" id="bid2%s" />円<br />'
    '入札額を記入し終えたらボタンを押してください。<input type="submit" id="offer%s"><br />'
    '（注意）<br />'
    '・入札価格は[500, 6000]の範囲で入力してください。<br />'
    '・1単位は必ず500円以上の入札をしてください。<br />'
    '・1単位のみ購入する場合は2単位目の入札価格記入欄に「0」を入力してください。<br /></p></div>'
     % (a, a, a, a, a), "#experiment")


def boardhide(a):
    hide("#board%s" % a)


def waitinfo(a, b=0):
    add("<p id='waitinfo%s'>しばらくお待ちください。</p>" % str(a+b*10000), "#info")


def waitinfohide(a, b=0):
    hide("#waitinfo%s" % str(a+b*10000))


def nextTA(a):
    add("<p id='next%s'>次のラウンドにうつる準備ができましたら、"
    "ボタンを押してください。<br />"
    "<input id='go' type='submit'></p>" % a, "#info")


def nextTAhide(a):
    hide("#next%s" % a)
