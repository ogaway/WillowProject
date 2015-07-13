# -*- coding: utf-8 -*-﻿
from willow.willow import *
from wifunc_v2 import *


def session(me):
    # 0 : The First Price Auction
    # 1 : Vickrey Auction
    # 2 : The Reference Rule Auction
    auction = 1
    Round = 3

    if me == 0:
        # 変数のセット
        plnum = 0
        i1list = []
        i2list = []
        jlist = []
        i1bid = 0
        i2bid = 0
        jbid = 0
        i1num = 0
        i2num = 0
        jnum = 0
        i1price = 0
        i2price = 0
        jprice = 0
        revenue = 0
        add(open("web/index.html"))
        add("Auction For Complements : Monitor Display<br />", "#catch")
        add("パッケージ付きオークション 実験者", "#catch")
        # Initial Setting
        # Player Number
        numset()
        take({"id": "go"})
        plnum = get_num()
        numset_end(plnum)
        wait(1)
        # Open the Datasets
        f1 = open('data/data1.csv', 'rb')
        f2 = open('data/data2.csv', 'rb')
        f3 = open('data/data3.csv', 'rb')
        dataReader1 = csv.reader(f1)
        dataReader2 = csv.reader(f2)
        dataReader3 = csv.reader(f3)
        i1list = [row for row in dataReader1]
        i2list = [row for row in dataReader2]
        jlist = [row for row in dataReader3]
        # Instruction(a)
        for i in range(len(i1list[0])):
            put({"tag": "a", "type": "i1", "plnum": plnum})
        for i in range(len(i2list[0])):
            put({"tag": "a", "type": "i2", "plnum": plnum})
        for i in range(len(jlist[0])):
            put({"tag": "a", "type": "j", "plnum": plnum})
        # Ready to start(b)
        for i in range(plnum):
            take({"tag": "b"})
        waithide(1)
        start(1)
        take({"client": me})
        starthide(1)
        add("<h2>実験開始</h2>", "#main")
        log("mechanism", "is", auction)
        # Start!(c)
        for time in range(Round):
            add("<h2>第%sラウンド</h2>" % (time+1), "#main")
            # Reset variables
            i1s = i1list[time]
            i2s = i2list[time]
            js = jlist[time]
            i1bid = 0
            i2bid = 0
            jbid = 0
            i1price = 0
            i2price = 0
            jprice = 0
            i1num = 0
            i2num = 0
            jnum = 0
            averagebid = 0
            averageprice = 0
            info = []
            print i1s, i2s
            # Put Value and Estimates(c)
            for i in range(len(i1s)):
                put({"tag": "c", "type": "i1", "v": int(i1s[i])})
            for i in range(len(i2s)):
                put({"tag": "c", "type": "i2", "v": int(i2s[i])})
            for i in range(len(js)):
                put({"tag": "c", "type": "j", "v": int(js[i])})
            # Take Bids(d)
            add("Take Bids<br />", "#main")
            for i in range(plnum):
                msg = take({"tag": "d"})
                add("タイプ%s被験者No.%sが%s円の入札を行いました。<br />" % (msg["type"], msg["client"], msg["bid"]), "#main")
                if msg["type"] == "i1":
                    if int(msg["bid"]) > i1bid:
                        i1bid = int(msg["bid"])
                        i1num = int(msg["client"])
                elif msg["type"] == "i2":
                    if int(msg["bid"]) > i2bid:
                        i2bid = int(msg["bid"])
                        i2num = int(msg["client"])
                elif msg["type"] == "j":
                    if int(msg["bid"]) > jbid:
                        jbid = int(msg["bid"])
                        jnum = int(msg["client"])
            # Allocation and Price(e)
            add("Allocation and Price<br />", "#main")
            # 0 : The First Price Auction
            if auction == 0:
                if i1bid + i2bid > jbid:
                    add("Itype1被験者No.%sが%s円で財１を、Itype2被験者No.%sが%s円で財２を落札しました。<br />"
                     % (i1num, i1bid, i2num, i2bid), "#main")
                    log("winner", "seller", i1bid + i2bid)
                    revenue += i1bid + i2bid
                    for i in range(plnum):
                        put({"tag": "e", "win":"i", "i1num":i1num, "i1price":i1bid,
                        "i2num":i2num, "i2price":i2bid, "client": i+1})
                else:
                    add("Jtype被験者No.%sが%s円で財１・財２を落札しました。<br />" % (jnum, jbid), "#main")
                    log("winner", "seller", jbid)
                    revenue += jbid
                    for i in range(plnum):
                        put({"tag": "e", "win":"j", "jnum":jnum, "jprice":jbid, "client": i+1})
            # 1 : Vickrey Auction
            if auction == 1:
                if i1bid + i2bid > jbid:
                    i1price = max(jbid - i2bid, 0)
                    i2price = max(jbid - i1bid, 0)
                    add("Itype1被験者No.%sが%s円で財１を、Itype2被験者No.%sが%s円で財２を落札しました。<br />"
                    "価格は財1が%s円、財2が%s円に決まりました。<br />"
                     % (i1num, i1bid, i2num, i2bid, i1price, i2price), "#main")
                    log("winner", "seller", i1price + i2price)
                    revenue += i1price + i2price
                    for i in range(plnum):
                        put({"tag": "e", "win":"i", "i1num":i1num, "i1price":i1price,
                        "i2num":i2num, "i2price":i2price, "client": i+1})
                else:
                    jprice = i1bid + i2bid
                    add("Jtype被験者No.%sが%s円で財１・財２を落札しました。<br />"
                    "価格は%s円に決まりました。<br />" % (jnum, jbid, jprice), "#main")
                    log("winner", "seller", jprice)
                    revenue += jprice
                    for i in range(plnum):
                        put({"tag": "e", "win":"j", "jnum":jnum, "jprice":jprice, "client": i+1})
            # 2 : The Reference Rule Auction
            if auction == 2:
                if i1bid + i2bid > jbid:
                    if jbid % 2 == 0:
                        i1price = jbid/2
                        i2price = jbid/2
                    else:
                        i1price = (jbid + 1)/2
                        i2price = (jbid + 1)/2
                    add("Itype1被験者No.%sが%s円で財１を、Itype2被験者No.%sが%s円で財２を落札しました。<br />"
                    "価格は財1が%s円、財2が%s円に決まりました。<br />"
                     % (i1num, i1bid, i2num, i2bid, i1price, i2price), "#main")
                    log("winner", "seller", i1price + i2price)
                    revenue += i1price + i2price
                    for i in range(plnum):
                        put({"tag": "e", "win":"i", "i1num":i1num, "i1price":i1price,
                        "i2num":i2num, "i2price":i2price, "client": i+1})
                else:
                    jprice = i1bid + i2bid
                    add("Jtype被験者No.%sが%s円で財１・財２を落札しました。<br />"
                    "価格は%s円に決まりました。<br />" % (jnum, jbid, jprice), "#main")
                    log("winner", "seller", jprice)
                    revenue += jprice
                    for i in range(plnum):
                        put({"tag": "e", "win":"j", "jnum":jnum, "jprice":jprice, "client": i+1})
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
                wiput(plnum, {"tag": "h", "result": result, "revenue": revenue})
                add("<h2>結果発表</h2>", "#main")
                for i in range(plnum):
                    add("%s位：被験者No.%s, %s円<br />" % (i+1, result[i]["client"], result[i]["profit"]), "#main")
                add("収益：%s円<br />" % (revenue), "#main")
        add("<p>これで実験を終了します。</p>", "#main")

    else:
        add(open("web/index.html"))
        add("Auction For Complements ： Participants Display<br />", "#catch")
        add("パッケージオークション 参加者No.%s" % me, "#catch")
        wait(1)
        # Instruction(a)
        msg = take({"tag": "a"})
        waithide(1)
        mytype = msg["type"]
        plnum = msg["plnum"]
        if mytype == "i1":
            add(open("AFC_Itype1.html"), "#main")
        elif mytype == "i2":
            add(open("AFC_Itype2.html"), "#main")
        elif mytype == "j":
            add(open("AFC_Jtype.html"), "#main")
        if auction == 0:
            add(open("FP.html"), "#instruction")
        elif auction == 1:
            add(open("VA.html"), "#instruction")
        elif auction == 2:
            add(open("RR.html"), "#instruction")
        # Ready to start(b)
        ready()
        take({"client": me})
        put({"tag": "b"})
        hide("#ready")
        wait(2)
        # Start!(c)
        profit = 0
        for time in range(Round):
            counter = 0
            msg = take({"tag": "c", "type": mytype})
            if time == 0:
                waithide(2)
                hide("#instruction")
                add("<h2>情報板</h2>"
                "<p>タイプ：%s</p>"
                "<p>ラウンド数：第<span id='roundnum'>1</span>ラウンド</p>"
                "<p>現在の合計利潤：<span id='profit'>0</span>円</p>"
                "<p id='info'></p>" % mytype, "#experiment")
            elif time >= 1:
                let(time+1, "#roundnum")
                waitinfohide(2*time)
                boardhide(time-1)
            board_AFC(time)
            value = msg["v"]
            add(value, "#value%s" % time)
            let("入札価格記入欄に価格を入力して送信してください。", "#info")
            while True:
                bid_AFC(time, counter)
                take({"client": me})
                bid = peek("#%sbid%s" % (time, counter))
                if bid.isdigit():
                    bid = int(bid)
                    if (bid >= 0) and (bid <= 200):
                        let("", "#info")
                        log(value, mytype, bid)
                        break
                    else:
                        counter += 1
                        let("<font color='red'>入札価格は注意書きに従った金額を入力してください。</font>", "#info")
                else:
                    counter += 1
                    let("<font color='red'>入札価格は注意書きに従った金額を入力してください。</font>", "#info")
            hide("#offer%s" % time)
            waitinfo(2*(time+1) - 1)
            # Submit Bids(d)
            put({"tag": "d", "type": mytype, "bid": bid, "client": me})
            # Result(e)
            msg = take({"tag": "e", "client": me})
            if msg["win"] == "i":
                add("Itype1被験者No.%sが%s円で財１を、Itype2被験者No.%sが%s円で財２を落札しました。<br />"
                 % (msg["i1num"], msg["i1price"], msg["i2num"], msg["i2price"]), "#info")
                if me == msg["i1num"]:
                    add("私的価値%s円と取得価格との差分の%s円の効用を得ました。<br />" % (value, value-msg["i1price"]), "#info")
                    profit += value-msg["i1price"]
                    log("winner", "i1type", profit)
                elif me == msg["i2num"]:
                    add("私的価値%s円と取得価格との差分の%s円の効用を得ました。<br />" % (value, value-msg["i2price"]), "#info")
                    profit = value - msg["i2price"]
                    log("winner", "i2type", profit)
                else:
                    add("財を取得できませんでした。<br />", "#info")
                    profit += 0
            elif msg["win"] == "j":
                add("Jtype被験者No.%sが%s円で財１・財２を落札しました。<br />" % (msg["jnum"], msg["jprice"]), "#info")
                if me == msg["jnum"]:
                    add("私的価値%s円と取得価格との差分の%s円の効用を得ました。<br />" % (value, value-msg["jprice"]), "#info")
                    profit = value - msg["jprice"]
                    log("winner", "jtype", profit)
                else:
                    add("財を取得できませんでした。<br />", "#info")
                    profit += 0
            # Information(f)
            waitinfohide(2*(time+1) - 1)
            add("<p>あなたの合計利潤は%s円になりました。</p>" % profit, "#info")
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
                add("売り手の合計収益：%s円<br />" % (msg["revenue"]), "#info")
        add("<p>これで実験を終了します。</p>", "#info")

run(session)
