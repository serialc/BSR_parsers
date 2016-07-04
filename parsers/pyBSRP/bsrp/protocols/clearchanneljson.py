# Parser: bici (e.g., barcelona)

import json, re

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # parse out desired info
    # does the file have valid content
    try:
        json_data = json.loads(data)
    except ValueError:
        print utc + ' ' + df['bssid'] + " Parsing JSON failed for " + df['feedurl']
        return False

    # capture clean results in clean_stations_list
    # stnid, lat, lng, docks, bikes, spaces, name
    clean_stations_list = []
    for stn in json_data:

        if stn['status'] == 'OPN':
            active = 'yes'
        else:
            active = 'no'

        clean_stations_list.append([stn['id'], stn['lat'], stn['lon'], str(int(stn['bikes']) + int(stn['slots'])), stn['bikes'], stn['slots'], stn['name'].encode('utf8'), active])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print utc + ' ' + df['bssid'] + " Parser did not find any station's data."
        return False
    
    return clean_stations_list
