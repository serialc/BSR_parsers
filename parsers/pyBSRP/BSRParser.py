import os, imp

class BSRParser(object):
    """ Class for the retrieving data from BSS data feeds.
    Input required is the BSR data feed object
    Additional parameters can specify output, (array or string) or save (raw and cleaned) paths.
    """

    def __init__(self, bsr_feed):
        """Returns a BSRParser object containing feed details."""
        # Load the appropriate parser module
        self.proto = imp.load_source('protocol', os.path.dirname(os.path.abspath(__file__)) + '/protocols/' + bsr_feed['parsername'] + '.py')
        self.df = bsr_feed

        # set defaults
        self.utc = ''
        self.apikey = ''
        self.timeout = 20
        self.raw_data = False
        self.clean_data = False

    def set_timeout(self, timeout):
        """Set the timeout duration for scraping calls"""
        self.timeout = timeout

    def get_timeout(self):
        return self.timeout

    def retrieve(self):
        """Retrieves the parsed contents of the data feed from the operator's server."""
        try:
            # See if the the parser protocol has a scraper function
            self.raw_data = self.proto.scrape(self.df, self.apikey)
        except AttributeError:
            import urllib2
            from datetime import datetime
            # simple scrape
            try:
                self.utc = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
                res = urllib2.urlopen( self.df['feedurl'] + self.apikey, timeout=self.timeout)
                self.raw_data = res.read()
                if res.getcode() != 200:
                    print self.utc + ' ' + bsr_df['bssid'] + ' Failed to retrieve url=' + bsr_df['feedurl']
                    return False

            except (urllib2.URLError, urllib2.HTTPError) as e:
                print self.utc + ' ' + bsr_df['bssid'] + ' Failed to retrieve url=' + bsr_df['feedurl']
                return False

        # check data (self.raw_data)
        if self.raw_data == "" or self.raw_data == "False":
            print self.utc + ' ' + bsr_df['bssid'] + ' Retrieved url=' + bsr_df['feedurl'] + ' but contents are empty.'
            return False

        # Everything looks good
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
            fh.write(self.raw_data)
            fh.close()
        except:
            print self.utc + " Failed to save file path: " + path + fname
        return self

    def parse(self):
        if not self.raw_data:
            self.retrieve();
        self.clean_data = self.proto.parse(self.df, self.raw_data, self.utc)
        if not self.clean_data:
            print self.utc + " Failed to clean data."
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
            fh.write(self.schematize(schema=schema, return_type='string').encode('utf-8'))
            fh.close()
        except:
            print self.utc + " Failed to save file path: " + path + fname
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

    def schematize(self, schema='fullset', return_type='string'):
        """Returns the data in schematized format, array or string"""
        if not self.clean_data:
            self.parse()

        # self.clean_data contains
        # [0] stnid, [1] lat, [2] lng, [3] docks, [4] bikes, [5] spaces, [6] name
        headings = {'id':0, 'lat':1, 'lng':2, 'docks':3, 'bikes':4, 'spaces':5, 'name':6}
        if schema == 'fullset':
            schema_indices = range(7)
        elif schema == 'llstatus':
            schema_indices = [0, 1, 2, 4, 5]
        else:
            print self.utc + " Requested schema '" + schema + "' not found."
            return False

        output_array = []
        # build array with only the required columns
        for stn in self.clean_data:
            output_array.append( [ stn[i] for i in schema_indices ])

        # return array or string as requested
        if return_type == 'array':
            return output_array
        elif return_type == 'string':
            # add headings according to schema
            output_array = [[ ['id', 'lat', 'lng', 'docks', 'bikes', 'spaces', 'name'][i] for i in schema_indices ]] + output_array

            output_string = u''
            for line in output_array:
                output_string += "\t".join(str(part).decode('utf8') for part in line) + "\n"
            return output_string
        else:
            print self.utc + " Unknown output type '" + return_type + "' requested."
            return False
