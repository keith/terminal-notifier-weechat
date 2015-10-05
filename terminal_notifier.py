# This weechat plugin sends OS X notifications for weechat messages
#
# Install terminal-notifier, no other configuration needed.
#
# History:
# 10-04-2015
# Version 1.0.0: initial release

import distutils.spawn
import os
import pipes
import weechat


def notify(data, signal, signal_data):
    command = ("terminal-notifier -message %s -title WeeChat -sound Hero"
               % pipes.quote(signal_data))
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
