ADVENTURE
=========
亀夫君問題で多人数アドベンチャーゲームを作るために使用した
ユーザー別の記録プログラムです。

今はまだ簡易版ですが、皆さんのご所望があれば新機能を追加する予定です。

Pre-Requisition
---------------
- python3 or python2: ダウンロードリンクは[こちら](https://www.python.org/downloads/)

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
    ua, add-user <name> <place> <items> add user
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
    alias <name> <command>              alias a command (see `help alias`)
    aliases                             list aliases
    echo, print <message>               literally print line
    help, h                             print this help string
    save, w <file>                      save current state to file (default: autosave)
    savealias <file>                    save current alias to file (default: aliases)
    load <file>                         load state from file (default: autosave)
    loadalias <file>                    load aliases from file (default: aliases)
    wq <file>                           save & exit
    quit, exit, q                       quit program
```

TODO
----
1. 「イベント」class の追加と、イベントと事前に準備したテキストのリンク。（未定）

CONTRIBUTE
----------
このプログラムはライセンスがありません。自由に編集またはコピー出来ます。

**Pull requests are welcomed!**
