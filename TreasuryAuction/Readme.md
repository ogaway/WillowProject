Treasury Auction
=====

使い方
=====
ディレクトリ構造
-----
TreasuryAuction  
  |--willow  
  |     |--willow.py  
  |     |  ...  
  |  
  |--log  
  |--data  
  |--web  
  |     |--css  
  |     |     |--base.css  
  |     |--img  
  |     |     |--favicon.ico  
  |     |     |--oyamalogo.png  
  |     |--index.html  
  |     |--TAsubject_DESC.html  
  |     |--TAsubject_UNI.html  
  |     |--TAsubject_SPAN.html
  |--TreasuryAuction.py  
  |--TAdataset.py  
  |--wifunc_v2.py  
  |--wifunc_TA.py  
  |--Readme.md  

・logフォルダ、dataフォルダは中身は空で構いません。(ここにデータが生成されるのでフォルダは作っておいてください。)  

実験を始める前に
-----
実験参加者人数と実験ラウンド数を決めたら、まずそれに応じたデータセットを生成します。  
(生成手順)  
・TAdataset.pyで実験参加者人数(plnum)と実験ラウンド数(Round)を設定して、共通価値とその予想価格のデータセットをランダムに生成する。  

実験を行う際に
-----
TAdataset.pyでデータを作成した時に設定した実験参加者人数(plnum)と実験ラウンド数を(Round)を設定して実験を開始する。  
※plnumはTreasuryAuction.pyを動かした後にブラウザ上で設定。  
 RoundはTreasuryAuction.pyを動かす前に直接コードを書き換えて設定してください。

実験を終えた後に
-----
実験を終えるとlogフォルダとdataフォルダにそれぞれファイルが生成されているので、分析に役立ててください。  
logフォルダには各ラウンドにおける平均落札価格、全ラウンド終了後における売り手の合計収益が記録されています。  
dataフォルダには１列目に共通価値、それ以降の列にその予想価格を記した行がラウンド数分書かれています。
