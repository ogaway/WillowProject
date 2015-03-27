# coding: UTF-8
from willow.willow import *
from wifunc_v2 import *
import numpy as np
import random

"""
現在の目立つ不備
①量が反映されない
→解決
②共通価値と購入価格の差で利益を出せていない
→解決
③実験説明がない
"""

def session(me):
    if me == 0:
        add("<h1>国債オークション モニター</h1>")
        # 初期設定
        # 人数設定
        numset()
        take({"client": me})
        plnum = get_num()
        numset_end(plnum)
        # 財の数設定
        goodsset()
        take({"client": me})
        goodsnum = get_goods()
        goodsset_end(goodsnum)
        # 実験説明(a)
        wiput(plnum, {"tag": "a"})
        wait(1)
        # 実験説明完了(b)
        witake(plnum, {"tag": "b"})
        waithide(1)
        # 実験開始準備
        start()
        take({"client": me})
        hide("#start")
        add("実験を開始します。<br />")
        # 実験開始
        # 変数設定
        cvalue = random.randint(100, 900)  # 共通価値設定
        info = []                          # ビッド情報保存リスト
        get = []                           # 国債取得者Noリスト
        quan = 0                           # 注文量
        # 実験開始タグ(c)
        wiput(plnum, {"tag": "c", "cv": cvalue})
        # ビッド受け取り(d)
        for i in range(plnum):
            msg = take({"tag": "d"})
            quan += msg["quan"]
            add("被験者No.%sは%s円の注文を%sつ出しました。<br />" % (msg["client"], msg["bid"], msg["quan"]))
            for i in range(msg["quan"]):
                info.append(msg)
        # ビッド額の順にinfoをソートする
        info = sorted(info, key=lambda x:x["bid"], reverse=True)

        auction = 0
        """
        ビッド額オークション
        ---
        自分のビッド額が直接価格として設定される。
        """
        if auction == 0:
            for i in range(goodsnum):
                put({"tag": "e", "client": info[i]["client"], "get": 0, "price": info[i]["bid"]})
                add("%sは国債を１つ落札しました。<br />" % info[i]["client"])
            for i in range(goodsnum, quan):
                put({"tag": "e", "client": info[i]["client"], "get": 1, "price": info[i]["bid"]})
                add("%sは国債を１つ落札できませんでした。<br />" % info[i]["client"])
        """
        均一価格オークション
        ---

        """
        # if auction == 1:




        """
        スペイン式オークション
        """
        # if auction == 2:

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
        profit = 0
        add(svalue, "#svalue")
        take({"client": me})
        quan = int(peek("#quan"))
        bid = int(peek("#bid"))
        hide("#offer")
        wait(3)
        # 注文送信(d)
        put({"tag": "d", "quan": quan, "bid": bid, "client": me})
        # 結果受信(e)
        for i in range(quan):
            msg = take({"tag": "e", "client": me})
            add("%s目の注文：" % (i+1))
            # 取得できた場合
            if msg["get"] == 0:
                add("国債を%s円で取得できました。<br />" % msg["price"])
                add("セカンダリーでその国債を%s円で売り、%s円の利益を得ました。<br />" % (cvalue, cvalue-msg["price"]))
                profit += cvalue-msg["price"]
            # 取得できなかった場合
            else:
                add("国債を取得できませんでした。<br />")
        # 結果発表
        waithide(3)
        add("あなたの合計利潤は%s円でした。" % profit)
        add("<p>これで実験を終了します。</p>", "#info")

run(session)
