# Synopsis

Get data and graphs about your imgur accont.

This is a command-lne application, for now. Eventually it'l produce graphs and
websites and etcetera.

# Example

`./plot_contributions.py -u <username>`

# Installation

When using this, you'll need to create a config file, `config.py`. It should
containe a couple strings that imgur requires you to give for your application.
This file is loaded automatically.

    CLIENT_ID = 'FOO'
    CLIENT_SECRET = 'BAR'

Get the real strings for these two variables by registering your application at
https://api.imgur.com/oauth2/addclient

# Useful links for me while I'm building this

 - https://plot.ly/python/
 - https://github.com/Imgur/imgurpython
 - https://api.imgur.com/endpoints/account#comment-count
 - https://api.imgur.com/models/comment

# Author

Justin McGuire <jm@landewdstar.com> <@landedstar.com> http://landedstar.com

# License

MIT License

