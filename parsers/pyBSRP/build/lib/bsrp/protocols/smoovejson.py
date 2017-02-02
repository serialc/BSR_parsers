# Parser: smoovejson (e.g., vancouver)

import json, re

def parse(df, data, utc):
    # df contains an array named 'result', each item has:
    # {"name":"0001 10th & Cambie","coordinates":"49.262487, -123.114397","total_slots":52,"free_slots":27,"avl_bikes":25,"operative":true,"style":""}

    # parse out desired info
    # does the file have valid content
    try:
        json_data = json.loads(data)
        json_data = json_data['result']
    except ValueError:
        print(utc + ' ' + df['bssid'] + " Parsing JSON failed for " + df['feedurl'])
        return False

    # capture clean results in clean_stations_list
    # stnid, lat, lng, docks, bikes, spaces, name
    clean_stations_list = []
    for stn in json_data:

        if stn['operative'] == True:
            active = 'yes'
        else:
            active = 'no'

        # Id is in same string as title (silly!)
        stnid = stn['name'].split(' ')[0]
        name = ' '.join(stn['name'].split(' ')[1:])
        ll = stn['coordinates'].split(',') # need to remove spaces still

        clean_stations_list.append([stnid, ll[0].strip(), ll[1].strip(), str(int(stn['avl_bikes']) + int(stn['free_slots'])), stn['avl_bikes'], stn['free_slots'], name, active])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False
    
    return clean_stations_list
