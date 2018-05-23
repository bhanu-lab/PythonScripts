import xml.etree.ElementTree as ET
import urllib2

# Constants Start
MATCH_STATUS_LIVE = "inprogress"
MATCH_STATUS_UPCOMING = "preview"
MATCH_STATUS_COMPLETED = "Result"
COMPLETED_MATCH_STATES = {'stump', 'complete', 'Result'}
UPCOMING_MATCH_DETAILS_HEADER = "***UPCOMING MATCH DETAILS***"+"\n"
CRIC_BUZZ_URL = "http://synd.cricbuzz.com/j2me/1.0/livematches.xml"
# Costants End

# Work on cricbuzz API response Start
url = urllib2.Request(CRIC_BUZZ_URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"})
xml = urllib2.urlopen(url)
tree = ET.parse(xml)
root = tree.getroot()
# Work on cricbuzz API response End

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
    upcoming_matches = UPCOMING_MATCH_DETAILS_HEADER
    live_matches = ""
    if(match_status == MATCH_STATUS_UPCOMING):
        # add match details and send result
        # print "match is in progress"
        upcoming_matches = upcoming_matches + match_details["srs"] + "\n"
        upcoming_matches = upcoming_matches + match_details["mchDesc"] + " in " + match_details["grnd"]+"\n"
        upcoming_matches = upcoming_matches + status_details["status"]
        # notification = notification + "\n" + "----MATCH INFO COMPLETED----"
        print upcoming_matches
    elif(match_status == MATCH_STATUS_LIVE):
        match_score = match.find("mscr")
        bt_tm = match_score.find("btTm")
        inngs = bt_tm.find("Inngs")
        live_matches = upcoming_matches + bt_tm["sName"]










