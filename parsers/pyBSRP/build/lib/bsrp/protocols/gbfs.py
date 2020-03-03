# gbfs.py
# Parser: General Bikeshare Feed Specification

import json, requests
#from bsrp import bsrputil

def scrape(df, apikey):

    # get the GBFS 'pointer' file that indicates paths to the key files
    try:
        print("Trying:", df['feedurl'])
        gbfs_index = requests.get( df['feedurl'] )
        
        if gbfs_index.status_code != 200:
            print("Retrieval returned ", gbfs_index.status_code)
            return False

        # see if any other errors - throw
        gbfs_index.raise_for_status()

        # parse to JSON
        gbfs_json = json.loads(gbfs_index.text)

    except requests.exceptions.SSLError:
        print("Couldn't access GBFS feed for " + df['bssid'] + " due to SSL error.")
        return False

    # Get the two important urls with station status and station locations and names
    # Choose english if available
    languages = list(gbfs_json['data'])
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
        print("Did not find the feed for " + df['bssid'] + ".")
        print(gbfs_json)
        return False

    # Get the station information
    try:
        information_req = requests.get(station_information_url)
        information_json = json.loads(information_req.text)
        print(information_json)

        # see if any errors
        information_req.raise_for_status()

    except urllib3.URLError:
        print("Couldn't access station information for " + df['bssid'] + ".")
        return False

    # Get the station statuses
    try:
        status_req = requests.get(station_status_url)
        status_json = json.loads(status_req.text)
        print(status_json)

        # see if any errors
        status_req.raise_for_status()
    except urllib3.URLError:
        print("Couldn't access station status for " + df['bssid'] + ".")
        return False

    # Return both parts
    return {'information': information_json, 'status': status_json}

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    if not data:
        return False

    clean_stations_dict = dict()
    # Go through station information
    for stn in data['information']['data']['stations']:
        clean_stations_dict[stn['station_id']] = {'stnid': stn['station_id'], 'lat': stn['lat'], 'lon': stn['lon'], 'name': stn['name']}
        
    # Go through station status and fill the clean_stations_dict with complementary status info
    # Two possible bad outcomes a) No status for station, b) No station for status info
    for stn in data['status']['data']['stations']:
        # Check if this status station exists in information list
        try:
            clean_stations_dict[stn['station_id']]['bikes'] = stn['num_bikes_available']
        except KeyError:
            print('Station ' + str(stn['station_id']) + ' does not exist in station information data. Dropping it from list.')
            continue

        clean_stations_dict[stn['station_id']]['docks'] = stn['num_docks_available']
        clean_stations_dict[stn['station_id']]['active'] = 'yes'
        if stn['is_installed'] == 0 or stn['is_renting'] == 0 or stn['is_returning'] == 0:
            clean_stations_dict[stn['station_id']]['active'] = 'no'

    # Check that each station has been filled with some status
    for stn in list(clean_stations_dict):
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
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False

    return clean_stations_list
