# Parser: smovengo (e.g., New Paris - paris2)

import json, re

def parse(df, data, utc):

    # parse out desired info
    # does the file have valid content
    try:
        json_data = json.loads(data)
    except ValueError:
        print(utc + ' ' + df['bssid'] + " Parsing JSON failed for " + df['feedurl'])
        return False

    # capture clean results in clean_stations_list
    # stnid, lat, lng, docks, bikes, spaces, name
    clean_stations_list = []
    for stn in json_data:

        if stn['station']['state'] == 'Operative':
            active = 'yes'
        else:
            active = 'no'

        # Id is in same string as title (silly!)
        stnid = stn['station']['code']
        name =  stn['station']['name']
        ll = stn['station']['gps']

        clean_stations_list.append([stnid, ll['latitude'], ll['longitude'], stn['nbDock'] + stn['nbEDock'], stn['nbBike'] + stn['nbEbike'], stn['nbFreeDock'] + stn['nbFreeEDock'], name, active])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False
    
    return clean_stations_list
