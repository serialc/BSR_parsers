# Parser: smoovxml (montpellier, clermon ferrand, avignon, valence)
from bs4 import BeautifulSoup

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # parse out desired info
    soup = BeautifulSoup(data, "html.parser")
    
    # capture clean results in clean_stations_list
    clean_stations_list = []
    
    for station in soup.find_all('si'):

        # skip bad lines
        if station['na'] == '' and station['id'] == '':
            continue

        # total number of docks
        docks = int(station['av']) + int(station['fr'])

        # we want stnid, lat, lng, docks, bikes, spaces, name, active
        clean_stations_list.append([station['id'], station['la'], station['lg'], str(docks), station['av'], station['av'], station['na'], 'yes'])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False

    return clean_stations_list
