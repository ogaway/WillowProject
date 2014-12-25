# coding: UTF-8
from willow.willow import *
from wifunc import *


def session(me):
    if me == 0:
        add("<h1>公共財供給実験 モニター</h1>")
        add("<h2>初期設定</h2>")
        numset()
        take({"id": "go"})
        plnum = get_num()
        numset_end(plnum)
        wiput(plnum, {"tag": "c1", "plnum": plnum})
        add("投資額<br />")
        allinv = 0
        for i in range(plnum):
            msg = take({"tag": "m1"})
            allinv += msg["invest"]
            add("No.%s:%s円<br />" % (msg["client"], msg["invest"]))
        effect = round(allinv*0.7, 3)
        add("<br />投資額合計:%s円<br />" % allinv)
        add("1人あたりメリット:%s円<br />" % effect)
        wiput(plnum, {"tag": "c2", "effect": effect, "allinv": allinv})
        add("<br />利得<br />")
        log("Plnum", "Invest", "Gain")
        for i in range(plnum):
            msg = take({"tag": "m2"})
            add("No.%s:%s円<br />" % (msg["client"], msg["gain"]))
            log(msg["client"], msg["invest"], msg["gain"])
        add("<p>これで実験を終了します。</p>")

    else:
        add("<h1>公共財供給実験 クライアントNo.%s</h1>" % me)
        wait(1)
        msg = take({"tag": "c1"})
        plnum = msg["plnum"]
        waithide(1)
        add(open("publicgoods.html"))
        add(plnum, "#num1")
        add(plnum, "#num2")
        add(plnum*700, "#money")
        take({"client": me})
        hide("#form1")
        invest = int(peek("#invest"))
        add("<p>あなたは%s円の投資をし、手元に%s円残しました。" % (invest, 1000-invest))
        wait(2)
        put({"tag": "m1", "invest": invest, "client": me})
        msg = take({"tag": "c2"})
        effect = msg["effect"]
        allinv = msg["allinv"]
        gain = 1000 - invest + effect
        waithide(2)
        put({"tag": "m2", "client": me, "invest": invest, "gain": gain})
        add("<p>公共財に計%s円が集まり、1人%s円のメリットが出ました。</p>" % (allinv, effect))
        add("<p>あなたの利得は%s円です。</p>" % gain)
        add("<p>これで実験を終了します。</p>")

run(session)
