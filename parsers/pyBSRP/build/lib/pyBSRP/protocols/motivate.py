# Parser: Motivate (e.g., NYC, Chattanooga, Chicago, SF, Toronto)
# Schema: llstatusname

import json, re

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # parse out desired info
    # does the file have valid content
    if re.match('false', data) or re.match("\"\"(\s)+\n?", data) or re.match('[\s\"]*<html><head><title>Apache Tomcat', data):
        print utc + ' ' + df['bssid'] + " Parser found file to be empty of valid content."
        return False

    # parse json data
    try:
        data_json = json.loads(data)
    except ValueError:
        print utc + ' ' + df['bssid'] + " Parsing JSON failed for " + df['feedurl']
        return False
    
    # check if we retreived the station list
    if not data_json.has_key('stationBeanList'):
        print utc + ' ' + df['bssid'] + " Data does not contain 'stationBeanList' element'. No data found."
        return False
    
    # open the stationBeanList now that we know it exists
    stations_list = data_json['stationBeanList']

    # check for the size of stationBeanList
    if len(stations_list) <= 1:
        print utc + ' ' + df['bssid'] + " Data does not contain 'stationBeanList' element'. No data found."
        return False

    # capture clean results in clean_stations_list
    clean_stations_list = []
    for stn_dict in stations_list:
        stnid = -1
        if 'uaid' in stn_dict:
        # try chattanooga style id
            stnid = stn_dict['uaid']
        elif 'id' in stn_dict:
            # try
            stnid = stn_dict['id']
        else:
            print utc + ' ' + df['bssid'] + " Parser did not find valid id/uaid in for line: " + str(stn_dict)
            return False

        # build the list of valid data
        # check if the station is online
        if stn_dict['statusValue'] == 'In Service':
            # stnid, lat, lng, docks, bikes, spaces, name, active
            clean_stations_list.append([str(stnid), str(stn_dict['latitude']), str(stn_dict['longitude']), str(stn_dict['totalDocks']), str(stn_dict['availableBikes']), str(stn_dict['availableDocks']), stn_dict['stationName'], 'yes'])
        else:
            # The station can be 'Not In Service', 'Planned' or something unknown
            try:
                clean_stations_list.append([str(int(stnid)), str(stn_dict['latitude']), str(stn_dict['longitude']), str(stn_dict['totalDocks']), str(stn_dict['availableBikes']), str(stn_dict['availableDocks']), stn_dict['stationName'], 'no'])
            except:
                # information is missing to provide the full set, just skip
                continue

    # check if we have some data
    if len(clean_stations_list) == 0:
        print utc + ' ' + df['bssid'] + " Parser did not find any station's data."
        return False

    return clean_stations_list
