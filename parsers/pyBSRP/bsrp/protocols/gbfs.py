# gbfs.py
# Parser: General Bikeshare Feed Specification

import json, re, urllib2
from pyBSRP import bsrputil

def scrape(df, apikey):

    # get the GBFS 'pointer' file that indicates paths to the key files
    try:
        gbfs_index = bsrputil.get_url(df['feedurl'], df['bssid'])
        if gbfs_index == "":
            print "Failed to load the index file for " + df['bssid'] + "."
            return False

        gbfs_json = json.loads(gbfs_index)
    except urllib2.URLError:
        print "Couldn't access GBFS feed for " + df['bssid'] + "."
        return False

    # Get the two important urls with station status and station locations and names
    # Choose english if available
    languages = gbfs_json['data'].keys()
    language = languages[0]
    if 'en' in languages:
        language = 'en'

    station_status_url = ''
    station_information_url = ''
    for feed in gbfs_json['data'][language]['feeds']:
        if feed['name'] == 'station_status':
            station_status_url = feed['url']
        if feed['name'] == 'station_information':
            station_information_url = feed['url']

    if station_status_url == '' or station_information_url == '':
        print "Did not find the feed for " + df['bssid'] + "."
        print gbfs_json
        return False

    # Get the station information
    try:
        information_req = bsrputil.get_url(station_information_url, df['bssid'])
        information_json = json.loads(information_req)
    except urllib2.URLError:
        print "Couldn't access station information for " + df['bssid'] + "."
        return False

    # Get the station statuses
    try:
        status_req = bsrputil.get_url(station_status_url, df['bssid'])
        status_json = json.loads(status_req)
    except urllib2.URLError:
        print "Couldn't access station status for " + df['bssid'] + "."
        return False

    # Return both parts
    return {'information': information_json, 'status': status_json}

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    clean_stations_dict = dict()
    for stn in data['information']['data']['stations']:
        clean_stations_dict[stn['station_id']] = {'stnid': stn['station_id'], 'lat': stn['lat'], 'lon': stn['lon'], 'name': stn['name']}
        
    for stn in data['status']['data']['stations']:
        clean_stations_dict[stn['station_id']]['bikes'] = stn['num_bikes_available']
        clean_stations_dict[stn['station_id']]['docks'] = stn['num_docks_available']
        clean_stations_dict[stn['station_id']]['active'] = 'yes'
        if stn['is_installed'] == 0 or stn['is_renting'] == 0 or stn['is_returning'] == 0:
            clean_stations_dict[stn['station_id']]['active'] = 'no'
    
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
