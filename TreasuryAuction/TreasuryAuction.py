# coding: UTF-8
from willow.willow import *
from wifunc_v2 import *
from wifunc_TA import *
import numpy as np
import random


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
    "auction" == 0:
        Spanish Designs
        Winning bids that are above the weighted average winning bid
        pay the same price; this price is equal to weighted average
        winning bid.
        On the other hand, winning bids that are below the weighted
        average winning bid are fully paid.
    ---
    """
    auction = 0

    if me == 0:
        add("<h1>Auctions for Government Securities : Monitor Display</h1>")

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
        start()
        take({"client": me})
        hide("#start")
        add("実験を開始します。<br />")

        # Start(c)
        # Variables Setting
        cvalue = random.randint(1000, 5000)
        info = []
        wiput(plnum, {"tag": "c", "cv": cvalue})
        # Receive the Bids(d)
        add("Receive the Bid<br />")
        for i in range(plnum):
            msg = take({"tag": "d"})
            add("被験者No.%sは%s円と%s円の注文を出しました。<br />" % (msg["client"], msg["bid1"], msg["bid2"]))
            info.append({"client": msg["client"], "bid": msg["bid1"]})
            info.append({"client": msg["client"], "bid": msg["bid2"]})
        # Ranked
        info = sorted(info, key=lambda x:x["bid"], reverse=True)
        add("Allocation and Price<br />")
        # Discriminatory Designs
        if auction == 0:
            for i in range(goodsnum):
                put({"tag": "e", "client": info[i]["client"], "get": 0, "price": info[i]["bid"]})
                add("被験者No.%sは%s円で国債を１つ落札しました。<br />" % (info[i]["client"], info[i]["bid"]))
            for i in range(goodsnum, len(info)):
                put({"tag": "e", "client": info[i]["client"], "get": 1, "price": info[i]["bid"]})
                add("被験者No.%sは国債を１つ落札できませんでした。<br />" % info[i]["client"])
        # Uniform Designs
        # if auction == 1:

        # Spanish Designs
        # if auction == 2:

        add("<p>これで実験を終了します。</p>")

    else:
        add("<h1>Auctions for Government Securities : Participants Display</h1>")
        add("<h1>国債オークション 参加者No.%s</h1>" % me)
        wait(1)
        # Instruction(a)
        msg = take({"tag": "a"})
        waithide(1)
        if auction == 0:
            add(open("TAsubject.html"))
            add(msg["plnum"], "#plnum")
            add(msg["goodsnum"], "#goodsnum1")
            add(msg["goodsnum"], "#goodsnum2")
            add(msg["goodsnum"], "#goodsnum3")
            add(msg["goodsnum"], "#goodsnum4")
        # elif auction == 1:
        # elif auction == 2:
        ready()
        # Ready to start(b)
        take({"client": me})
        put({"tag": "b"})
        hide("#ready")
        wait(2)

        # Start(c)
        msg = take({"tag": "c"})
        waithide(2)
        hide("#instruction")
        show("#start")
        cvalue = msg["cv"]
        svalue = random.randint(cvalue-200, cvalue+200)
        profit = 0
        add(svalue, "#svalue")
        let("入札価格記入欄に価格を入力して送信してください。", "#info")
        while True:
            take({"client": me})
            bid1 = int(peek("#bid1"))
            bid2 = int(peek("#bid2"))
            if (bid1 >= 500) and (bid1 <= 6000) and (bid2 >= 500 or bid2 == 0) and (bid2 <= 6000):
                let("", "#info")
                break
            else:
                let("<font color='red'>入札価格は注意書きに従った金額を入力してください。</font>", "#info")
        hide("#offer")
        waitinfo(1)
        # Submit Bids(d)
        put({"tag": "d", "bid1": bid1, "bid2": bid2, "client": me})
        # Result(e)
        for i in range(2):
            msg = take({"tag": "e", "client": me})
            add("%sつ目の注文：" % (i+1), "#info")
            # win
            if msg["get"] == 0:
                add("国債を%s円で取得できました。<br />" % msg["price"], "#info")
                add("購入した国債を共通価格%s円で売り、%s円の利益を得ました。<br />" % (cvalue, cvalue-msg["price"]), "#info")
                profit += cvalue-msg["price"]
            # lose
            else:
                add("国債を取得できませんでした。<br />", "#info")
        # Information
        waitinfohide(1)
        add("あなたの合計利潤は%s円でした。" % profit, "#info")
        add("<p>これで実験を終了します。</p>", "#info")

run(session)
