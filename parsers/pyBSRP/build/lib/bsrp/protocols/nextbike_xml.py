# Parser: nextbike_xml (Note it downloads a large file for the whole world)
from bs4 import BeautifulSoup

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # parse out desired info
    soup = BeautifulSoup(data, "html.parser")

    # get this system from the large list of all nextbike systems
    nbsys = soup.find('country', attrs={"name":df['feedname']})
    
    # capture clean results in clean_stations_list
    clean_stations_list = []

    for stn in nbsys.find_all('place'):

        # status, unknown, assume if in list it is
        active = 'yes'

        try:
            # we want stnid, lat, lng, docks, bikes, spaces, name, active
            clean_stations_list.append([stn['number'], round(float(stn['lat']), 5), round(float(stn['lng']), 5), stn['bike_racks'], stn['bikes'], stn['free_racks'], stn['name'], active])
        except KeyError:
            # something is strange with this station, skip
            continue

    # check if we have some data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False

    return clean_stations_list
