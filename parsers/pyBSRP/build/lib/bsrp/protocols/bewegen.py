# Parser: bewegen (baltimore)
import json
from bs4 import BeautifulSoup

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # data is json list of stations
    try:
        json_data = json.loads(data)
    except ValueError:
        print(utc + ' ' + df['bssid'] + " Parsing JSON failed for " + df['feedurl'])
        return False

    # capture clean results in clean_stations_list
    # stnid, lat, lng, docks, bikes, spaces, name
    clean_stations_list = []
    for stn in json_data:

        soup = BeautifulSoup(stn['popup'], "html.parser")
        b = soup.find_all('b')
        bikes = int(b[0].string)
        spaces = int(b[1].string)

        if stn['type'] == "OPEN":
            active = 'yes'
        else:
            active = 'no'

        stnid = stn['serial_number'].split(' ')
        stnid = stnid.pop()
        
        clean_stations_list.append([stnid, stn['location'][0], stn['location'][1], str(bikes + spaces), bikes, spaces, stn['name'], active])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False

    return clean_stations_list
