# Parser: bcycle (e.g., Vancouver)

import json, re
from bs4 import BeautifulSoup

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # parse out desired info
    data = data.split("\n")

    clean_stations_list = []
    antidupedict = dict()

    # parse line by line
    for line in data:
        # remove line returns if any (shouldn't be)
        line = line.strip()
        
        # skip any lines that are blank
        if line == "":
            continue
        
        data_match = re.match("var stations = \[\[", line)

        if data_match:

            # line holds all the goodies
            line = line.lstrip("var stations = [[")
            line = line.strip("],];")

            for marker in line.split("],["):

                parts = marker.split(',')
                try:
                    soup = BeautifulSoup(parts[0], features="html.parser")
                    name = soup.find(class_="titleveloh").text
                except AttributeError:
                    # this is because they also pass other non-BSS station junk in here that is formatted funny, just skip
                    continue
                #print(parts)

                stnid = re.search("photos/(.+)\.jpg", soup.find(class_="photoimg").attrs['style'])
                if not stnid:
                    # probably not a BSS station, other marker type
                    continue

                # should be only/first item in list
                stnid = stnid.groups()[0]

                tds = soup.find_all("td")
                if len(tds) != 6:
                    # probably not a BSS station, other marker type
                    continue

                bikes, docks = tds[1].text.split('/')
                free_docks = str(int(docks) - int(bikes))

                lat = parts[1].strip()
                lng = parts[2].strip()
                
                # stnid, lat, lng, docks, bikes, spaces, name, active
                clean_stations_list.append([stnid, lat, lng, docks, bikes, free_docks, name, 'yes'])

            # We only want this one line, break out of html file
            break

    # check if we have retrieved any data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False

    return clean_stations_list
