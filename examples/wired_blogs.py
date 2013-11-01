#!/usr/bin/env python
# -*- coding=utf-8 -*-

import urllib2
from urlparse import urlparse
import json
import re

from torquery import Query
from random import choice
import sys, os


### Config
some_posts = [
    "http://daily.wired.it/news/internet/2013/10/07/signori-twitter-classifica-campioni-vip-564573.html",
]

### Everyghing else
output_checking = {"wired":0, "tired": 0, "expired": 0} # Global dictionary

def check_vote_done(self, output):
    """
        This function is used by Query class in order to check if
        the query is done or not.
    """
    try:
        j = json.loads(output)
    except:
        print output
        sys.stdout.write("\nfailed")
        return False

    #Checking if the past data is the same
    if not j["wired"] >= output_checking["wired"] or \
     not j["tired"] >= output_checking["tired"] or \
     not j["expired"] >= output_checking["expired"]:
        sys.stdout.write(" failed, nothing different")
        return False

    #Saving data into global dictionary in order to check changes
    output_checking["wired"] = j["wired"]
    output_checking["tired"] = j["tired"]
    output_checking["expired"] = j["expired"]

    sys.stdout.write("done\n")
    return True

def find_url_to_query(url):
    """
        Extract the correct URL to vote Wired post.
    """
    data = urllib2.urlopen(url).read()
    parsed_uri = urlparse( url )
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    urls = re.findall(r'sfzhref=[\'"]?([^\'" >]+)', data)
    if len(urls) <= 0:
        return None

    # urls[0] -> Wired
    # urls[1] -> Tired
    # urls[-1] or urls[2] -> Expired
    # print urls
    path = choice(urls)
    #path = urls[-1]
    return "%s%s" % (domain,path)


urls = list()
for posts_url in some_posts:
    urls.append(find_url_to_query(posts_url))

q = Query(choice(urls), tor_cmd="/Applications/TorBrowser_en-US.app/Contents/MacOS/tor")
q.is_query_working = check_vote_done

while 1:
    try:
        q.url = choice(urls)
        sys.stdout.write("Querying %s : " % q.url)
        sys.stdout.flush()
        try:
            q.single_cycle(verbose=False)
        except KeyboardInterrupt:
            q.tor_process.terminate()
            os.kill(os.getpid(), 1)
            break
        except: 
            sys.stdout.write("Error\n")
        sys.stdout.flush()
    except KeyboardInterrupt:
        q.tor_process.terminate()
        os.kill(os.getpid(), 1)
        break
