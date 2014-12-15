# -*- coding: utf-8 -*-﻿
from willow.willow import *
from wifunc import *


def session(me):
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
        pricemechanism = 2
        # 0 : The First Price Auction
        # 1 : Vickrey Auction
        # 2 : The Reference Rule Auction
        add("<h1>Auction For Complements モニター</h1>")
        add("<h2>初期設定</h2>")
        # 被験者人数設定
        numset()
        take({"id": "go"})
        plnum = get_num()
        numset_end(plnum)
        # 私的価値設定
        AFCpriceset(plnum)
        take({"id": "go"})
        AFCpriceset_end(plnum, i1list, i2list, jlist)
        wait(1)
        for i in range(len(i1list)):
            put({"tag": "tc", "prmech":pricemechanism, "type": "i1", "value": "%s" % i1list[i]})
        for i in range(len(i2list)):
            put({"tag": "tc", "prmech":pricemechanism, "type": "i2", "value": "%s" % i2list[i]})
        for i in range(len(jlist)):
            put({"tag": "tc", "prmech":pricemechanism, "type": "j", "value": "%s" % jlist[i]})
        # 実験開始
        for i in range(plnum):
            take({"tag": "tm"})
        waithide(1)
        start()
        take({"client": me})
        hide("#start")
        add("<h2>実験開始</h2>")
        log("mechanism", "type", "bid")
        for i in range(plnum):
            put({"tag": "tc0"})
        for i in range(plnum):
            msg = take({"tag": "tm"})
            add("タイプ%s被験者No.%sが%s円の入札を行いました。<br />" % (msg["type"], msg["client"], msg["price"]))
            log(pricemechanism, msg["type"], msg["price"])
            if msg["type"] == "i1":
                if msg["price"] > i1bid:
                    i1bid = int(msg["price"])
                    i1num = int(msg["client"])
            elif msg["type"] == "i2":
                if msg["price"] > i2bid:
                    i2bid = int(msg["price"])
                    i2num = int(msg["client"])
            elif msg["type"] == "j":
                if msg["price"] > jbid:
                    jbid = int(msg["price"])
                    jnum = int(msg["client"])
        # 0 : The First Price Auction
        if pricemechanism == 0:
            if i1bid + i2bid > jbid:
                add("Itype1被験者No.%sが%s円で財１を、Itype2被験者No.%sが%s円で財２を落札しました。<br />"
                 % (i1num, i1bid, i2num, i2bid))
                log("winner", "seller", i1bid + i2bid)
                for i in range(plnum):
                    put({"tag": "tc1", "win":"i", "i1num":i1num, "i1price":i1bid,
                    "i2num":i2num, "i2price":i2bid})
            else:
                add("Jtype被験者No.%sが%s円で財１・財２を落札しました。<br />" % (jnum, jbid))
                log("winner", "seller", jbid)
                for i in range(plnum):
                    put({"tag": "tc1", "win":"j", "jnum":jnum, "jprice":jbid})
        # 1 : Vickrey Auction
        if pricemechanism == 1:
            if i1bid + i2bid > jbid:
                i1price = max(jbid - i2bid, 0)
                i2price = max(jbid - i1bid, 0)
                add("Itype1被験者No.%sが%s円で財１を、Itype2被験者No.%sが%s円で財２を落札しました。<br />"
                "価格は財1が%s円、財2が%s円に決まりました。<br />"
                 % (i1num, i1bid, i2num, i2bid, i1price, i2price))
                log("winner", "seller", i1price + i2price)
                for i in range(plnum):
                    put({"tag": "tc1", "win":"i", "i1num":i1num, "i1price":i1price,
                    "i2num":i2num, "i2price":i2price})
            else:
                jprice = i1bid + i2bid
                add("Jtype被験者No.%sが%s円で財１・財２を落札しました。<br />"
                "価格は%s円に決まりました。<br />" % (jnum, jbid, jprice))
                log("winner", "seller", jprice)
                for i in range(plnum):
                    put({"tag": "tc1", "win":"j", "jnum":jnum, "jprice":jprice})
        # 2 : The Reference Rule Auction
        if pricemechanism == 2:
            if i1bid + i2bid > jbid:
                if jbid % 2 == 0:
                    i1price = jbid/2
                    i2price = jbid/2
                else:
                    i1price = (jbid + 1)/2
                    i2price = (jbid + 1)/2
                add("Itype1被験者No.%sが%s円で財１を、Itype2被験者No.%sが%s円で財２を落札しました。<br />"
                "価格は財1が%s円、財2が%s円に決まりました。<br />"
                 % (i1num, i1bid, i2num, i2bid, i1price, i2price))
                log("winner", "seller", i1price + i2price)
                for i in range(plnum):
                    put({"tag": "tc1", "win":"i", "i1num":i1num, "i1price":i1price,
                    "i2num":i2num, "i2price":i2price})
            else:
                jprice = i1bid + i2bid
                add("Jtype被験者No.%sが%s円で財１・財２を落札しました。<br />"
                "価格は%s円に決まりました。<br />" % (jnum, jbid, jprice))
                log("winner", "seller", jprice)
                for i in range(plnum):
                    put({"tag": "tc1", "win":"j", "jnum":jnum, "jprice":jprice})
        for i in range(plnum):
            msg = take({"tag":"tm2"})
            add("被験者No.%sの利潤は%s円でした。<br />" % (msg["client"], msg["profit"]))
        add("以上で実験を終了します。")

    else:
        add("<h1>Auction For Complements 被験者No.%s</h1>" % me)
        wait(1)
        msg = take({"tag": "tc"})
        waithide(1)
        add("<h2>実験内容について</h2>")
        type = msg["type"]
        value = int(msg["value"])
        pricemechanism = msg["prmech"]
        if type == "i1":
            add(open("AFC_Itype1.html"))
        elif type == "i2":
            add(open("AFC_Itype2.html"))
        elif type == "j":
            add(open("AFC_Jtype.html"))
        if pricemechanism == 0:
            add(open("FP.html"))
        elif pricemechanism == 1:
            add(open("VA.html"))
        elif pricemechanism == 2:
            add(open("RR.html"))
        add(value, "#value")
        ready()
        take({"client": me})
        put({"tag": "tm", "number": me})
        hide("#ready")
        wait(2)
        #実験開始
        take({"tag": "tc0"})
        waithide(2)
        add("<h2>実験開始</h2>")
        add("<div id='auc'><p>価格を入力して入札してください。"
        "<input id='price' type='text' />円<br />"
        "<input id='go' type='submit'></p></div>")
        take({"client": me})
        hide("#auc")
        wait(3)
        put({"tag": "tm", "type": type, "price": peek("#price"), "client": me})
        msg = take({"tag":"tc1"})
        waithide(3)
        if msg["win"] == "i":
            add("Itype1被験者No.%sが%s円で財１を、Itype2被験者No.%sが%s円で財２を落札しました。<br />"
             % (msg["i1num"], msg["i1price"], msg["i2num"], msg["i2price"]))
            if me == msg["i1num"]:
                profit = value - msg["i1price"]
                log("winner", "i1type", profit)
            elif me == msg["i2num"]:
                profit = value - msg["i2price"]
                log("winner", "i2type", profit)
            else:
                profit = 0
        elif msg["win"] == "j":
            add("Jtype被験者No.%sが%s円で財１・財２を落札しました。<br />" % (msg["jnum"], msg["jprice"]))
            if me == msg["jnum"]:
                profit = value - msg["jprice"]
                log("winner", "jtype", profit)
            else:
                profit = 0
        put({"tag": "tm2", "profit": profit, "client": me})
        add("あなたの利潤は%s円でした。" % profit)
        add("以上で実験を終了します。")


run(session)
