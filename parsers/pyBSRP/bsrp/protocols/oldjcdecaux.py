# Parser: oldjcdecaux (Brisbane)
# Schema: llstatus

import urllib2
from datetime import datetime
from bs4 import BeautifulSoup
from bsrp import bsrputil

def scrape(df, apikey):

    # Part 1 of 2 - Requesting list of existing stations
    try:
        utc = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        res = urllib2.urlopen( df['feedurl'] + apikey, timeout=20)
        site_data_string = res.read()
        if not res or res.getcode() != 200:
            print utc + ' ' + df['bssid'] + ' Request code=' + res.getcode() + '. Failed to retrieve url=' + df['feedurl']
            return False
    except (urllib2.URLError, urllib2.HTTPError) as e:
        print utc + ' ' + df['bssid'] + ' Failed to retrieve url=' + df['feedurl']
        return False

    soup = BeautifulSoup(site_data_string)
    # go through and create a clean dict list
    stns_list = []
    for marker in soup.find_all('marker'):
        stns_list.append(marker)

    # Part 2 of 2 - Requesting individual stations
    data_list = []
    # append important info stn_list list
    for stn in stns_list:
        data_list.append([df['feedurl2'], stn['number'], df['bssid']])

    # MULTIPROCESSING
    # Returns array of XML
    return [stns_list, bsrputil.multiprocess_data(data_list)]

def parse(df, data, utc):
    # df is a dict with the following keys:
    # [u'feedurl', u'feedname', u'bssid', u'format', u'feedurl2', u'keyreq', u'parsername', u'rid']

    '''
    data contains a two element array:
    [0] - Array of BS4 tags containing station names, lat/lng
    [1] - Array of station bikes, spaces

        try:
            stn_res = urllib2.urlopen( df['feedurl2'] + stn['number'], timeout=20)
    For each station we have two parts therefore:
    <marker address="Regatta Ferry Terminal / Sylvan Rd" bonus="0" fulladdress="Regatta Ferry Terminal / Sylvan Rd  " lat="-27.483168" lng="152.996419" name="143 - REGATTA FERRY TERMINAL / SYLVAN RD" number="143" open="1"></marker>

    <station><available>15</available><free>5</free><total>21</total><ticket>0</ticket><open>1</open><updated>1452554641</updated><connected>1</connected></station>
    '''

    # check that both arrays are the same length
    if len(data[0]) != len(data[1]):
        print "Error in oldjcdecaux.py for " + df['bssid'] + ". The length of the two arrays is not the same!"

    # capture clean results in clean_stations_list
    # stnid, lat, lng, docks, bikes, spaces, name, open/active station
    clean_stations_list = []
    for stnnum in range(len(data[0])):
        # data[0] has BS4 tags
        stn_name = data[0][stnnum]
        # data[1] has text
        stn_state = BeautifulSoup(data[1][stnnum]).find('station')

        # open station? Active?
        stn_connected = 'no'
        if stn_state.connected.string == '1':
            stn_connected= 'yes'

        clean_stations_list.append([
            stn_name['number'],
            stn_name['lat'],
            stn_name['lng'],
            stn_state.total.string,
            stn_state.available.string,
            stn_state.free.string,
            stn_name['name'].encode('utf8'),
            stn_connected
            ])

    # check if we have some data
    if len(clean_stations_list) == 0:
        print utc + ' ' + df['bssid'] + " Parser oldjcdecaux.py did not find any station's data."
        return False
    
    return clean_stations_list
