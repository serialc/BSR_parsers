# Parser: bcycle (e.g., Philadelphia, Indianapolis, Denver, Austin)

import json, re

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # parse out desired info
    data = data.split("\n")

    # parser helpers
    hot_zone = False
    hot_line = 1
    stn_dict = dict()
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
                ll_match = re.match("var point = new google.maps.LatLng\(([\-0-9.]+),\s*([\-0-9.]+)\)", line)

                if ll_match:
                    stn_dict['lat'] = ll_match.group(1)
                    stn_dict['lng'] = ll_match.group(2)
            
                # Example of string
                # var marker = new createMarker(point, "<div class='markerTitle'><h3>Memorial Union</h3></div><div class='markerPublicText'><h5></h5></div><div class='markerAddress'>1401 Administrative Ave<br />Fargo, ND 58102</div><div class='markerAvail'><div style='float: left; width: 50%'><h3>1</h3>Bikes</div><div style='float: left; width: 50%'><h3>29</h3>Docks</div></div>", icon, back, false);
                # Old matching
                # attr_match = re.match("var marker = new createMarker\(point.+<div class='markerTitle'><h3>([^<]+)</h3></div>.+<strong>([0-9]*)</strong>.+<strong>([0-9]*)</strong>([0-9]*).+", line)
                # New matching
                attr_match = re.match("var marker = new createMarker\(point.+<div class='markerTitle'><h3>([^<]+)</h3></div>.+<h3>([0-9]*)</h3>.+<h3>([0-9]*)</h3>", line)

                if attr_match:
                    # we *should* have a full data set now, note there are no ids! id = 0
                    name = attr_match.group(1)
                    bikes = int(attr_match.group(2))
                    spaces = int(attr_match.group(3))

                    # stnid, lat, lng, docks, bikes, spaces, name, active
                    clean_stations_list.append([0, stn_dict['lat'], stn_dict['lng'], bikes + spaces, bikes, spaces, name, 'yes'])

                    # reset to -1
                    stn_dict['lat'] = -1
                    stn_dict['lng'] = -1

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
