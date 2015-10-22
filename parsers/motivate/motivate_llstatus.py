# Parser: Motivate (e.g., NYC, Chattanooga, Chicago, SF, Toronto)
# Schema: llstatus

import json, re, urllib2, os
from datetime import datetime

def scrape(url, data_path, error_file, timeout_sec=20):
    # retrieve data
    try:
        res = urllib2.urlopen( url, timeout=timeout_sec)
        utc = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        url_data = res.read()
    except (urllib2.URLError, urllib2.HTTPError) as e:
        log_error(error_file, 'Failed to retrieve url=' + url)
        return False

    # check data
    if url_data == "" or url_data == "False" or res.getcode() != 200:
        log_error(error_file, 'Retrieved url=' + url + ' but contents are empty.')
        return False

    filename = data_path.strip('/') + '/' + utc + '.txt'
    fh = open(filename, 'w')
    fh.write(url_data)
    fh.close()

    return filename 

def parse(source_file, output_file, error_file, delete_source=False):

    # Part 1
    # parse out desired info
    ########################
    
    fh = open(source_file, 'r')
    big_string = fh.read()
    fh.close()

    # does the file have valid content
    if re.match('false', big_string) or re.match("\"\"(\s)+\n?", big_string) or re.match('[\s\"]*<html><head><title>Apache Tomcat', big_string):
        log_error(error_file, 'Parser found file to be empty of valid content.')
        return False

    # parse json data
    data_json = json.loads(big_string)
    
    # check if we retreived the station list
    if not data_json.has_key('stationBeanList'):
        log_error(error_file, "Parser didn't find 'stationBeanList'.")
        return False
    
    # open the stationBeanList now that we know it exists
    stations_list = data_json['stationBeanList']

    # check for the size of stationBeanList
    if len(stations_list) <= 1:
        log_error(error_file, "Parser found no stations.")
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
            log_error(error_file, "Parser did not find valid id/uaid in file: " + file + " for line: " + str(stn_dict))
            return False

        # build the list of valid data
        clean_stations_list.append([str(int(stnid)), str(stn_dict['latitude']), str(stn_dict['longitude']), str(stn_dict['availableBikes']), str(stn_dict['availableDocks'])])

    # Part 2
    # save cleaned version, and move all parsed files to the appropriate folder
    ###########################################################################
    
    # convert to a big string
    output = u''
    for line in clean_stations_list:
        output += "\t".join(str(part) for part in line) + "\n"
    
    # move/archive all files from this timestamp
    fh = open(output_file, 'w')
    fh.write(output.encode('utf8'))
    fh.close()

    if delete_source:
        os.remove(source_file)

def log_error(file, msg):
    fh = open(file, 'a')
    fh.write(datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S') + ':' + msg)
    fh.close()
