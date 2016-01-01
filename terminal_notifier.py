# This weechat plugin sends OS X notifications for weechat messages
#
# Install terminal-notifier, no other configuration needed.
#
# History:
#
# Version 1.0.0: initial release
# Version 1.0.1: fix escape characters which broke terminal-notifier
# Version 1.0.2: set the nick as the title of the notification
# Version 1.0.3: throttle notification calls


import datetime
import distutils.spawn
import functools
import os
import os.path
import pipes
import weechat


# https://gist.github.com/ChrisTM/5834503
class throttle(object):
    """
    Decorator that prevents a function from being called more than once every
    time period.

    To create a function that cannot be called more than once a minute:

        @throttle(minutes=1)
        def my_fun():
            pass
    """
    def __init__(self, seconds=0, minutes=0, hours=0):
        self.throttle_period = datetime.timedelta(
            seconds=seconds, minutes=minutes, hours=hours
        )
        self.time_of_last_call = datetime.datetime.min

    def __call__(self, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            now = datetime.datetime.now()
            time_since_last_call = now - self.time_of_last_call
            if time_since_last_call > self.throttle_period:
                self.time_of_last_call = now
                return fn(*args, **kwargs)
        return wrapper


def needs_escape(string):
    return string[0] in '[-("'


@throttle(seconds=1)
def notify(data, signal, signal_data):
    separated = signal_data.split("\t")
    try:
        name = separated[0]
    except IndexError:
        name = "WeeChat"

    message = "\t".join(separated[1:])
    if needs_escape(message):
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

    if not weechat.register("terminal_notifier", "Keith Smiley", "1.0.3", "MIT",
                            "Get OS X notifications for messages", "", ""):
        return weechat.WEECHAT_RC_ERROR

    weechat.hook_signal("weechat_pv", "notify", "")
    weechat.hook_signal("weechat_highlight", "notify", "")

    return weechat.WEECHAT_RC_OK

if __name__ == "__main__":
    main()
