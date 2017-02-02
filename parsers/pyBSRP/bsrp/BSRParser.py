import os, imp, requests, json, imp, sys
from datetime import datetime
from bsrp import bsrputil

class BSRParser(object):
    """ Class for the retrieving data from BSS data feeds.
    Input required is the BSR data feed object
    Additional parameters can specify output, (array or string) or save (raw and cleaned) paths.
    """

    def __init__(self, bsr_feed):
        """Returns a BSRParser object containing feed details."""

        # Check if a parser module is set in feed
        if bsr_feed['parsername'] is None:
            print("This feed has no designated parser set. Update on BSR and try again.")
            return

        # Load the appropriate parser module
        try:
            del sys.modules['protocol']
        except KeyError:
            # module is not yet loaded
            pass
        self.proto = imp.load_source('protocol', os.path.dirname(os.path.abspath(__file__)) + '/protocols/' + bsr_feed['parsername'] + '.py')
        #self.proto = imp.load_source('protocol', '/protocols/' + bsr_feed['parsername'] + '.py')
        self.df = bsr_feed

        # set defaults
        self.utc = ''
        self.apikey = ''
        self.timeout = 20
        self.raw_data = False
        self.clean_data = False
        self.complex_scrape = False

    def set_timeout(self, timeout):
        """Set the timeout duration for scraping calls"""
        self.timeout = timeout

    def get_timeout(self):
        return self.timeout

    def retrieve(self):
        """Retrieves the parsed contents of the data feed from the operator's server."""

        if self.df['keyreq'] == 'yes' and self.apikey == '':
            print("Gathering data for this BSS (" + self.df['bssid'] + ") and parser (" + self.df['parsername'] + ") requires a key according to BSR. None is provided. Trying anyways.")

        # The time of the data retrieval
        self.utc = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')

        # See if the the parser protocol has a scraper function
        if "scrape" in dir(self.proto):
            self.raw_data = self.proto.scrape(self.df, self.apikey)
            self.complex_scrape = True
        else:

            # Add apikey to end of request - at worst it's empty
            headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) Gecko/20100101 Firefox/48.0',
                    'accept-encoding':'gzip, deflate, br',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'cache-control':'no-cache',
                    'accept-language':'en-US,en;q=0.5'
                    }

            r = requests.get( self.df['feedurl'] + self.apikey, headers=headers)

            if r.status_code == 200:
                self.raw_data = r.text
            else:
                print(r.status_code, r.headers['content-type'], r.encoding, r.content)
                print(self.utc + ' ' + self.df['bssid'] + ' Failed to retrieve url=' + self.df['feedurl'])
                return False

        # check data (self.raw_data)
        if self.raw_data == "" or self.raw_data == "False" or self.raw_data == False:
            print(self.utc + ' ' + self.df['bssid'] + ' Retrieved url=' + self.df['feedurl'] + ' but contents are empty.')
            return False

        # Everything looks good
        return self

    def retrieve_raw(self, filepath):
        """Retrieves file and stores it as if it had been downloaded, allowing parsing without downloading."""
        fh = open(filepath, 'r')
        self.raw_data = fh.read()
        fh.close()
        return self

    def set_apikey(self, apikey):
        """Provides the APIKEY for the BSS operator data feed."""
        self.apikey = apikey
        return self

    def save_raw(self, path):
        """Saves raw downloaded data into provided path. Filename will have format "[bssid] [UTC date time].txt". E.g., "boston_2015-10-31_13:26:52.txt" """
        if not self.raw_data:
            self.retrieve();

        try:
            fname = 'raw_' + self.df['bssid'] + '_' + self.utc + '.txt'
            fh = open(path + fname, 'w')

            # check type of raw_data
            if isinstance(self.raw_data, unicode):
                fh.write(self.raw_data.encode('utf-8'))
            elif isinstance(self.raw_data, dict):
                fh.write(json.dumps(self.raw_data))
            elif isinstance(self.raw_data, str):
                fh.write(self.raw_data)
            else:
                # try this for other data types
                fh.write(self.raw_data)
            fh.close()
        except:
            print(self.utc + " Failed to save file path: " + path + fname)
        return self

    def parse(self):
        if not self.raw_data:
            self.retrieve();

        self.clean_data = self.proto.parse(self.df, self.raw_data, self.utc)

        if not self.clean_data:
            print(self.utc + " Failed to clean data.")
            return False
        return self

    def get_raw(self):
        if not self.raw_data:
            self.retrieve();
        return self.raw_data

    def save(self, path, schema='fullset'):
        """Saves raw downloaded data into provided path. Filename will have format "[bssid] [UTC date time].txt". E.g., "boston_2015-10-31_13:26:52.txt" """
        if not self.raw_data:
            self.retrieve();
        if not self.clean_data:
            self.parse()

        fname = self.df['bssid'] + '_' + self.utc + '.txt'
        try:
            fh = open(path + fname, 'w')
            fh.write(self.schematize(schema=schema, return_type='string'))
            fh.close()
        except:
            print(self.utc + " Failed to save file path: " + path + fname)
            return False
        return self

    def get_data_array(self, schema='fullset'):
        """Returns the data in array format without headers according to schema formatting"""
        if not self.raw_data:
            self.retrieve();
        if not self.clean_data:
            self.parse()
        return self.schematize(schema=schema, return_type='array')

    def get_string(self, schema='fullset'):
        """Returns the data in string format with headers according to schema formatting"""
        if not self.raw_data:
            self.retrieve();
        if not self.clean_data:
            self.parse()
        return self.schematize(schema, 'string')

    def schematize(self, schema='fullset', return_type='string', sep=''):
        """Returns the data in schematized format, array or string"""

        # Check that we have data to schematize
        if not self.clean_data:
            self.parse()
            if not self.clean_data:
                print(self.utc + " Unable to retrieve data so abandoning schematization.")
                return False

        # self.clean_data contains
        # [0] stnid, [1] lat, [2] lng, [3] docks, [4] bikes, [5] spaces, [6] name, [7] active
        headings = {'id':0, 'lat':1, 'lng':2, 'docks':3, 'bikes':4, 'spaces':5, 'name':6, 'active':7}
        headingsa = ['id', 'lat', 'lng', 'docks', 'bikes', 'spaces', 'name', 'active'] # don't generate this using keys() - order is primordial!

        # DEFINE what headings/items are included in schema
        if schema == 'fullset':
            schema_indices = range(8)
        elif schema == 'llstatus':
            schema_indices = [0, 1, 2, 4, 5]
        else:
            print(self.utc + " Requested schema '" + schema + "' not found.")
            return False

        # DEFINE separator according to schema but allow overide
        if sep == '':
            if schema == 'fullset':
                sep = '\t'
            elif schema == 'llstatus':
                sep = '\t'
            else:
                print(self.utc + " Schema '" + schema + "' does not have a separator definition.")
                return False
        # sep is defined

        output_array = []
        # build array with only the required columns
        for stn in self.clean_data:
            output_array.append( [ stn[i] for i in schema_indices ])

        # return array or string as requested
        if return_type == 'array':
            return output_array
        elif return_type == 'string':
            # add headings according to schema
            output_array = [[ headingsa[i] for i in schema_indices ]] + output_array

            output_string = ''
            for line in output_array:
                line_array = []
                #output_string += sep.join(str(part).decode('utf8') for part in line) + "\n"
                # parse out parts differently depending on type
                for part in line:
                    if isinstance(part, unicode):
                        line_array.append(str(part.encode('utf8')))
                    elif isinstance(part, str):
                        line_array.append(part)
                    else:
                        line_array.append(str(part))
                # recombine into string with separations defined by sep
                output_string += sep.join(line_array) + "\n"

            # return the string in correct format
            if isinstance(output_string, unicode):
                return output_string.encode('utf-8')
            # type str
            return output_string
        else:
            print(self.utc + " Unknown output type '" + return_type + "' requested.")
            return False
