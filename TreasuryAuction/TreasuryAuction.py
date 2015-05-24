# coding: UTF-8
from willow.willow import *
from wifunc_v2 import *
from wifunc_TA import *
import numpy as np
import random
import csv


def session(me):
    """
    Setup of the Auction Designs
    ---
    The variable "auction" is the switch to change an auction design.
    "auction" == 0:
        Discriminatory Designs
        The winnig bidders pay the price they habe bid.
    "auction" == 1:
        Uniform Designs
        The winning bidders are all charged a price that is equal to
        the cut-off price, the highest market-clearing price.
    "auction" == 2:
        Spanish Designs
        Winning bids that are above the weighted average winning bid
        pay the same price; this price is equal to weighted average
        winning bid.
        On the other hand, winning bids that are below the weighted
        average winning bid are fully paid.
    ---
    """
    auction = 1
    Round = 10

    if me == 0:
        add(open("web/index.html"))
        add("Auctions for Government Securities : Monitor Display<br />", "#catch")
        add("国債オークション 実験者", "#catch")
        # Initial Setting
        # Player Number
        numset()
        take({"client": me})
        plnum = get_num()
        numset_end(plnum)
        # Goods Number
        goodsset()
        take({"client": me})
        goodsnum = get_goods()
        goodsset_end(goodsnum)
        # Instruction(a)
        wiput(plnum, {"tag": "a", "plnum": plnum, "goodsnum": goodsnum})
        wait(1)
        # Ready to start(b)
        witake(plnum, {"tag": "b"})
        waithide(1)
        start(1)
        take({"client": me})
        starthide(1)
        add("実験を開始します。<br />", "#main")
        log("PlayerNum:%s" % plnum, "GoodsNum:%s" % goodsnum)

        # Start !!
        # Open the Datasets
        if auction == 0:
            f = open('data/data1.csv', 'rb')
            log("Value", "DISC")
        elif auction == 1:
            f = open('data/data2.csv', 'rb')
            log("Value", "UNI")
        elif auction == 2:
            f = open('data/data3.csv', 'rb')
            log("Value", "SPAN")
        dataReader = csv.reader(f)
        datasets = []
        revenue = 0
        for row in dataReader:
            datasets.append(row)
        for time in range(Round):
            add("<h2>第%sラウンド</h2>" % (time+1), "#main")
            # Reset variables
            data = datasets[time]
            averagebid = 0
            averageprice = 0
            info = []
            # Put Value and Estimates(c)
            for i in range(plnum):
                put({"tag": "c", "v": int(data[0]), "e": int(data[i+1])})
            # Take Bids(d)
            add("Take Bids<br />", "#main")
            for i in range(plnum):
                msg = take({"tag": "d"})
                add("被験者No.%sは%s円と%s円の注文を出しました。<br />" % (msg["client"], msg["bid1"], msg["bid2"]), "#main")
                info.append({"client": msg["client"], "bid": msg["bid1"]})
                info.append({"client": msg["client"], "bid": msg["bid2"]})
            # Ranked
            info = sorted(info, key=lambda x:x["bid"], reverse=True)
            # Allocation and Price(e)
            add("Allocation and Price<br />", "#main")
            # Discriminatory Designs
            if auction == 0:
                for i in range(goodsnum):
                    averagebid += info[i]["bid"]
                    averageprice += info[i]["bid"]
                    put({"tag": "e", "client": info[i]["client"], "get": 0, "price": info[i]["bid"]})
                    add("被験者No.%sは%s円で国債を１つ落札しました。<br />" % (info[i]["client"], info[i]["bid"]), "#main")
                for i in range(goodsnum, len(info)):
                    put({"tag": "e", "client": info[i]["client"], "get": 1})
                    add("被験者No.%sは国債を１つ落札できませんでした。<br />" % info[i]["client"], "#main")
            # Uniform Designs
            if auction == 1:
                price = info[goodsnum-1]["bid"]
                for i in range(goodsnum):
                    averagebid += info[i]["bid"]
                    averageprice += price
                    put({"tag": "e", "client": info[i]["client"], "get": 0, "price": price})
                    add("被験者No.%sは%s円で国債を１つ落札しました。<br />" % (info[i]["client"], price), "#main")
                for i in range(goodsnum, len(info)):
                    put({"tag": "e", "client": info[i]["client"], "get": 1})
                    add("被験者No.%sは国債を１つ落札できませんでした。<br />" % info[i]["client"], "#main")
            # Spanish Designs
            if auction == 2:
                for i in range(goodsnum):
                    averageprice += info[i]["bid"]
                price = averageprice /goodsnum
                for i in range(goodsnum):
                    averagebid += info[i]["bid"]
                    if info[i]["bid"] >= price:
                        put({"tag": "e", "client": info[i]["client"], "get": 0, "price": price})
                        add("被験者No.%sは%s円で国債を１つ落札しました。<br />" % (info[i]["client"], price), "#main")
                    else:
                        put({"tag": "e", "client": info[i]["client"], "get": 0, "price": info[i]["bid"]})
                        add("被験者No.%sは%s円で国債を１つ落札しました。<br />" % (info[i]["client"], info[i]["bid"]), "#main")
                for i in range(goodsnum, len(info)):
                    put({"tag": "e", "client": info[i]["client"], "get": 1})
                    add("被験者No.%sは国債を１つ落札できませんでした。<br />" % info[i]["client"], "#main")
            # Put Average Winning Bid(f)
            averagebid = averagebid / goodsnum
            averageprice = averageprice /goodsnum
            add("平均勝ち入札価格は%s円、平均落札価格は%s円でした。<br />" % (averagebid, averageprice), "#main")
            log("Value(%s)" % int(data[0]), averageprice*goodsnum)
            revenue += averageprice
            wiput(plnum, {"tag": "f", "ave": averagebid})
            # Next Round(g)
            if time != Round-1:
                for i in range(plnum):
                    take({"tag": "g"})
                start(time+2)
                take({"client": me})
                starthide(time+2)
            else:
                result = []
                # Take Profit(g)
                for i in range(plnum):
                    msg = take({"tag": "g"})
                    result.append({"client": msg["client"], "profit": msg["profit"]})
                # Ranked
                result = sorted(result, key=lambda x:x["profit"], reverse=True)
                add("<p id='start%s'>被験者の準備が整いました。<br />"
                "ボタンを押すと結果発表にうつります。<br />"
                "<input id='go' type='submit'></p>" % (time+2), "#main")
                take({"client": me})
                starthide(time+2)
                # Put Result(h)
                wiput(plnum, {"tag": "h", "result": result})
                add("<h2>結果発表</h2>", "#main")
                for i in range(plnum):
                    add("%s位：被験者No.%s, %s円<br />" % (i+1, result[i]["client"], result[i]["profit"]), "#main")
        add("<p>これで実験を終了します。</p>", "#main")

    else:
        add(open("web/index.html"))
        add("Auctions for Government Securities ： Participants Display<br />", "#catch")
        add("国債オークション 参加者No.%s" % me, "#catch")
        wait(1)
        # Instruction(a)
        msg = take({"tag": "a"})
        plnum = msg["plnum"]
        waithide(1)
        # Discriminatory Designs Instruction
        if auction == 0:
            add(open("web/TAsubject_DESC.html"), "#main")
        # Uniform Designs Instruction
        elif auction == 1:
            add(open("web/TAsubject_UNI.html"), "#main")
        # Spanish Designs Instruction
        elif auction == 2:
            add(open("web/TAsubject_SPAN.html"), "#main")
        add(plnum, "#plnum")
        add(msg["goodsnum"], "#goodsnum1")
        add(msg["goodsnum"], "#goodsnum2")
        add(msg["goodsnum"], "#goodsnum3")
        add(msg["goodsnum"], "#goodsnum4")
        # Ready to start(b)
        ready()
        take({"client": me})
        put({"tag": "b"})
        hide("#ready")
        wait(2)

        # Start !!
        # Take Value and Estimate(c)
        profit = 0
        for time in range(Round):
            msg = take({"tag": "c"})
            if time == 0:
                waithide(2)
                hide("#instruction")
                add("<h2>情報板</h2>"
                "<p>ラウンド数：第<span id='roundnum'>1</span>ラウンド</p>"
                "<p>現在の合計利潤：<span id='profit'>0</span>円</p>"
                "<p id='info'></p>", "#experiment")
            elif time >= 1:
                let(time+1, "#roundnum")
                waitinfohide(2*time)
                boardhide(time-1)
            board(time)
            value = msg["v"]
            estimate = msg["e"]
            add(estimate, "#estimate%s" % time)
            let("入札価格記入欄に価格を入力して送信してください。", "#info")
            while True:
                take({"client": me})
                bid1 = int(peek("#bid1%s" % time))
                bid2 = int(peek("#bid2%s" % time))
                if (bid1 >= 500) and (bid1 <= 6000) and (bid2 >= 500 or bid2 == 0) and (bid2 <= 6000):
                    let("", "#info")
                    break
                else:
                    let("<font color='red'>入札価格は注意書きに従った金額を入力してください。</font>", "#info")
            hide("#offer%s" % time)
            waitinfo(2*(time+1) - 1)
            # Submit Bids(d)
            put({"tag": "d", "bid1": bid1, "bid2": bid2, "client": me})
            # Result(e)
            for i in range(2):
                msg = take({"tag": "e", "client": me})
                add("%sつ目の注文：" % (i+1), "#info")
                # win
                if msg["get"] == 0:
                    add("国債を%s円で取得できました。<br />" % msg["price"], "#info")
                    add("購入した国債を共通価格%s円で売り、%s円の利益を得ました。<br />" % (value, value-msg["price"]), "#info")
                    profit += value-msg["price"]
                # lose
                else:
                    add("国債を取得できませんでした。<br />", "#info")
            # Information(f)
            waitinfohide(2*(time+1) - 1)
            add("<p>あなたの合計利潤は%s円になりました。</p>" % profit, "#info")
            msg = take({"tag": "f"})
            add("<p>このラウンドにおける<br />勝ち入札の平均入札額：%s円<br />共通価値：%s円</p>" % (msg["ave"], value), "#info")
            let(profit, "#profit")
            # Next Round(g)
            if time != Round-1:
                nextTA(time)
                take({"client": me})
                nextTAhide(time)
                put({"tag": "g"})
                waitinfo(2*(time+1))
            else:
                add("<p id='next%s'>結果発表にうつる準備ができましたら、"
                "ボタンを押してください。<br />"
                "<input id='go' type='submit'></p>" % time, "#info")
                take({"client": me})
                nextTAhide(time)
                # Put Profit(g)
                put({"tag": "g", "client": me, "profit": profit})
                waitinfo(2*(time+1))
                # Take Result(h)
                msg = take({"tag": "h"})
                let("", "#info")
                result = msg["result"]
                for i in range(plnum):
                    add("%s位：被験者No.%s, %s円<br />" % (i+1, result[i]["client"], result[i]["profit"]), "#info")
        add("<p>これで実験を終了します。</p>", "#info")

run(session)
