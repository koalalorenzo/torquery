#!/usr/bin/env python
# -*- coding=utf-8 -*-

from torquery import Query

# TorBrowser Bundle contains tor command inside /Application folder.
q = Query(
    "http://google.com/search?q=koalalorenzo", 
    tor_cmd="/Applications/TorBrowser_en-US.app/Contents/MacOS/tor"
)

q.start_loop()
q.tor_process.terminate()
