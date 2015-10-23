# Parser: jcdecaux (e.g., Paris, Lyon, Strassbourg, Luxembourg)
# Schema: llstatus

import json, re, urllib2, os
from datetime import datetime

def get(bsr_df, save_dir='', timeout_sec=20, apikey='', save_raw=False, save_raw_dir=''):
    # bsr_df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # check an apikey is provided
    if apikey == '':
        print bsr_df['bssid'] + ' An API key from JCDecaux is required. See https://developer.jcdecaux.com'
        return False

    # 1. retrieve data
    try:
        # https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}
        utc = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        res = urllib2.urlopen( bsr_df['feedurl'] + apikey, timeout=timeout_sec)
        url_data = res.read()
    except (urllib2.URLError, urllib2.HTTPError) as e:
        print utc + ' ' + bsr_df['bssid'] + ' Failed to retrieve url=' + bsr_df['feedurl']
        return False

    # check data
    if url_data == "" or url_data == "False" or res.getcode() != 200:
        print utc + ' ' + bsr_df['bssid'] + ' Retrieved url=' + bsr_df['feedurl'] + ' but contents are empty.'
        return False

    if save_raw:
        fh = open(save_dir + bsr_df['bssid'] + '_raw_' + utc + '.txt', 'w')
        fh.write(url_data)
        fh.close()

    # 2. parse out desired info
    # parse json data
    try:
        json_data = json.loads(url_data)
    except ValueError:
        print utc + ' ' + bsr_df['bssid'] + " Parsing JSON failed for " + bsr_df['feedurl']
        return False

    # capture clean results in clean_stations_list
    # llstatus schema: id, lat, long, bikes, spaces
    clean_stations_list = []
    for stn in json_data:
        clean_stations_list.append([stn['number'], stn['position']['lat'], stn['position']['lng'], stn['available_bikes'], stn['available_bike_stands']])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print utc + ' ' + bsr_df['bssid'] + " Parser did not find any station's data."
        return False

    # 3. save parsed data
    # convert to a big string and add headers
    output = u'id\tlat\tlong\tbikes\tspaces\n'
    for line in clean_stations_list:
        output += "\t".join(str(part) for part in line) + "\n"
    
    # save
    fh = open(save_dir + bsr_df['bssid'] + '_' + utc + '.txt', 'w')
    fh.write(output.encode('utf8'))
    fh.close()
