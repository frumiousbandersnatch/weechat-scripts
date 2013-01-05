#!/usr/bin/env python
# -*- coding: utf-8 -*-

SCRIPT_NAME    = "bee"
SCRIPT_AUTHOR  = "Frumious Bandersnatch <frumious.irc@gmail.com>"
SCRIPT_VERSION = "0"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "Correct spelling."
SCRIPT_COMMAND = "bee"

settings = {
}

import_ok = True
try:
    import weechat
except ImportError:
    print "This script must be run under WeeChat."
    print "Get WeeChat now at: http://www.weechat.org/"
    import_ok = False

try:
    import enchant
except ImportError:
    print "This script requires the Enchant Python package."
    import_ok = False

spelling = enchant.Dict("en_US")
bar_name = "beebar"
bar_item = "bee_suggestions"

recent_suggestions = []


def bee_item_cb(data, item, window):
    return ' '.join(recent_suggestions)


def get_word(line, pos):
    start = line.rfind(' ',0,pos)
    if start == -1: 
        start = 0
    end = line.find(' ', pos)
    if end == -1: 
        end = len(line)
    return line[start:end].strip()

def beebar_toggle(what = 'toggle'):
    weechat.command("", "/bar %s %s" % (what, bar_name))
def beebar_update():
    weechat.bar_item_update(bar_item)

def bee_cmd(data, buffer, args):
    line = weechat.buffer_get_string(buffer, 'input')
    if not line:
        return weechat.WEECHAT_RC_OK

    pos = weechat.buffer_get_integer(buffer, 'input_pos')
    word = get_word(line, pos)
    if not word:
        return weechat.WEECHAT_RC_OK        

    global recent_suggestions
    recent_suggestions = spelling.suggest(word)

    beebar_toggle("show")
    beebar_update()
    return weechat.WEECHAT_RC_OK

def init():
    ok = import_ok and weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, 
                                        SCRIPT_LICENSE, SCRIPT_DESC, "", "")
    if not ok: 
        return

    # Set default settings
    for option, default_value in settings.iteritems():
        if not weechat.config_is_set_plugin(option):
            weechat.config_set_plugin(option, default_value)

    return True


def main():
    if not init(): return

    weechat.hook_command(SCRIPT_COMMAND,
                         SCRIPT_DESC,
                         "[cmd1 | cmd2]",
                         "   cmd1: comand1\n"
                         "   cmd2: command2\n",
                         "cmd1 example",
                         "bee_cmd", "")
    
    weechat.bar_item_new(bar_item, "bee_item_cb", "");
    weechat.bar_new(bar_name, "on", "0", "root", "", "top", "horizontal",
                    "vertical", "0", "0", "default", "default", "default", "0",
                    bar_item);
    return

if '__main__' == __name__:
    main()
