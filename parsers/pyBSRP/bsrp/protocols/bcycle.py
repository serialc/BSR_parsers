# Parser: bcycle (e.g., Philadelphia, Indianapolis, Denver, Austin)

import json, re
from bs4 import BeautifulSoup

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # parse out desired info
    data = data.split("\n")

    # parser helpers
    hot_zone = False
    hot_line = 1
    stn_dict = dict()
    active_available = 'no'
    clean_stations_list = []

    # parse line by line
    for line in data:
        # remove line returns if any
        line = line.strip()
        
        # skip any lines that are blank
        if line == "" or line == "{":
            continue
        
        # detect end of hot zone
        if line == "}":
            hot_zone = False
            
        if hot_zone:
            # start parsing each line for lat/long or attributes
            try:
                active_match = re.match("var back = '(.+)';", line)
                if active_match:
                    if active_match.group(1) == 'makerAvailable' or active_match.group(1) == 'infowin-available':
                        active_available = 'yes'
                    # else it stays 'no'

                ll_match = re.match("var point = new google.maps.LatLng\(([\-0-9.]+),\s*([\-0-9.]+)\)", line)

                if ll_match:
                    stn_dict['lat'] = ll_match.group(1)
                    stn_dict['lng'] = ll_match.group(2)
            
                # Match the html containing name, bikes, spaces
                xml_match = re.match("var marker = new createMarker\(point, \"(.+)\",", line)

                if xml_match:
                    soup = BeautifulSoup(xml_match.group(1))
                    # we *should* have a full data set now, note there are no ids! id = 0
                    # determine type of syntax
                    if len(soup.find_all('strong')) == 3:
                        soupparts = soup.find_all('strong')
                    else:
                        soupparts = soup.find_all('h3')

                    name = soupparts[0].string.encode('utf8')
                    bikes = soupparts[1].string
                    spaces = soupparts[2].string
                    docks = str(int(bikes) + int(spaces))

                    # stnid, lat, lng, docks, bikes, spaces, name, active
                    clean_stations_list.append([0, stn_dict['lat'], stn_dict['lng'], docks, bikes, spaces, name, active_available])

                    # reset
                    stn_dict['lat'] = -1
                    stn_dict['lng'] = -1
                    active_available = 'no'

            except (IndexError, KeyError) as e:
                print(utc + ' ' + df['bssid'] + " Something is wrong with the line:\n" + line + "\nParsing for this BSS stopped. Error msg: \n" + str(e))
                return

        # check if this line is the start of the 'hot' zone
        match = re.search(r"function LoadKiosks()", line)
        if match:
            hot_zone = True

    # check if we have some data
    if len(clean_stations_list) == 0:
        print utc + ' ' + df['bssid'] + " Parser did not find any station's data."
        return False

    return clean_stations_list
