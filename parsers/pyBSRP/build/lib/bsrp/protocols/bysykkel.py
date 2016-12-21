# gbfs.py
# Parser: General Bikeshare Feed Specification

import json, re, urllib2, requests
from bsrp import bsrputil

def scrape(df, apikey):

    # get the GBFS 'pointer' file that indicates paths to the key files
    try:
        info_req = requests.get( df['feedurl'] )
        info_json = json.loads(info_req.text)
    except urllib2.URLError:
        print "Couldn't access info feed for " + df['bssid'] + "."
        return False

    # Get the station statuses
    try:
        status_req = requests.get( df['feedurl2'] )
        status_json = json.loads(status_req.text)
    except urllib2.URLError:
        print "Couldn't access station status for " + df['bssid'] + "."
        return False

    # Return both parts
    return {'information': info_json, 'status': status_json}

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    clean_stations_dict = dict()
    # Go through station information
    for stn in data['information']['stations']:
        clean_stations_dict[stn['id']] = {'stnid': stn['id'], 'lat': stn['center']['latitude'], 'lon': stn['center']['longitude'], 'name': stn['title'].replace('\n','')}
        
    # Go through station status and fill the clean_stations_dict with complementary status info
    # Two possible bad outcomes a) No status for station, b) No station for status info
    for stn in data['status']['stations']:
        # Check if this status station exists in information list
        try:
            clean_stations_dict[stn['id']]['bikes'] = stn['availability']['bikes']
        except KeyError:
            #print 'Station ' + str(stn['id']) + ' does not exist in station information data. Dropping it from list.'
            continue

        clean_stations_dict[stn['id']]['docks'] = stn['availability']['locks']
        clean_stations_dict[stn['id']]['active'] = 'yes'

    # Check that each station has been filled with some status
    for stn in clean_stations_dict.keys():
        try:
            clean_stations_dict[stn]['active']
        except KeyError:
            # That's fine we expect some to fail
            clean_stations_dict.pop(stn)

    # capture clean results in clean_stations_list
    # stnid, lat, lng, docks, bikes, spaces, name, active
    clean_stations_list = []
    for stn in clean_stations_dict:
        stn = clean_stations_dict[stn]
        clean_stations_list.append([stn['stnid'], stn['lat'], stn['lon'], int(stn['docks']) + int(stn['bikes']), stn['bikes'], stn['docks'], stn['name'], stn['active']])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print utc + ' ' + df['bssid'] + " Parser did not find any station's data."
        return False

    return clean_stations_list
