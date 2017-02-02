# Parser: transdev (e.g., Calais, Nice, Vannes)

import json, urllib

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
    if not data_json.has_key('stand'):
        print(utc + ' ' + df['bssid'] + " Data does not contain 'stand' element'. No data found.")
        return False
    
    # open the stationBeanList now that we know it exists
    stations_list = data_json['stand']

    # check for the size of stationBeanList
    if len(stations_list) <= 1:
        print(utc + ' ' + df['bssid'] + " Data does not contain 'stationBeanList' element'. No data found.")
        return False

    # capture clean results in clean_stations_list
    clean_stations_list = []
    for stn in stations_list:
        
        # Active or not
        if stn['neutral'] == '0':
            active = 'yes'
        else:
            active = 'no'

        # Lat lng
        lat = stn['lat']
        lng = stn['lng']
        if lat == '0' or lng == '0':
            # skip these stations
            continue

        if (len(lat) - lat.rfind('.')) > 7:
            lat = lat[0:(lat.rfind('.') + 7)]
        if (len(lng) - lng.rfind('.')) > 7:
            lng = lng[0:(lng.rfind('.') + 7)]

        # ab is bikes
        # ap is places

        # docks
        docks = int(stn['ab']) + int(stn['ap'])

        # get name - tag differs by bss
        if stn['wcom'] == "" or stn['wcom'] is None:
            name = stn['name']
        else:
            name = stn['wcom']

        name = urllib.unquote_plus(name).encode('iso-8859-1').decode('utf8')
        if len(name.split(':')) > 1:
            name = name.split(' : ')[1]

        # we want stnid, lat, lng, docks, bikes, spaces, name, active
        clean_stations_list.append([stn['id'], lat, lng, str(docks), stn['ab'], stn['ap'], name, active])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False

    return clean_stations_list
