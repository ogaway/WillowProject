# coding: UTF-8
from willow import *
from wifunc_v1 import *
import numpy as np
import random
from pandas import *
import matplotlib.pyplot as plt


def session(me):
    # 一期を何秒にするか変更可能
    ts = 50
    if me == 0:
        add("<h1>Asset Market : Monitor</h1>")
        # 人数登録
        numset()
        take({"client": me})
        plnum = get_num()
        numset_end(plnum)
        # 実験説明開始(a)
        wiput(plnum, {"tag": "a"})
        wait(1)
        # 実験内容把握(b)
        witake(plnum, {"tag": "b"})
        waithide(1)
        # 実験開始確認
        start()
        take({"client": me})
        hide("#start")
        # 実験開始(c)
        add(open("assetmarket_moni.html"))
        wiput(plnum, {"tag": "c"})
        # 変数・関数の定義
        buyprice = 0
        sellprice = 1000000
        buynum = 0
        sellnum = 0
        dividend_list = [0, 8, 28, 60]
        def timer():
            put({"id": "d", "tag": 1})
        def ping():
            put({"id": "d", "tag": 2})
        for i in range(15):
            background(ping, ts)
            for j in range(ts):
                background(timer, j)
            while True:
                # 注文を受け取る(d)
                msg = take({"id": "d"})
                if msg["tag"] == 1:
                    wiput(plnum, {"id": "e", "tag": 2})
                elif msg["tag"] == 2:
                    break
                elif msg["type"] == "buy":
                    if buyprice < msg["value"]:
                        buyprice = msg["value"]
                        buynum = msg["client"]
                        let(msg["value"], "#buyprice")
                        let(msg["client"], "#buynum")
                    # 板情報更新(e)
                    wiput(plnum, {"id": "e", "tag": 3, "type": "buy",
                    "buyprice": buyprice, "buynum": buynum})
                elif msg["type"] == "sell":
                    if sellprice > msg["value"]:
                        sellprice = msg["value"]
                        sellnum = msg["client"]
                        let(msg["value"], "#sellprice")
                        let(msg["client"], "#sellnum")
                    # 板情報更新(e)
                    wiput(plnum, {"id": "e", "tag": 3, "type": "sell",
                    "sellprice": sellprice, "sellnum": sellnum})
                if buyprice > sellprice:
                    wiput(plnum, {"id": "e", "tag": 4, "buyprice": buyprice,
                    "buynum": buynum, "sellprice": sellprice,
                    "sellnum": sellnum})
                    logprice = (buyprice + sellprice) * 0.5
                    exbond = (15 - i) * 24
                    log("期待収益と約定価格", exbond, logprice)
                    let("(入札なし)", "#buyprice")
                    let("(入札なし)", "#buynum")
                    let("(入札なし)", "#sellprice")
                    let("(入札なし)", "#sellnum")
                    buyprice = 0
                    sellprice = 1000000
                    buynum = 0
                    sellnum = 0
            # 配当の決定(e)
            dividend = random.choice(dividend_list)
            wiput(plnum, {"id": "e", "tag": 5, "div": dividend})
        add("<p>これで実験を終了します。</p>")

    else:
        add("<h1>Asset Market : Client_No.%s</h1>" % me)
        wait(1)
        # 実験説明開始(a)
        take({"tag": "a"})
        waithide(1)
        # 実験内容把握(b)
        nameset()
        take({"client": me})
        myname = get_name()
        hide("#nameset")
        put({"tag": "b"})
        wait(2)
        # 実験開始(c)
        take({"tag": "c"})
        waithide(2)
        add(open("assetmarket_sub.html"))
        # 変数・関数の定義
        capital = 100
        bond = 10
        buyprice = 0
        sellprice = 1000000
        buynum = 0
        sellnum = 0
        let(capital, "#capital")
        let(bond, "#bond")
        for i in range(15):
            counter = ts
            let(counter, "#time")
            let(i+1, "#number")
            while True:
                # 板情報更新、もしくは注文受け取り(e)
                # 他の被験者も注文を受け取れてしまう。
                msg = take({"id": "e", "client": me})
                # タイマー更新
                if msg["tag"] == 2:
                    counter -= 1
                    let(counter, "#time")
                # 板情報更新
                elif msg["tag"] == 3:
                    if msg["type"] == "buy":
                        let(msg["buyprice"], "#buyprice")
                        let(msg["buynum"], "#buynum")
                    if msg["type"] == "sell":
                        let(msg["sellprice"], "#sellprice")
                        let(msg["sellnum"], "#sellnum")
                # 取引成立
                elif msg["tag"] == 4:
                    if msg["buynum"] == me:
                        capital -= msg["buyprice"]
                        bond += 1
                    if msg["sellnum"] == me:
                        capital += msg["sellprice"]
                        bond -= 1
                    add("プレイヤー%sとプレイヤー%sの間で取引が成立しました。<br />" %
                    (msg["buynum"], msg["sellnum"]), "#info")
                    let("(入札なし)", "#buyprice")
                    let("(入札なし)", "#buynum")
                    let("(入札なし)", "#sellprice")
                    let("(入札なし)", "#sellnum")
                    let(capital, "#capital")
                    let(bond, "#bond")
                # 配当の受け渡し
                elif msg["tag"] == 5:
                    break
                # 注文(d)
                else:
                    if (peek("#ask") != "") and (peek("#bid") != ""):
                        add("買い売りどちらの欄にも値が記入されています。<br />",
                        "#info")
                    elif peek("#ask") != "":
                        put({"id": "d", "type": "buy", "value": int(peek("#ask")),
                        "client": me, "tag": 0})
                    elif peek("#bid") != "":
                        put({"id": "d", "type": "sell", "value": int(peek("#bid")),
                        "client": me, "tag": 0})
            dividend = msg["div"]
            capital += dividend * bond
            let(capital, "#capital")
            let(bond, "#bond")
            add("%s期目の配当額は証券1枚あたり%s円でした。<br />" % (i+1, dividend), "#info")
        add("<p>これで実験を終了します。</p>", "#info")
        log(me, myname, capital)

run(session)
