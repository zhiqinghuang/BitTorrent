#!/usr/bin/env python

# Written by Bram Cohen
# this file is public domain

from BitTorrent.download import downloadurl
from BitTorrent.parseargs import parseargs
from threading import Event, Thread
from Tkinter import Tk, Label, Button
from tkFileDialog import asksaveasfilename
from sys import argv, version
assert version >= '2', "Install Python 2.0 or greater"

configDefinitions = [
    # ( <name in config dict>, <long getopt descript>, <short getopt descript>, <default value>, '''usage''')
    ('unthrottle_diff', 'unthrottle-diff=', None, 2 ** 23,
     """How much a peer's balance must exceed that of the lowest balance current downloader before they get unthrottled.  Currently defaults to 2 ** 23.  Will be removed after the switch from balances to transfer rates."""),
    ('rethrottle_diff', 'rethrottle-diff=', None, 2 ** 20,
     """the point at which unthrottle_diff is undone. Defaults to 2 ** 20, will be removed after the switch to transfer rates."""),
    ('max_uploads', 'max-uploads=', None, 2,
     """the maximum number of uploads to allow at once. Default is 2, will be changed to 3."""),
    ('max_downloads', 'max-downloads=', None, 4,
     """the maximum number of downloads to do at once. Default is 4, will be increased."""),
    ('download_chunk_size', 'download-chunk-size=', None, 2 ** 15,
     """How many bytes to query for per requests. Defaults to 2 ** 15."""),
    ('request_backlog', 'request-backlog=', None, 5,
     """how many requests to keep in a single pipe at once. Defaults to 5."""),
    ('max_message_length', 'max-message-length=', None, None,
     """maximum length prefix encoding you'll accept over the wire - larger values get the connection dropped."""),
    ('port', 'port=', 'p:', 6800, """Port to listen on.  Defaults to 6800.  Will be random in the future."""),
    ('socket_poll_period', 'socket-poll-period=', None, None,
     """Number of milliseconds to block in calls to poll()"""),
    ('myip', 'ip=', 'i:', None,
     """ip to report you have to the publicist."""),
    (None, 'help', 'h', None, """Display the command line help.""")
    ]

def run(configDictionary, files):
    root = Tk()
    root.withdraw()
    root.title('BitTorrent')
    def getname(default, root = root):
        result = asksaveasfilename(initialfile = default)
        return result
    l = Label(root, text = "You shouldn't see this")
    l.pack()
    doneflag = Event()
    def shutdown(root = root, doneflag = doneflag):
        doneflag.set()
        root.destroy()
    quit_button = Button(root, text = 'garbage', width=28, height=1, 
        command = shutdown)
    quit_button.pack(side = 'bottom')
    def displayfunc(a, b, root = root, l = l, button = quit_button):
        root.deiconify()
        l.config(text = a)
        button.config(text = b)
    Thread(target = root.mainloop).start()
    configDictionary['prefetched'] = prefetched
    downloadurl(files[0], getname, displayfunc, doneflag, configDictionary)
    root.destroy()

if __name__ == '__main__':
    usageHeading = "usage: %s [options] <url>" % argv[0]
    config, files = parseargs(argv[1:], usageHeading, configDefinitions, 1, 1) 
    run(config, files)
