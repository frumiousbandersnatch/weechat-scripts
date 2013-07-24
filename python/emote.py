#!/usr/bin/env python
# -*- coding: utf-8 -*-

SCRIPT_NAME    = "emote"
SCRIPT_AUTHOR  = "frumious <frumious.irc@gmail.com>"
SCRIPT_VERSION = "0"
SCRIPT_LICENSE = "GPL2"
SCRIPT_DESC    = "Faciliate silly faces"
SCRIPT_COMMAND = "emote"

import_ok = True
try:
    import weechat
except Exception:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org/")
    import_ok = False
wprint = weechat.prnt

import os
import sys
import codecs
from collections import OrderedDict
def decode(s):
    if isinstance(s, str):
        s = s.decode('utf-8')
    return s

def encode(u):
    if isinstance(u, unicode):
        u = u.encode('utf-8')
    return u


bag = dict({
    'smile':':)', 
    'frown':':(',
    "facecry":"(╥﹏╥)",
    "lenny":"(﻿ ͡° ͜ʖ ͡°)",
    "whatever":"¯L(ツ)_/¯",
    "pointup":"(☝ﾟヮﾟ)☝",
    "pointleft":"☜(ﾟヮﾟ☜)",
    "pigtails":"／人◕ ‿‿ ◕人＼",
    "tossbox":"(╯°□°）╯︵ ┻━┻",
    "highfive":"(✿ˇ◡◡ˇ)人(ˇ◡◡ˇ❀)",
    "facelook":"ʘᴥʘ",
    "fuckyou":"╭∩╮(-_-)╭∩╮",
    "glass2":"(⌐■_■)",
    "arrowup":"↑",
    "bow":"＿|￣|○",
    "pointright":"(☞ﾟヮﾟ)☞",
    "tosschi":"ヽ(#`Д´)ﾉ ︵ ┻━┻",
    "yum":"ლ(´ڡ`ლ)",
    "musicnotes":"♪ ♫",
    "glass1":"( •_•)>⌐■-■",
    "dance1":"〜(￣▽￣〜)(〜￣▽￣)〜",
    "dance2":"♪┏(・o･)┛♪",
    "boobies":"(⊙)(⊙ԅ(ˆ⌣ˆԅ)",
    "strong1":"ᕙ(⇀‸↼‶)ᕗ",
    "strong2":"ᕦ❜⦺❜ᕤ",
    "grr":"ლ(ಠ益ಠლ)",
    "pig":"(•ω•)",
    "dunno":"┐('～`；)┌",
    "faceemo":"(///_ಥ)",
    "blowkiss":"(づ￣ ³￣)づ・゜゜・。。・゜゜❤",
    "facebear":"ʕ •ᴥ•ʔ",
    "want":"ლ(╹◡╹ლ)",
    "throwstars":"*･゜ﾟ･*\(^O^)/*･゜ﾟ･*☆",
    "inlove":"(✿ ♥‿♥)",
    "manchest":"ლ(́◉◞౪◟◉‵ლ)",
    "catch":"(／_^)／ 　　　　　　●　＼(^_＼)",
    "therethere":"(ｏ・_・)ノ”(ノ_＜。)",
    "kick":"ヽ(#ﾟДﾟ)ﾉ┌┛",
    "stache":"(￣┏Д┓￣°*)",
    "smug":"（￣へ￣）",
    "worried":"⊙﹏⊙",

})
emoji = OrderedDict(sorted(bag.items()))

# fixme: make this configurable
# emoji_filename = os.path.expanduser("~/.weechat/emote.txt")
# def load_emoji():
#     od = OrderedDict()
#     with codecs.open(emoji_filename,encoding='utf-8') as fp:
#         everything = fp.read()
#         for line in everything.split('\n'):
#             line = line.strip()
#             if not line: continue
#             name, face = line.split(' ',1)
#             od[name] = face.encode('utf-8', 'replace')
#     return od


return_buffer = None
def buffer_insert_text(buf, text):
    pos = weechat.buffer_get_integer(buf, 'input_pos')
    input = decode(weechat.buffer_get_string(buf, 'input'))

    begin = input[:pos]
    middle = decode(text)
    end = input[pos:]

    newpos = pos + len(middle)
    newinput = begin + middle + end
    #newinput = '%s%s%s' %(begin, middle, end)

    #weechat.buffer_set(buffer, 'input', encode(input))
    #weechat.buffer_set(buffer, 'input_pos', str(pos - n + len(replace)))

    weechat.buffer_set(buf, 'input', encode(newinput))
    weechat.buffer_set(buf, 'input_pos', str(newpos))
    return begin, middle, end

# callback for data received in input
def buffer_input_cb(data, buf, input_data):
    global return_buffer
    if return_buffer is None:
        wprint("",'No return buffer for emote')
        return weechat.WEECHAT_RC_OK

    the_face = None
    try:
        the_face = emoji[input_data]
    except KeyError:
        return weechat.WEECHAT_RC_OK        
    
    weechat.buffer_set(return_buffer, 'display', '1')
    buffer_insert_text(return_buffer, the_face)

    wprint(buf,'Inserting %s -> %s in %s is now "%s"' %\
           (input_data, the_face, 
            weechat.buffer_get_string(return_buffer, "full_name"),
            weechat.buffer_get_string(return_buffer, "input")))

    return_buffer = None
    return weechat.WEECHAT_RC_OK

# callback called when buffer is closed
def buffer_close_cb(data, buffer):
    # ...
    return weechat.WEECHAT_RC_OK

def make_buffer():
    emote_buf = weechat.buffer_new("emote", "buffer_input_cb", "", 
                                   "buffer_close_cb", "")
    weechat.buffer_set(emote_buf, "Emote", "Facetious Faces.")
    weechat.buffer_set(emote_buf, "localvar_set_no_log", "1")
    return emote_buf



def command_show_emotes_cb(data, cmd_buf, args):
    global emoji
    global return_buffer
    return_buffer = cmd_buf     # is this the best way?

    args = args.split()

    if args[0] == 'list':
        buf = weechat.buffer_search("python", "emote")
        weechat.buffer_clear(buf)
        wprint(buf, 'got data="%s" args="%s"' % (str(data), str(args)))
        for k,v in emoji.items():
            wprint(buf, '%16s --> %s' % (k,v))
        weechat.buffer_set(buf, 'display', '1')
        return weechat.WEECHAT_RC_OK

    # if args[0] == 'load':
    #     emoji = load_emoji()
    #     return weechat.WEECHAT_RC_OK

    return weechat.WEECHAT_RC_OK

if __name__ == "__main__" and import_ok:
    if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                        SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
        buf = make_buffer()
        #buf = weechat.buffer_search("python", "emote")


        #emoji = load_emoji()
        
        wprint(buf, 'Hello from emote, I have %d emoji' % len(emoji))
        wprint(buf, 'Running with Python: %s' % sys.version)

        weechat.hook_command("emote", "Facetious Faces",
                             "[list] | [<name>]",
                             "description:",
                             "list: show all | <name> insert named",
                             "command_show_emotes_cb", "some data")
        
