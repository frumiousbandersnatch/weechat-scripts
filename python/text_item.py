# -*- coding: utf-8 -*-
#
# Copyright (c) 2012-2013 by nils_2 <weechatter@arcor.de>
#
# add a plain text to item bar
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# 2013-01-25: nils_2, (freenode.#weechat)
#       0.2 : make script compatible with Python 3.x
#
# 2012-12-23: nils_2, (freenode.#weechat)
#       0.1 : initial release
#
# requires: WeeChat version 0.3.0
#
# How to use:
# ===========
#
# Template:
#  /set plugins.var.python.text_item.<item_name> <type> <${color}><text>
#  type : all, channel, server, private
#  (use /buffer localvar)
#
# Example:
# =======
# creates an option for a text item (nick_text), to use in all channel buffers:
#  /set plugins.var.python.text_item.nick_text channel ${yellow}Nicks:
#
# add the item "nick_text" to the bar.items (use auto-completion or iset.pl!)
# /set weechat.bar.status.items nick_text
#
# The text "Nicks:" will be displayed in the status bar (yellow colored!).
#
# Development is currently hosted at
# https://github.com/weechatter/weechat-scripts

try:
    import weechat,re

except Exception:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org/")
    quit()

SCRIPT_NAME     = "text_item"
SCRIPT_AUTHOR   = "nils_2 <weechatter@arcor.de>"
SCRIPT_VERSION  = "0.2"
SCRIPT_LICENSE  = "GPL"
SCRIPT_DESC     = "add a plain text to item bar"

# regexp to match ${color} tags
regex_color=re.compile('\$\{([^\{\}]+)\}')

# ================================[ options refresh ]===============================
def create_bar_items():
    ptr_infolist_option = weechat.infolist_get('option','','plugins.var.python.' + SCRIPT_NAME + '.*')

    if not ptr_infolist_option:
        return

    while weechat.infolist_next(ptr_infolist_option):
        option_full_name = weechat.infolist_string(ptr_infolist_option, 'full_name')
        option_name = option_full_name[len('plugins.var.python.' + SCRIPT_NAME + '.'):]      # get optionname

        if weechat.bar_item_search(option_name):
            weechat.bar_item_update(option_name)
        else:
            weechat.bar_item_new(option_name,'update_item',option_name)
        weechat.bar_item_update(option_name)

    weechat.infolist_free(ptr_infolist_option)

def update_item (data, item, window):
    if not data:
        return ""

    value = weechat.config_get_plugin(data)

    if value:
        value = check_buffer_type(window,value)
    else:
        return ""

    if not value:
        return ""

    # substitute colors in output
    return re.sub(regex_color, lambda match: weechat.color(match.group(1)), value)

def toggle_refresh(pointer, name, value):
    option_name = name[len('plugins.var.python.' + SCRIPT_NAME + '.'):]      # get optionname

    # option was removed? remove bar_item from struct!
    if not weechat.config_get_plugin(option_name):
        ptr_bar = weechat.bar_item_search(option_name)
        if ptr_bar:
            weechat.bar_item_remove(ptr_bar)
            return weechat.WEECHAT_RC_OK
        else:
            return weechat.WEECHAT_RC_OK

    # check if option is new or simply changed
    if weechat.bar_item_search(option_name):
        weechat.bar_item_update(option_name)
    else:
        weechat.bar_item_new(option_name,'update_item',option_name)

    weechat.bar_item_update(option_name)
    return weechat.WEECHAT_RC_OK

def check_buffer_type(window, value):

    bufpointer = weechat.window_get_pointer(window,"buffer")
    if bufpointer == "":
        return ""

    value = value.split(' ', 1)
    if len(value) <= 1:
        return ""

    channel_type = value[0]
    value = value[1]

    if channel_type == 'all' or weechat.buffer_get_string(bufpointer,'localvar_type') == channel_type:
        return value

    return ""
# ================================[ main ]===============================
if __name__ == "__main__":
    if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, '', ''):
        version = weechat.info_get("version_number", "") or 0
        create_bar_items()
        weechat.hook_config( 'plugins.var.python.' + SCRIPT_NAME + '.*', 'toggle_refresh', '' )
