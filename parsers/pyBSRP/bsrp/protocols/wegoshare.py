# Parser: wegoshare (e.g., raleigh citrixcycle)
import json
import requests

def scrape(df, apikey):

    headers = {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'accept-encoding':'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Content-Type': 'application/json',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'cache-control':'max-age=0',
            'accept-language':'en-US,en;q=0.5'
        }

    try:
        res = requests.post( df['feedurl'], json= {'isPublic': 'true'}, timeout=20, headers= headers )

        if not res or res.status_code != 200:
            print(df['bssid'] + ' Request code=' + str(res.status_code) + '. Failed to retrieve url=' + df['feedurl'])
            return False

        # raise error if any
        res.raise_for_status()

    except ValueError: 
        print(df['bssid'] + ' Failed to retrieve url=' + df['feedurl'])
        return False

    return res.json()

def parse(df, json_data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    if not isinstance(json_data, dict):
        print("Failed to parse data as json is not formed as expected")
        return False

    # capture clean results in clean_stations_list
    # stnid, lat, lng, docks, bikes, spaces, name
    clean_stations_list = []
    for stn in json_data['results']:

        bikes  = int(stn['totalLockedCycleCount'])
        spaces = int(stn['freeDocksCount']) + int(stn['freeSpacesCount'])
        docks = int(stn['fullCycleStockingCount']) + int(stn['overFullCycleStockingCount'])

        if stn['stationStatus'] == "OPEN":
            active = 'yes'
        else:
            active = 'no'

        stnid = stn['serialNumber']
        
        # stnid, lat, lng, docks, bikes, spaces, name, active
        clean_stations_list.append([stnid, stn['areaCentroid']['latitude'], stn['areaCentroid']['longitude'], docks, bikes, spaces, stn['name'], active])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False

    return clean_stations_list
