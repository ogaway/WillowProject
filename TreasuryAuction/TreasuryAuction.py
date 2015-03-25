# coding: UTF-8
from willow.willow import *
from wifunc_v1 import *
import numpy as np
import random

"""
現在の目立つ不備
①量が反映されない
②共通価値と購入価格の差で利益を出せていない
③実験説明がない
"""

def session(me):
    if me == 0:
        add("<h1>国債オークション モニター</h1>")
        # 初期設定
        numset()
        take({"client": me})
        plnum = get_num()
        numset_end(plnum)
        wiput(plnum, {"tag": "a"})
        wait(1)
        witake(plnum, {"tag": "b"})
        waithide(1)
        start()
        take({"client": me})
        hide("#start")
        # 実験開始
        cvalue = random.randint(100, 900)  # 共通価値設定
        info = []                          # ビッド情報保存リスト
        get = []                           # 国債取得者Noリスト
        # 実験開始タグ(c)
        wiput(plnum, {"tag": "c", "cv": cvalue})
        # ビッド受け取り(d)
        for i in range(plnum):
            msg = take({"tag": "d"})
            info.append(msg)               # infoに情報収納
        # ビッド額の順にinfoをソートする
        info = sorted(info, key=lambda x:x["bid"], reverse=True)
        # 国債の枚数分をソートしたinfoの上からgetリストに入れる。
        # 国債の取得可否タグ(e)
        # ---
        # 国債の枚数をplnum/2にしてるけど後々偶数奇数でわけたりするべきかも
        # ---
        for i in range(plnum/2):
            get.append(info[i]["client"])
            put({"tag": "e", "client": info[i]["client"], "get": 0, "price": info[i]["bid"]})
            add("%sは国債を落札しました。" % info[i]["client"])
        for i in range(plnum/2, plnum):
            put({"tag": "e", "client": info[i]["client"], "get": 1, "price": info[i]["bid"]})
            add("%sは国債を落札できませんでした。" % info[i]["client"])

        add("<p>これで実験を終了します。</p>")
    # 誰がどれくらいのビッドをしたのかもモニター画面に表示するようにしなきゃ。。
    # あとこれだと国債を購入する量がまだ反映できてない。。。

    else:
        add("<h1>国債オークション クライアントNo.%s</h1>" % me)
        wait(1)
        # 実験説明開始(a)
        take({"tag": "a"})
        waithide(1)
        add(open("TAsubject.html"))
        ready()
        # 実験内容把握(b)
        take({"client": me})
        put({"tag": "b"})
        hide("#ready")
        wait(2)
        # 実験開始(c)
        msg = take({"tag": "c"})
        waithide(2)
        show("#start")
        cvalue = msg["cv"]
        svalue = random.randint(cvalue-200, cvalue+200)
        add(svalue, "#svalue")
        take({"client": me})
        quan = int(peek("#quan"))
        bid = int(peek("#bid"))
        hide("#offer")
        wait(3)
        # 注文送信(d)
        put({"tag": "d", "quan": quan, "bid": bid, "client": me})
        # 結果受信(e)
        msg = take({"tag": "e", "client": me})
        if msg["get"] == 0:
            add("国債を%s円で取得できました。" % msg["price"])
        else:
            add("国債を取得できませんでした。")
        waithide(3)
        add("<p>これで実験を終了します。</p>", "#info")

run(session)
