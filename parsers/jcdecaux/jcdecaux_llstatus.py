# Parser: jcdecaux (e.g., Paris, Lyon, Strassbourg, Luxembourg)
# Schema: llstatus

import json, re, urllib2, os
from datetime import datetime

def scrape(url, data_path, error_file, timeout_sec=20, apikey):
    # retrieve data
    try:
        # https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={api_key}
        res = urllib2.urlopen( url + apikey, timeout=timeout_sec)
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

    # parse json data
    try:
        json_data = json.loads(big_string)
    except ValueError:
        log_error(error_file, "Parsing JSON failed for " + source_file)
        return False

    # capture clean results in clean_stations_list
    # llstatus schema: id, lat, long, bikes, spaces
    clean_stations_list = []
    for stn in json_data:
        clean_stations_list.append([stn['number'], stn['position']['lat'], stn['position']['lng'], stn['available_bikes'], stn['available_bike_stands']])

    # check if we have some data
    if len(clean_stations_list) == 0:
        log_error(error_file, "Parsing completed but no data found for " + source_file)
        return False

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
