# This weechat plugin sends OS X notifications for weechat messages
#
# Install terminal-notifier, no other configuration needed.
#
# History:
#
# Version 1.0.0: initial release
# Version 1.0.1: fix escape characters which broke terminal-notifier
# Version 1.0.2: set the nick as the title of the notification

import distutils.spawn
import os
import pipes
import weechat


def notify(data, signal, signal_data):
    separated = signal_data.split("\t")
    try:
        name = separated[0]
    except IndexError:
        name = "WeeChat"

    message = "\t".join(separated[1:])
    if message[0] is "[":
        message = "\\%s" % message
    elif message[0] is "-":
        message = "\\%s" % message
    elif message[0] is "(":
        message = "\\%s" % message
    elif message[0] is '"':
        message = "\\%s" % message

    command = ("terminal-notifier -message %s -title %s -sound Hero"
               % (pipes.quote(message), pipes.quote(name)))
    exit_code = os.system(command)
    if exit_code == 0:
        return weechat.WEECHAT_RC_ERROR
    else:
        return weechat.WEECHAT_RC_OK


def main():
    if distutils.spawn.find_executable("terminal-notifier") is None:
        return weechat.WEECHAT_RC_ERROR

    if not weechat.register("terminal_notifier", "Keith Smiley", "1.0.0", "MIT",
                            "Get OS X notifications for messages", "", ""):
        return weechat.WEECHAT_RC_ERROR

    weechat.hook_signal("weechat_pv", "notify", "")
    weechat.hook_signal("weechat_highlight", "notify", "")

    return weechat.WEECHAT_RC_OK

if __name__ == "__main__":
    main()
