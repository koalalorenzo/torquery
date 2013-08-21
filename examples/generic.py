#!/usr/bin/env python
# -*- coding=utf-8 -*-

from torquery import Query

q = Query("http://google.com/search?q=koalalorenzo")

q.start_loop()
q.tor_process.terminate()
