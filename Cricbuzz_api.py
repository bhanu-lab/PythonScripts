import xml.etree.ElementTree as ET
import urllib2

'''
Author: @blackram

a simple python script which uses CRIC BUZZ LIVE CRICKET FEED
for getting live cricket feed in xml file using urllib2
and formatting xml file to readable format. 

***requirements***
needed to install urllib2 before running this script
try pip install urllib2 for installing
'''

# Constants Start
MATCH_STATUS_LIVE = "inprogress"
MATCH_STATUS_UPCOMING = "preview"
MATCH_STATUS_COMPLETED = "Result"
COMPLETED_MATCH_STATES = ["stump", "complete", "Result"]
UPCOMING_MATCH_DETAILS_HEADER = "***UPCOMING MATCH DETAILS***"+"\n"
LIVE_MATCH_DETAILS_HEADER = "***LIVE CRICKET SCORES***"+"\n"
COMPLETED_MATCH_DETAILS_HEADER = "***COMPLETED MATCHES***"+"\n"
CRIC_BUZZ_URL = "http://synd.cricbuzz.com/j2me/1.0/livematches.xml"
# Costants End

# Work on cricbuzz API response Start
url = urllib2.Request(CRIC_BUZZ_URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"})
xml = urllib2.urlopen(url)
tree = ET.parse(xml)
root = tree.getroot()
# Work on cricbuzz API response End

# properties for updating to map
live_feed = ""
upcoming_feed = ""
completed_feed = ""
# properties for updating to map

# dictionary is useful when integrated with bots/messages/mails
dict = {'live_matches': live_feed, 'upcoming_matches': upcoming_feed, 'completed_matches': completed_feed}

# Iterating through all matches available
for match in root.findall('match'):
    series = match.find('srs')
    state = match.find('state')
    match_state = match.find('state')
    match_details = match.attrib
    status_details = state.attrib
    # print match.attrib
    # print state.attrib
    # print match_details["srs"]
    match_status = status_details["mchState"]
    # print match_status

    if(match_status == MATCH_STATUS_UPCOMING):
        upcoming_matches = UPCOMING_MATCH_DETAILS_HEADER
        upcoming_matches = upcoming_matches + match_details["srs"] + "\n"
        upcoming_matches = upcoming_matches + match_details["mchDesc"] + " in " + match_details["grnd"]+"\n"
        upcoming_matches = upcoming_matches + "will be playing "+match_details["mnum"] + "\n"
        upcoming_matches = upcoming_matches + status_details["status"] + "\n"
        upcoming_feed = upcoming_feed + upcoming_matches
        dict['upcoming_matches'] = upcoming_feed

    elif(match_status == MATCH_STATUS_LIVE):
        live_matches = LIVE_MATCH_DETAILS_HEADER
        match_score = match.find("mscr")
        bt_tm = match_score.find("btTm")
        inngs = bt_tm.find("Inngs")
        live_matches = live_matches + bt_tm["sName"] + ": " + inngs["r"] + "for " + inngs["wkts"] + " in "+ inngs["ovrs"] + "\n"
        live_matches = live_matches + "playing in "+match_details["mnum"] + "\n"
        live_feed = live_feed + live_matches
        dict['live_feed'] = live_feed

    elif(match_status in COMPLETED_MATCH_STATES):
        completed_matches = COMPLETED_MATCH_DETAILS_HEADER
        completed_matches = completed_matches + match_details["srs"] + "\n"
        completed_matches = completed_matches + match_details["mchDesc"] + "\n"
        completed_matches = completed_matches + status_details["status"] + "\n"
        completed_matches = completed_matches + "has played in " + match_details["mnum"] + "\n"
        completed_feed = completed_feed + completed_matches
        dict['completed_matches'] = completed_feed

# printing to console for testing
print dict['live_matches']
print dict['upcoming_matches']
print dict['completed_matches']












