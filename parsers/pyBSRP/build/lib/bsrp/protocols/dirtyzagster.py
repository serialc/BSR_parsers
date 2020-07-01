# Parser: zagster (e.g., Wichita)

import json, re

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
        
        json_match = re.match("var phpLocationsData = JSON\.parse\('(.+)'\);", line)

        if json_match:

            stns = json.loads(json_match.group(1))

            for stn in stns:
#{"StationID":"04423b00-e62c-451c-909a-f5e471e674fa","StationName":"WSU - Metroplex","NetworkID":"7d3b92d2-e72b-4683-a41b-3cf240a48c7a","CreatedOn":"/Date(1550168930000)/","MondayOpen":"00:00","MondayClose":"24:00","TuesdayOpen":"00:00","TuesdayClose":"24:00","WednesdayOpen":"00:00","WednesdayClose":"24:00","ThursdayOpen":"00:00","ThursdayClose":"24:00","FridayOpen":"00:00","FridayClose":"24:00","SaturdayOpen":"00:00","SaturdayClose":"24:00","SundayOpen":"00:00","SundayClose":"24:00","Address":"","Lat":"37.735413","Lng":"-97.278793","DockType":"K1"}
                stnid = stn['StationID']
                name = stn['StationName']
                docks = ''
                bikes = ''
                spaces = ''

                # stnid, lat, lng, docks, bikes, spaces, name, active
                clean_stations_list.append([stnid, stn['Lat'], stn['Lng'], docks, bikes, spaces, name, 'yes'])

            # We only want this one line, break out of html file
            break

    # check if we have retrieved any data
    if len(clean_stations_list) == 0:
        print(utc + ' ' + df['bssid'] + " Parser did not find any station's data.")
        return False

    return clean_stations_list
