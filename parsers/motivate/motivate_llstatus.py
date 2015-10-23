# Parser: Motivate (e.g., NYC, Chattanooga, Chicago, SF, Toronto)
# Schema: llstatus

import json, re, urllib2, os
from datetime import datetime

def get(bsr_df, save_dir='', timeout_sec=20, apikey='', save_raw=False, save_raw_dir=''):
    # bsr_df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    # 1. retrieve data
    try:
        utc = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        res = urllib2.urlopen( bsr_df['feedurl'], timeout=timeout_sec)
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
    # does the file have valid content
    if re.match('false', url_data) or re.match("\"\"(\s)+\n?", url_data) or re.match('[\s\"]*<html><head><title>Apache Tomcat', url_data):
        log_error(error_file, 'Parser found file to be empty of valid content.')
        print utc + ' ' + bsr_df['bssid'] + " Parser found file to be empty of valid content."
        return False

    # parse json data
    try:
        data_json = json.loads(url_data)
    except ValueError:
        print utc + ' ' + bsr_df['bssid'] + " Parsing JSON failed for " + bsr_df['feedurl']
        return False
    
    # check if we retreived the station list
    if not data_json.has_key('stationBeanList'):
        print utc + ' ' + bsr_df['bssid'] + " Data does not contain 'stationBeanList' element'. No data found."
        return False
    
    # open the stationBeanList now that we know it exists
    stations_list = data_json['stationBeanList']

    # check for the size of stationBeanList
    if len(stations_list) <= 1:
        print utc + ' ' + bsr_df['bssid'] + " Data does not contain 'stationBeanList' element'. No data found."
        return False

    # capture clean results in clean_stations_list
    # llstatus schema: id, lat, long, bikes, spaces
    clean_stations_list = []
    for stn_dict in stations_list:
        # check if the station is online
        if stn_dict['statusValue'] != 'In Service':
            # The station can be 'Not In Service' or 'Planned'
            # skip tracking this station, go to next
            continue

        stnid = -1
        if 'uaid' in stn_dict:
        # try chattanooga style id
            stnid = stn_dict['uaid']
        elif 'id' in stn_dict:
            # try
            stnid = stn_dict['id']
        else:
            print utc + ' ' + bsr_df['bssid'] + " Parser did not find valid id/uaid in for line: " + str(stn_dict)
            return False

        # build the list of valid data
        clean_stations_list.append([str(int(stnid)), str(stn_dict['latitude']), str(stn_dict['longitude']), str(stn_dict['availableBikes']), str(stn_dict['availableDocks'])])

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
