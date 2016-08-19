# Parser: bcycle (e.g., Vancouver)

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
        
        json_match = re.match("<script>jQuery.extend\(Drupal.settings, (.+)\);</script>", line)

        if json_match:

            jdata = json.loads(json_match.group(1))

            for marker in jdata['markers']:
                if marker['poi'] == False:
                    stnid = marker['title'].split(' ')[0]
                    name = ' '.join(marker['title'].split(' ')[1:])
                    docks = str(int(marker['avl_bikes']) + int(marker['free_slots']))

                    if stnid in antidupedict:
                        continue
                    else:
                        antidupedict[stnid] = True
                    
                    # stnid, lat, lng, docks, bikes, spaces, name, active
                    clean_stations_list.append([stnid, marker['latitude'], marker['longitude'], docks, marker['avl_bikes'], marker['free_slots'], name, 'yes'])

            # We only want this one line, break out of html file
            break

    # check if we have retrieved any data
    if len(clean_stations_list) == 0:
        print utc + ' ' + df['bssid'] + " Parser did not find any station's data."
        return False

    return clean_stations_list
