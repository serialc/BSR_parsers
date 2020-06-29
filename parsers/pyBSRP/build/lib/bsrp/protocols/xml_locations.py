# Parser: xml_locations (made for Citi Bike Miami Beach)
from bs4 import BeautifulSoup

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # parse out desired info
    soup = BeautifulSoup(data, "html.parser")

    # capture clean results in clean_stations_list
    clean_stations_list = []

    for stn in soup.find_all('location'):

        # status, unknown, assume if in list it is
        active = 'yes'

        docks = int(stn.dockings.string) + int(stn.bikes.string)

        try:
            # we want stnid, lat, lng, docks, bikes, spaces, name, active
            clean_stations_list.append([stn.id.string, round(float(stn.latitude.string), 5), round(float(stn.longitude.string), 5), docks, int(stn.bikes.string), int(stn.dockings.string), stn.address.string, active])
        except KeyError:
            # something is strange with this station, skip
            continue

    # check if we have some data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False

    return clean_stations_list
