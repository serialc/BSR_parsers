# Parser: Bicycle Transit Systems (e.g., LA, Philadelphia)

import json, re

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # parse json data
    try:
        data_json = json.loads(data)
    except ValueError:
        print(utc + ' ' + df['bssid'] + " Parsing JSON failed for " + df['feedurl'])
        return False
    
    # check if we retreived the station list
    if not data_json.has_key('features'):
        print(utc + ' ' + df['bssid'] + " Data does not contain 'features' element'. No data found.")
        return False
    
    # open the stationBeanList now that we know it exists
    stations_list = data_json['features']

    # check for the size of stationBeanList
    if len(stations_list) <= 1:
        print(utc + ' ' + df['bssid'] + " Data does not contain 'feautres' element'. No data found.")
        return False

    # capture clean results in clean_stations_list
    clean_stations_list = []
    for stn_dict in stations_list:

        # build the list of valid data
        # check if the station is online
        if stn_dict['properties']['kioskPublicStatus'] == 'Active':
            active = 'yes'
        else:
            active = 'no'

        # stnid, lat, lng, docks, bikes, spaces, name, active
        clean_stations_list.append([
            str(stn_dict['properties']['kioskId']),
            str(stn_dict['geometry']['coordinates'][1]), # lat
            str(stn_dict['geometry']['coordinates'][0]), # long
            str(int(stn_dict['properties']['docksAvailable']) + int(stn_dict['properties']['bikesAvailable'])),
            str(stn_dict['properties']['bikesAvailable']),
            str(stn_dict['properties']['docksAvailable']),
            str(stn_dict['properties']['name']),
            active])
    # End of stations looping

    # check if we have some data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False

    return clean_stations_list
