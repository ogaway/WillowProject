# -*- coding: utf-8 -*-﻿
from willow.willow import *
from wifunc import *
import random


def session(me):
    if me == 0:
        # 変数のセット
        plnum = 0
        buylist = []
        selllist = []
        buyprice = 0
        sellprice = 1000000
        buynum = 0
        sellnum = 0
        group = []

        # 初期設定
        add(open("DAmonitor_01.html"))
        take({"id": "go"})
        hide("#numset")
        show("#numsetcomp")
        plnum = int(peek("#plnum"))
        add(plnum, "#num")
        show("#priceset")
        priceset(plnum)
        take({"id": "go"})
        hide("#priceset")
        show("#pricesetcomp")
        pricesetcomp(plnum, buylist, selllist)
        wait(1)
        for i in range(len(buylist)):
            put({"tag": "tc", "type": "buy", "value": "%s" % buylist[i]})
        for i in range(len(selllist)):
            put({"tag": "tc", "type": "sell", "value": "%s" % selllist[i]})

        # 実験開始
        for i in range(plnum):
            take({"tag": "tm"})
        waithide(1)
        start()
        take({"client": me})
        hide("#start")
        show("#auction")
        for i in range(plnum):
            put({"tag": "tc0"})
        for i in range(plnum):
            group.append(i+1)
        counter = 0
        while True:
            if len(group) <= 1:
                add("実験を終了します。<br />", "#info")
                for i in range(plnum):
                    put({"tag": "tc1", "if": 1})
                break
            else:
                # step1 ランダムに当てて価格を聞く
                random.shuffle(group)
                client = group[0]
                for i in range(plnum):
                    put({"tag": "tc1", "if": 2, "client": client})

                # step2 板情報を更新
                # 取引成立するパターンと取引成立しないパターンの２通りを書く
                msg = take({"tag": "tm"})
                for i in range(plnum):
                    put({"tag": "tc2", "type": msg["type"], "price": msg["price"], "bidder": msg["client"]})
                if msg["type"] == "buy":
                    buyprice = int(msg["price"])
                    buynum = client
                    let(buyprice, "#buyprice")
                    let(buynum, "#buynum")
                    add("クライアント%sが%s円で買値を提示しました。<br />"
                     % (client, msg["price"]), "#info")
                if msg["type"] == "sell":
                    sellprice = int(msg["price"])
                    sellnum = client
                    let(sellprice, "#sellprice")
                    let(sellnum, "#sellnum")
                    add("クライアント%sが%s円で売値を提示しました。<br />"
                     % (client, msg["price"]), "#info")
                if buyprice < sellprice:
                    for i in range(plnum):
                        put({"tag": "tc3", "if": 2})
                    for i in range(plnum):
                        msg = take({"tag": "tm"})
                        if msg["client"] in group:
                            if int(msg["deci"]) == 2:
                                a = group.index(int(msg["client"]))
                                group.pop(a)
                                add("クライアント%sは取引を降りました。<br />" % msg["client"], "#info")
                if buyprice >= sellprice:
                    add("クライアント%sとクライアント%sの間で%s円での取引が成立しました。<br />"
                     % (buynum, sellnum, sellprice), "#info")
                    add("次の取引へうつります。<br />", "#info")
                    for i in range(plnum):
                        put({"tag": "tc3", "if": 1, "buynum": buynum, "sellnum": sellnum, "price": sellprice})
                    buyprice = 0
                    sellprice = 1000000
                    buynum = 0
                    sellnum = 0
                    group = []
                    for i in range(plnum):
                        group.append(i+1)
                    let("入札なし", "#sellprice")
                    let("入札なし", "#buyprice")
                    let("入札なし", "#sellnum")
                    let("入札なし", "#buynum")
                    for i in range(plnum):
                        take({"tag": "tm"})

    else:
        add(open("DAsubject_01.html"))
        add("No.%s" % me, "#num")
        wait(1)

        # id="inst"
        msg = take({"tag": "tc"})
        waithide(1)
        show("#inst")
        type = msg["type"]
        value = msg["value"]
        if type == "buy":
            add("買い手", "#type")
            add(value, "#value")
            show("#buyside")
        if type == "sell":
            add("売り手", "#type")
            add(value, "#value")
            show("#sellside")
        take({"client": me})
        hide("#instBT")
        show("#instBTcomp")
        put({"tag": "tm", "number": me})

        # id="auction"
        take({"tag": "tc0"})
        hide("#inst")
        show("#auction")
        if type == "buy":
            add("買い手", "#type2")
            add(value, "#value2")
        if type == "sell":
            add("売り手", "#type2")
            add(value, "#value2")

        counter = 0
        while True:
            msg = take({"tag": "tc1"})
            waithide(counter-1, 2)

            # 取引者がいなくなったらループから出る
            if msg["if"] == 1:
                add("取引に残った人が１人以下となったので実験を終了します。<br />", "#info")
                break

            # step1　ランダムに当てて価格を聞く
            if msg["if"] == 2:
                add("<p id='c1step%s'>被験者をランダムに当てた結果、"
                "今回は被験者No.<span id='client%s'></span>"
                "が指名されました。</p>" % (str(counter), str(counter)), "#info")
                add(msg["client"], "#client%s" % str(counter))
                if me == msg["client"]:
                    add("<p id='Tc1step%s'>価格を掲示してください。<br />"
                    "<input class='num' id='pricesug%s' type='text' /><br />"
                    "<input id='go' type='submit'></p>" % (str(counter), str(counter)), "#info")
                    take({"id": "go"})
                    hide("#Tc1step%s" % str(counter))
                    wait(counter, 1)
                    put({"tag": "tm", "type": type, "price": peek("#pricesug%s" % str(counter)), "client": me})
                else:
                    wait(counter, 1)

                # step2 板情報を更新
                msg = take({"tag": "tc2"})
                hide("#c1step%s" % str(counter))
                waithide(counter, 1)
                if msg["type"] == "buy":
                    let(msg["price"], "#buyprice")
                    let(msg["bidder"], "#buynum")
                if msg["type"] == "sell":
                    let(msg["price"], "#sellprice")
                    let(msg["bidder"], "#sellnum")

                # step3 新たな価格を提示したい人を募集する
                msg = take({"tag": "tc3"})
                if msg["if"] == 1:
                    if msg["buynum"] == me:
                        let("売り手", "#type2")
                        let(str(int(value) - int(msg["price"])), "#profit")
                    if msg["sellnum"] == me:
                        let("買い手", "#type2")
                        let(str(int(msg["price"]) - int(value)), "#profit")
                    add("<p id='c3step%s'>"
                    "クライアント%sとクライアント%sの間で%s円での取引が成立しました。<br />"
                    "次の取引へうつります。ボタンを押してください。<br />"
                    "<input id='go' type='submit'></p>"
                    % (str(counter), msg["buynum"], msg["sellnum"], msg["price"]), "#info")
                    take({"client": me})
                    put({"tag": "tm"})
                    hide("#c3step%s" % str(counter))
                    wait(counter, 2)
                    let("入札なし", "#sellprice")
                    let("入札なし", "#buyprice")
                    let("入札なし", "#sellnum")
                    let("入札なし", "#buynum")
                if msg["if"] == 2:
                    add("<p id='c3step%s'>"
                    "価格が更新されました。"
                    "買値と売値がまだ一致していないので新しい価格を掲示する人を募集します。<br />"
                    "どちらかのボタンを押してください。"
                    "※一度取引から降りるとその取引にもう一度入ることは出来なくなります。<br />"
                    "<input id='1' type='submit' value='価格を掲示'><br />"
                    "<input id='2' type='submit' value='取引から降りる'><br /></p>" % str(counter), "#info")
                    msg = take({"client": me})
                    put({"tag": "tm", "deci": msg["id"], "client": me})
                    hide("#c3step%s" % str(counter))
                    wait(counter, 2)
                counter = counter + 1


run(session)
