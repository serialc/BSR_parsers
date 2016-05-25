# Parser: jcdecaux (e.g., Paris, Lyon, Strassbourg, Luxembourg)
# Schema: llstatus

import json, re

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # parse out desired info
    # does the file have valid content
    try:
        json_data = json.loads(unicode(data, 'iso-8859-1'))
    except ValueError:
        print utc + ' ' + df['bssid'] + " Parsing JSON failed for " + df['feedurl']
        return False

    # capture clean results in clean_stations_list
    # stnid, lat, lng, docks, bikes, spaces, name
    clean_stations_list = []
    for stn in json_data:
        clean_stations_list.append([stn['number'], stn['position']['lat'], stn['position']['lng'], stn['bike_stands'], stn['available_bikes'], stn['available_bike_stands'], stn['name'].encode('utf8'), 'yes'])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print utc + ' ' + df['bssid'] + " Parser did not find any station's data."
        return False
    
    return clean_stations_list
