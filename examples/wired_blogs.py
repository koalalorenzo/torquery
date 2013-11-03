#!/usr/bin/env python
# -*- coding=utf-8 -*-

import urllib2
from urlparse import urlparse
import json
import re

from torquery import Query
from random import choice
import sys, os

### Checking Args

if len(sys.argv) < 3 or sys.argv[1] in ["-h", "--help", "help", "h"]:
    sys.stdout.write("Use a valid command to vote on wired blogs:\n")
    sys.stdout.write("   wired_blogs.py METHOD URL\n")
    sys.stdout.flush()
    sys.exit(1)

if sys.argv[1] not in ["wired","tired","expired"]:
    sys.stdout.write("Use wired, tired or exipred as method:\n")
    sys.stdout.write("   wired_blogs.py METHOD URL\n")
    sys.stdout.flush()
    sys.exit(1)

if len(sys.argv[2]) < 5:
    sys.stdout.write("Use a completed and valid URL. (ex: http://domains.ext/path )")
    sys.stdout.write("   wired_blogs.py METHOD URL\n")
    sys.stdout.flush()
    sys.exit(1)

### Config
the_method = sys.argv[1]
the_url = sys.argv[2]

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

def find_url_to_query(url, method="tired"):
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

    if method == "wired":
        path = urls[0]
    elif method == "tired":
        path = urls[1]
    elif method == "expired":
        path = urls[2]
    else:
        path = choice(urls)

    #path = urls[-1]
    return "%s%s" % (domain,path)


url_to_nuke = find_url_to_query(the_url, the_method)
query = Query( url_to_nuke, tor_cmd="/Applications/TorBrowser_en-US.app/Contents/MacOS/tor")
query.is_query_working = check_vote_done

while 1:
    try:
        sys.stdout.write("Querying %s : " % query.url)
        sys.stdout.flush()
        try:
            query.single_cycle(verbose=False)
        except KeyboardInterrupt:
            query.tor_process.terminate()
            os.kill(os.getpid(), 1)
            break
        except: 
            query.tor_process.terminate()
            sys.stdout.write("Error\n")
        sys.stdout.flush()
    except KeyboardInterrupt:
        query.tor_process.terminate()
        os.kill(os.getpid(), 1)
        break
