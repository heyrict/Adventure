# -*- coding: utf8 -*-
from __future__ import print_function
from game import *
from six.moves import cPickle as pickle
from six.moves import range
from six.moves import input
import pickle
import random
import sys, os


def userinfo(game, name):
    user = game.get_user(name)
    print("Place:",c(user.place.name,"magenta"))
    print("Items:","\n  ".join(user.items))

def placeinfo(game, name):
    place = game.get_place(name)
    print("Users:","  ".join([c(i.name,"red") for i in place.users]))
    print("Items:","\n  ".join(place.items))

def dumpGame(game, filename="autosave"):
    with open(filename+".pickle", "wb") as f:
        pickle.dump(game, f, protocol=2)

def loadGame(filename="autosave"):
    with open(filename+".pickle", "rb") as f:
        return pickle.load(f)

if __name__ == "__main__":
    helpstr = '''
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
    help, h                             print this help string
    save, w <file>                      save current state to file
    load <file>                         load current state from file
    wq <file>                           save & exit
    quit, exit, q                       quit program
    '''
    help_alias_str = '''
    Alias
    -----
    Usage: alias <name> <command>

    <name>
        name of your new command

    <command>
        a python string for formatting

    Examples:
        alias myua ua {} myplace myitem
        myua me # equivalent to `ua me myplace myitem`

        alias mypa pa a_{0}_place_of_{1} {0}_juice {0}_cake
        mypa tasty chocolate
        # equivalent to `pa a_tasty_place_of_chocolate tasty_juice tasty_cake`

        alias mynewua pa room{0} tons_of_books; ua {0} book
        mynewua Kitty
        # equivalent to:
        # `pa roomKitty tons_of_books`
        # `ua Kitty book`
    '''

    game = Game(sys.argv[1] if len(sys.argv) > 1 else "party")
    indicator = "<"+game.name+">: "
    aliases = {}
    cmdQueue = []
    while True:
        try:
            if cmdQueue == []:
                cmdQueue.append(input(c(indicator, "yellow")))
            cmd = cmdQueue.pop(0).split()
            if len(cmd) == 0: continue
            if cmd[0] in aliases:
                cmdQueue.extend(aliases[cmd[0]].format(*cmd[1:]).split(';'))
                cmd = cmdQueue.pop(0).split()

            if cmd[0] in ['alias']:
                aliases[cmd[1]] = " ".join(cmd[2:])
            elif cmd[0] in ['ua', 'add-user']:
                game.add_user(cmd[1], cmd[2], cmd[3:])
            elif cmd[0] in ['pa', 'add-place']:
                game.add_place(cmd[1], cmd[2:])
            elif cmd[0] in ['ul', 'us']:
                game.show_users()
            elif cmd[0] in ['pl', 'ps']:
                game.show_places()
            elif cmd[0] in ['gl', 'gs', 'game']:
                game.show_game_info()
            elif cmd[0] in ['ui']:
                userinfo(game, cmd[1])
            elif cmd[0] in ['pi']:
                placeinfo(game, cmd[1])
            elif cmd[0] in ['ls']:
                try: userinfo(game, cmd[1])
                except: pass
                try: placeinfo(game, cmd[1])
                except: pass
            elif cmd[0] in ['up', 'pick']:
                game.user_pickitem(cmd[1], cmd[2])
            elif cmd[0] in ['ud', 'drop']:
                game.user_dropitem(cmd[1], cmd[2])
            elif cmd[0] in ['ux', 'discard']:
                game.user_discarditem(cmd[1], cmd[2])
            elif cmd[0] in ['ug', 'get']:
                game.user_getitem(cmd[1], cmd[2])
            elif cmd[0] in ['um','mv']:
                game.user_move(cmd[1], cmd[2])
            elif cmd[0] in ['kill']:
                game.kill_user(cmd[1], " ".join(cmd[2:]))
            elif cmd[0] in ['in']:
                indicator = cmd[1]
            elif cmd[0] in ['help', 'h']:
                if "".join(cmd[1:]) == "alias":
                    print(help_alias_str)
                else:
                    print(helpstr)
            elif cmd[0] in ['save','w']:
                filename = "".join(cmd[1:])
                dumpGame(game, filename if filename else "autosave")
                print("Save succeed")
            elif cmd[0] in ['load']:
                filename = "".join(cmd[1:])
                game = loadGame(filename if filename else "autosave")
                print("Load succeed")
            elif cmd[0] in ['wq']:
                filename = "".join(cmd[1:])
                dumpGame(game, filename if filename else "autosave")
                print("Save succeed.\n\nThank you for playing. Bye!")
                break
            elif cmd[0] in ['quit', 'exit', 'q']:
                print("Thank you for playing. Bye!")
                break
            else:
                raise ValueError("Command unable to recognize")

        except (KeyboardInterrupt, EOFError) as e:
                dumpGame(game, "autosave")
                print("\nSave current status to autosave.pickle. Exiting.")
                exit(0)
        except Exception as e:
            print(e)
