WillowProject
=======
* [Double Auction](https://github.com/yoshimasaogawa/WillowProject/tree/master/DoubleAuction)
* [Auctions For Complements](https://github.com/yoshimasaogawa/WillowProject/tree/master/AuctionForComplements)
* [Public Goods Game](https://github.com/yoshimasaogawa/WillowProject/tree/master/PublicGoodsGame)
* [Binary Option](https://github.com/yoshimasaogawa/WillowProject/tree/master/BinaryOption)
* [Wifunc](https://github.com/yoshimasaogawa/WillowProject/tree/master/Wifunc)

Double Auction
-------
[11/17ダブルオークション発表資料](https://docs.google.com/viewer?url=https://github.com/yoshimasaogawa/Auction/blob/master/Double%20Auction/DoubleAuction.pdf?raw=true)  
ダブルオークションのプログラムが書けました。  
少しまだ実験説明画面において日本語が下手くそな部分がちらほら見かけられますが、だいたい動きます。  

Auctions For Complements
-------  
[12/15複数財オークション発表資料](https://docs.google.com/viewer?url=https://github.com/yoshimasaogawa/Auction/blob/master/Auction%20For%20Complements/Auction%20for%20complements.pdf?raw=true)  
複数材オークションのプログラムが書けました。
[この論文](http://www.cirje.e.u-tokyo.ac.jp/research/workshops/micro/micropaper14/micro1021.pdf)を参考にしました。  
当日はエンコードの仕様の違いやコードミスによりプログラムが上手く動きませんでした。発表するはずだった資料を置いておきます。当日の発表で何をやっているかよく分からなかった人は参考にしていただければ幸いです。

Public Goods Game
-------
サンプルコードが仕上がりました。コード上には山岸がコメントを残してくれました。  
何か改善すべき部分がありましたらプルリクエスト(?)してもらえれば嬉しいです。。

Wifunc
-------
Wifunc.py(ワイファンク)というファイルに汎用性の高そうなコードを関数化してまとめました。  
これをimportしておけばコードがより一層楽に書けるようになる予定です。  
今のところ、初期設定における人数、価格の決定などを関数化してあります。  
wifunc.pycという付属でついてくるファイルいついてはよく分かりませんが勝手に生成されました。  

次回に向けて
-------
・エージェントをコード内に組み込む。  
・pandasでデータ分析プログラムを作る。(まず最低限の統計のお勉強を) 
