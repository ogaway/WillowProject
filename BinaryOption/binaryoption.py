# coding: UTF-8
from willow.willow import *
from wifunc import *
import numpy as np
from pandas import *
import matplotlib.pyplot as plt



def session(me):
    # 為替レートの推移を何回するか変更可能
    ts = 50
    if me == 0:
        add("<h1>バイナリーオプション モニター</h1>")
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
        wiput(plnum, {"tag": "c"})
        data = [100]
        time = [0]
        def ping():
            put({"client": me})
        wiput(plnum, {"tag": "d", "data": data[0], "time": time})
        plt.plot(time, data)
        plt.ylim( 90, 110)
        plt.xlim(0, 50)
        plt.savefig("img/image.png")
        add("<p id='info%s'>%s回目 : %s円</p>" % (0, 1, data[0]))
        add("<img id='img%s' src='img/image.png'>" % 0)
        background(ping, 4)
        take({"client": me})
        for i in range(ts-1):
            data.append(np.random.randn()+data[i])
            time.append(i+1)
            wiput(plnum, {"tag": "d", "data": data[i+1], "time": time})
            plt.plot(time, data, color="k")
            plt.savefig("img/image.png")
            hide("#info%s" % (i))
            hide("#img%s" % (i))
            add("<p id='info%s'>%s回目 : %s円</p>" % (i+1, i+2, data[i+1]))
            add("<img id='img%s' src='img/image.png'>" % (i+1))
            background(ping, 4)
            take({"client": me})
        add("<p>これで実験を終了します。</p>")

    else:
        add("<h1>バイナリーオプション クライアントNo.%s</h1>" % me)
        wait(1)
        # 実験説明開始(a)
        take({"tag": "a"})
        add(open("binary.html"))
        add(ts, "#ts1")
        add(ts-6, "#ts2")
        waithide(1)
        ready()
        # 実験内容把握(b)
        take({"client": me})
        put({"tag": "b"})
        hide("#ready")
        wait(2)
        # 実験開始(c)
        take({"tag": "c"})
        waithide(2)
        show("#start")
        # 関数,変数の準備
        def set_input(a):
            add("<p id='input%s'>賭金<input type='text' id='bet%s' >円<br />"
            "<input type='submit' value='円安(上方向)' id='0'>"
            "<input type='submit' value='円高(下方向)' id='1'></p>" % (a, a), "#info")
        def hide_input(a):
            hide("#input%s" % a)
        def ping():
            put({"id": 2, "client": me})
        def win(i, bet, all, profit):
            add("<p id='counter%s'>おめでとうございます！あなたは勝ちました。<br />"
            "掛け金の2倍の額が手元に入りました。</p>" % i, "#info")
            let(all, "#all")
            let(profit, "#profit")
        def lose(i, bet, all, profit):
            add("<p id='counter%s'>残念でした。あなたの負けです。<br />"
            "掛け金は全て没収されました。</p>" % i, "#info")
            let(all, "#all")
            let(profit, "#profit")
        data = []
        time = []
        all = 100000
        profit = 0
        counter = 0
        counter_input = 0
        bet = 0
        type = 0
        # 画面生成
        set_input(0)
        add(100000, "#all")
        add(0, "#profit")
        for i in range(ts):
            # レート情報受け取り(d)
            msg = take({"tag": "d"})
            data.append(msg["data"])
            time.append(msg["time"])
            # レート情報更新
            let(data[i], "#rate")
            let(i+1, "#number")
            hide("#img%s" % (i-1))
            add("<img id='img%s' src='img/image.png'>" % i)
            # 推移数が45を超えたら賭けは終了。
            if i == ts-5:
                hide_input(counter_input)
                add("<p>賭けの受付を終了しました。%s回目の推移が終わるまでお待ちください。</p>" % ts, "#info")
            # 賭けをするかどうか待機(既に賭けている場合は4秒待機)
            background(ping, 4)
            msg = take({"client": me})
            # 既に賭けている場合(if1_1)
            if counter >= 1 and counter <=5:
                hide("#counter%s" % (i-1))
                add("<p id='counter%s'>あと%s回目の推移で決定します。</p>" % (i, 6-counter), "#info")
                counter += 1
            # 賭けが勝ったか負けたか(if1_2)
            elif counter == 6:
                # 円安に賭けていた場合
                if type == 0:
                    if data[i-6] <= data[i]:
                        all += bet
                        profit += bet
                        win(i, bet, all, profit)
                    else:
                        all -= bet
                        profit -= bet
                        lose(i, bet, all, profit)
                # 円高に賭けていた場合
                elif type == 1:
                    if data[i-6] >= data[i]:
                        all += bet
                        profit += bet
                        win(i, bet, all, profit)
                    else:
                        all -= bet
                        profit -= bet
                        lose(i, bet, all, profit)
                counter = -1
                counter_input += 1
                hide("#counter%s" % (i-1))
                if i <= ts -6:
                    set_input(counter_input)
            # 賭けの次の推移でinfoからwin,loseを消す(if1_3)
            elif counter == -1:
                hide("#counter%s" % (i-1))
                hide("#betinfo%s" % (counter_input-1))
                counter = 0
            # 円安のボタンが押された場合(if2_1)
            if msg["id"] == "0":
                hide_input(counter_input)
                bet = int(peek("#bet%s" % counter_input))
                add("<p id='betinfo%s'>あなたは6回の推移後に為替レートが%s円の状態よりも"
                "円安(グラフで上方向)になるということに%s円賭けました。</p>" % (counter_input, data[i], bet), "#info")
                add("<p id='counter%s'>あと%s回目の推移で決定します。</p>" % (i, 6-counter), "#info")
                counter = 1
                type = 0
            # 円高のボタンが押された場合(if2_2)
            elif msg["id"] == "1":
                hide_input(counter_input)
                bet = int(peek("#bet%s" % counter_input))
                add("<p id='betinfo%s'>あなたは6回の推移後に為替レートが%s円の状態よりも"
                "円高(グラフで下方向)になるということに%s円賭けました。</p>" % (counter_input, data[i], bet), "#info")
                add("<p id='counter%s'>あと%s回目の推移で決定します。</p>" % (i, 6-counter), "#info")
                counter = 1
                type = 1
        add("<p>これで実験を終了します。</p>", "#info")

run(session)
