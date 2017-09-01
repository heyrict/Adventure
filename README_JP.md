ADVENTURE
=========
亀夫君問題で多人数アドベンチャーゲームを作るために使用した
ユーザー別の記録プログラムです。

今はまだ簡易版ですが、皆さんのご所望があれば新機能を追加する予定です。

Pre-Requisition
---------------
python3(recommended) or python2

python3 の場合はこのまま使います。

python2 の場合２つのpyファイルの最初の`#import six`の
`#`を取り除く必要があります。

Usage
-----
```bash
python3 main.py
```
インタフェースが`main.py`で、ゲームのクラス定義は`game.py`にあります。

コマンドは以下の通り：
```
    Commands
    --------
    ua, add-user <name>                 add user
    pa, add-place <name> <items>        add place
    ul, us                              list users
    pl, ps                              list places
    gl, gs, game                        show game details
    ui <name>                           show user items
    pi <place>                          show place items
    ls <name/place>                     show user/place items
    up, pick <name> <item>              user pick-item
    ud, drop <name> <item>              user drop-item
    ux, discard <name> <item>           user discard-item
    ug, get <name> <item>               user get-item
    um, mv <name> <dest>                user move place
    kill <name> [<byname>]              user dead
    in <indicator>                      set indicator
    help, h                             print this help string
    save, w <file>                      save current state to file
    load <file>                         load current state from file
    wq <file>                           save & exit
    quit, exit, q                       quit program
```

TODO
----
1. 「イベント」class の追加と、イベントと事前に準備したテキストのリンク。（未定）

CONTRIBUTE
----------
このプログラムはライセンスがない。自由に編集またはコピー出来ます。

**Pull requests are welcomed!**
