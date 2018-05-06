#!/usr/local/bin/python
import os
import requests
from lxml import html
import pync

CRICKET_SITE = 'http://www.cricbuzz.com'
CONTENT_FROM_HTML = '//div[@class="cb-ovr-flo cb-hmscg-tm-nm"  or @class="cb-ovr-flo" or  @class=" cb-ovr-flo cb-text-complete" or @class=" cb-ovr-flo cb-text-live"]/text()'
TITLE = 'Cricket Scores'

page = requests.get(CRICKET_SITE)
# print page.content
tree = html.fromstring(page.content)

# searching for required data
allscoreslist = tree.xpath(CONTENT_FROM_HTML)
allscores = []
# for loop used to remove duplicate values may override actual existing values some time
# todo
for score in allscoreslist:
    if score not in allscores:
        allscores.append(score)

message = ""
teamscores = []

# formatting data received for readability
for score in allscoreslist:

    if score[0].isdigit():
        message = message + (score + "\n")
    else:
        if len(score) > 6:
            score = score + "\n"

            message = message + score
            message = message + "**************" + "\n"
            if message not in teamscores:
                #                print "in message"
                teamscores.append(message)
                message = ""
            else:
                #                print("Met matching values")
                message = ""
        else:
            message = message + (score + "\t")


# Adding Notification information
# Sending only first cricket match information from array
pync.notify(teamscores[0],title=TITLE, activate='com.apple.Safari', open=CRICKET_SITE, execute='Test')

pync.remove_notifications(os.getpid())
pync.list_notifications(os.getpid())
