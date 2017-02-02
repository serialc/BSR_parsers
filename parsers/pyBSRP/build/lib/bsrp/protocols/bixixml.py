# Parser: bixixml (For older bixi streams, used to be common)
from bs4 import BeautifulSoup

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # parse out desired info
    soup = BeautifulSoup(data)
    
    # capture clean results in clean_stations_list
    clean_stations_list = []
    
    for station in soup.find_all('station'):

        # total number of docks
        docks = int(station.nbemptydocks.string) + int(station.nbbikes.string)

        # status
        if station.locked.string == 'false' and station.installed.string == 'true':
            status = 'yes'
        else:
            status = 'no'

        # we want stnid, lat, lng, docks, bikes, spaces, name, active
        clean_stations_list.append([station.id.string, station.lat.string, station.long.string, str(docks), station.nbbikes.string, station.nbemptydocks.string, station.find('name').string, status])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False

    return clean_stations_list
