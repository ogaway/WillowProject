# coding: UTF-8
from willow.willow import *
from wifunc import *

"""
ポイントは、"take"と"put"の使い方。willow使用中によく見た
どんどんコマンドが流れてくる画面(Board)がありますが、あそこを介し
辞書型データを各人が上手くやりとりすることで、必要な情報を
他人に送ったり、実験進行のタイミングを制御したりできる。
"""


def session(me):
    if me == 0:  # はじめにログインした人＝実験者
        # 太字のタイトル画面を設定
        add("<h1>公共財供給実験 モニター</h1>")
        add("<h2>初期設定</h2>")
        # 実験人数を入力させる。wifunc参照
        numset()
        # 実験人数が入力され、{"id": "go"}をもつ辞書が
        # アップされるまで、takeで待つ
        take({"client": me})
        # int型に変換して、実験者数をplnumに保存
        plnum = get_num()
        # 実験人数入力を削除し、画面に結果を表示
        numset_end(plnum)
        # Boardに、人数分以下の辞書を送信（wifunc)→被験者側が受け取る(a)
        wiput(plnum, {"tag": "a", "plnum": plnum})
        add("投資額<br />")
        # allinv = all investment
        allinv = 0
        # for内にtakeがあるので、待っています(b)。待ち終わったら、投資総額を計算
        for i in range(plnum):
            msg = take({"tag": "b%s" % (i+1)})
            allinv += msg["invest"]
            add("No.%s : %s円<br />" % (msg["client"], msg["invest"]))
        # 投資による利益を算出
        effect = int(allinv*0.7)
        add("<br />投資額合計 : %s円<br />" % allinv)
        add("1人あたりメリット : %s円<br />" % effect)
        # 指定された辞書で投資結果の情報をBoardに送り、被験者の待ちを解除(c)
        wiput(plnum, {"tag": "c", "effect": effect, "allinv": allinv})
        add("<br />利得<br />")
        # 結果保存時の、ラベルを記録しています
        log("Plnum", "Invest", "Gain")
        # takeで個別利得計算を待ってから、最終結果を記録します(d)
        for i in range(plnum):
            msg = take({"tag": "d%s" % (i+1)})
            add("No.%s : %s円<br />" % (msg["client"], msg["gain"]))
            log(msg["client"], msg["invest"], msg["gain"])
        add("<p>これで実験を終了します。</p>")

    else:  # その他の人＝被験者
        add("<h1>公共財供給実験 クライアントNo.%s</h1>" % me)
        # waitで待てと表示させ(wifunc)、takeで待機させます
        wait(1)
        # (a)の辞書がBoardにアップされるまで待機。アップされたらそれをmsgに保存
        msg = take({"tag": "a"})
        plnum = msg["plnum"]
        # 待て、の表示を取る(wifunc)
        waithide(1)
        # 別ファイルに保存されたhtmlを開く。"span"になっている部分ををさらにaddで埋めていく
        add(open("publicgoods.html"))
        add(plnum, "#num1")
        add(plnum, "#num2")
        add(plnum*700, "#money")
        # htmlファイルで、入力があるまでこのtakeで待ちます
        take({"client": me})
        # 入力が合ったのでhideでhtmlファイル内の入力画面を隠す
        hide("#form1")
        invest = int(peek("#invest"))
        add("<p>あなたは%s円の投資をし、手元に%s円残しました。</p>" % (invest, 1000-invest))
        wait(2)
        # putで辞書を送り、実験者側の待ちを解除します(b)
        put({"tag": "b%s" % me, "invest": invest, "client": me})
        # 実験者の処理を待ちます(c)。解除されたら、個別の利得計算を行う
        msg = take({"tag": "c"})
        effect = msg["effect"]
        allinv = msg["allinv"]
        gain = 1000 - invest + effect
        waithide(2)
        # 実験者の待ちを解除すべくputします(d)
        put({"tag": "d%s" % me, "client": me, "invest": invest, "gain": gain})
        add("<p>公共財に計%s円が集まり、1人%s円のメリットが出ました。</p>" % (allinv, effect))
        add("<p>あなたの利得は%s円です。</p>" % gain)
        add("<p>これで実験を終了します。</p>")

run(session)
