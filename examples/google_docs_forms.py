#!/usr/bin/env python
# -*- coding=utf-8 -*-

# This file is an example to perform fake "responses" to google docs forms.

from torquery import Query
from random import choice

# define available values that could be filled inside the form
first_entry_values = ["C D E", "A B C"]
second_entry_values = ["Fake", "SuperFake", "UltraFake"]

# Defining the function to check that everything is working.
# This function will change the request_data used for the next query.
def check_form_sent(self, output):
    # change the values for the next query:
    self.request_data = {
        "draftResponse": [],
        "pageHistory": 0,

        "entry.1242870294": choice(first_entry_values),
        "entry.295214320": choice(second_entry_values)
    }

    if "Your response has been recorded." in output:
        return True
    else:
        return False

# The url of the google docs form that will accept POST values
url = "https://docs.google.com/forms/d/1oyI2krnwwBhPq5HOkWJCAg0u9tasp0-A_-V3LxrloCg/formResponse"

# Form data to use for the query
data = {
    "draftResponse": [],
    "pageHistory": 0,

    "entry.1242870294": choice(first_entry_values),
    "entry.295214320": choice(second_entry_values)
}

# Using POST method and Mac OS TorBrowser Bundle.
q = Query( url, request_data=post_data, method="POST")

# Once the tor local process is running, use this function to check 
q.is_query_working = check_form_sent

while 1:
    try:
        q.single_cycle(verbose=True)
    except KeyboardInterrupt:
        q.tor_process.terminate()
