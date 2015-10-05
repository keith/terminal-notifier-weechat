# terminal-notifier-weechat

This is a simple [weechat](https://weechat.org/) plugin that shows
weechat messages through native OS X notifications using
[`terminal-notifier`](https://github.com/julienXX/terminal-notifier).

## Installation

Install `terminal-notifier` and copy the script to
`~/.weechat/python/autoload`

```sh
brew install terminal-notifier
mkdir -p ~/.weechat/python/autoload
wget https://raw.githubusercontent.com/keith/terminal-notifier-weechat/master/terminal_notifier.py
```

This is a python rewrite of [this ruby
plugin](https://gist.github.com/BlakeWilliams/887612cf3e082134975e)
