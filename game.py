from __future__ import print_function
#from six.moves import cPickle as pickle
#from six.moves import range
import re
from datetime import datetime


class Logger():
    def __init__(self, logfilename):
        self.fn = logfilename

    def write(self, *args, sep=' ', end="\n"):
        l2w = sep.join([str(i) for i in args]) + end
        l2w = "#" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")\
                + "# " + l2w
        print(l2w, end="")
        with open(self.fn, 'a') as f:
            f.write(l2w)


class Game():
    def __init__(self, name, places=[], users=[], logfile="log.txt"):
        self.name = name
        self.users = users
        self.places = places
        self.logger = Logger(logfile)

    def add_place(self, placename, items=[]):
        if placename in [i.name for i in self.places]:
            place = self.get_place(placename)
            place.additem(items)
            self.logger.write("Place",c(place.name,"magenta"),
                    "get",c("  ".join(items),"cyan"))
            return
        p2a = Place(placename, items)
        self.places.append(p2a)
        self.logger.write("Add",c(placename,"magenta"),
                "with items:",c(items,"cyan"))

    def add_user(self, username, initplace=None, inititems=[]):
        if username in [i.name for i in self.users]:
            user = self.get_user(username)
            user.getitem(items)
            self.logger.write("User",c(user.name,"red"),
                    "get",c("  ".join(inititems),"cyan"))
            return

        if initplace == None:
            initplace = self.place[0]
        elif isinstance(initplace, Place):
            if initplace not in self.places:
                raise ValueError("add_user: initplace not in places")
        elif isinstance(initplace, str):
            initplace = self.get_place(initplace)
        else:
            raise ValueError("add_user: initplace type {0} invalid".format(
                type(c(initplace,"magenta"))))

        u2a = User(username, initplace, inititems)
        initplace.adduser(u2a)
        self.users.append(u2a)
        self.logger.write("Add",c(username,"red"),
                "at",c(initplace.name,"magenta"),
                "with items:",c("  ".join(inititems),"cyan"))

    def kill_user(self, username, by=None):
        u2bk = self.get_user(username)
        self.users.remove(u2bk)
        u2bk.place.additem("body_of_"+u2bk.name)
        u2bk.place.additem(u2bk.items)
        u2bk.place.removeuser(u2bk)
        if by:
            self.users.remove(u2bk)
            self.logger.write("User",c(u2bk.name,"red"),
                    "is killed by",by,
                    "in",c(u2bk.place.name,"magenta"))
        else:
            self.logger.write("User",c(u2bk.name,"red"),
                    "died in",c(u2bk.place.name,"magenta"))

    def get_user(self, username):
        for u in self.users:
            if re.findall("^"+username, u.name):
                return u
        raise ValueError(c(username,"red")+" not in self.users")

    def get_place(self, placename):
        for p in self.places:
            if re.findall("^"+placename, p.name):
                return p
        raise ValueError(c(placename,"magenta")+" not in self.places")

    def show_game_info(self):
        print("Game {0}\n==========".format(c(self.name.title(),"green")))
        print("Users\n-----")
        for u in self.users:
            print(c(u.name,"red")+':')
            print("  "+"Current Place")
            print("    "+c(u.place.name,"magenta"))
            print("  "+"Items:")
            for i in u.items: print("    "+c(i,"cyan"))
        print("\nPlaces\n------")
        for p in self.places:
            print(c(p.name,"magenta")+":")
            print("  "+"Users here")
            for u in p.users: print("    "+c(u.name,"red"))
            print("  "+"Items here")
            for i in p.items: print("    "+c(i,"cyan"))

    def show_users(self):
        print("  ".join([i.name for i in self.users]))

    def show_places(self):
        print("  ".join([i.name for i in self.places]))

    def user_dropitem(self, username, itemname):
        user = self.get_user(username)
        place = user.place
        itemname = user.dropitem(itemname)
        place.additem(itemname)
        self.logger.write("User",c(user.name,"red"),
                "drops",c(itemname,"cyan"),
                "at",c(place.name,"magenta"))

    def user_pickitem(self, username, itemname):
        user = self.get_user(username)
        place = user.place
        itemname = place.removeitem(itemname)
        user.getitem(itemname)
        self.logger.write("User",c(user.name,"red"),
                "picks",c(itemname,"cyan"),
                "up at",c(place.name,"magenta"))

    def user_getitem(self, username, itemname):
        user = self.get_user(username)
        user.getitem(itemname)
        self.logger.write("User",c(user.name,"red"),
                "gets",c(itemname,"cyan"))

    def user_discarditem(self, username, itemname):
        user = self.get_user(username)
        item = user.dropitem(itemname)
        self.logger.write("User",c(user.name,"red"),
                "discards",c(item,"cyan"))

    def user_move(self, username, placename):
        user = self.get_user(username)
        preplace = user.place
        postplace = self.get_place(placename)
        preplace.removeuser(user)
        postplace.adduser(user)
        user.goto(postplace)
        self.logger.write("User",c(user.name,"red"),
                "move from", c(preplace.name,"magenta"),
                "to",c(postplace.name,"magenta"))


class Place():
    def __init__(self, name, items=[], events=[]):
        self.name = name
        self.users = []
        self.items = items
        self.events = events

    def removeitem(self, item):
        for i in self.items:
            if re.findall("^"+item, i):
                self.items.remove(i)
                return i
        raise ValueError("Item {0} doesn't exists".format(item))

    def additem(self, item):
        if isinstance(item, list):
            self.items.extend(item)
        else:
            self.items.append(item)

    def adduser(self, user):
        self.users.append(user)

    def removeuser(self, user):
        try: self.users.remove(user)
        except: "User {0} isn't here".format(user.name)


class User():
    def __init__(self, name, place=None, items=[]):
        self.name = name
        self.place = place
        self.items = items

    def goto(self, place):
        self.place = place

    def getitem(self, item):
        self.items.append(item)

    def dropitem(self, item):
        for i in self.items:
            if re.findall("^"+item, i):
                self.items.remove(i)
                return i
        raise ValueError("Item {0} doesn't exists".format(item))


def c(string,color):
    colors = ['black','red','green','yellow','blue','magenta',\
            'cyan','white','gray','lightred','lightgreen','lightyellow',\
            'lightblue','lightmagenta','lightcyan']
    if type(color) == str:
        if color not in colors:
            raise ValueError('Given color',color,'not supported')
        color = colors.index(color)
    else:
        if color not in range(256):
            raise ValueError(color,'is not a 256-color index')

    return '\033[38;5;%dm%s\033[0m'%(color,string)
