import urllib2, json

# Let's grab the lineage of the feed I want
chicago = urllib2.urlopen('http://bikeshare-research.org/api/v1/categories/data/lineages/9/')
chicago_feeds = chicago.read()
# [{"rid":"7","bssid":"chicago","feedname":"Divvy JSON","feedurl":"http://www.divvybikes.com/stations/json","feedurl2":"","format":"json","keyreq":"no","parsername":null},
#  {"rid":"9","bssid":"chicago","feedname":"Divvy JSON","feedurl":"http://www.divvybikes.com/stations/json","feedurl2":"","format":"json","keyreq":"no","parsername":"motivate"}]
# We see that the parsername was specified in the last update.

# let's use the last update
chicago_feeds_json = json.loads(chicago_feeds)
chicago_data_feed = chicago_feeds_json[len(chicago_feeds_json)-1]

# Get parsers to easily retrieve data by cloning the BSR_parsers repository locally:
# git clone https://github.com/serialc/BSR_parsers.git

# load the python parser
from bsrp import BSRParser

# Example 1: Chicago and method chaining
# create instance of parser with data feed details
parser = BSRParser(chicago_data_feed)

# retrieving will return False or, if successfull, the parser object (self)
parser.retrieve()

# save cleaned data locally according to the default schema (fullset)
parser.save('')

# save the raw data if you wish
parser.save_raw('')

# retrieve the data in array form, perhaps to insert into DB
data_array = parser.get_data_array()

# or, since most of these methods return the object/self, do it all in one line
data_array = parser.retrieve().save('').save_raw('').get_data_array()

# Example 2: Lyon and data feed API keys
# For lyon we have already identified the feed we would like:
lyon = urllib2.urlopen('http://bikeshare-research.org/api/v1/categories/data/records/10')
lyon_data_feed = json.loads(lyon.read())[0]

parser = BSRParser(lyon_data_feed)
# we don't need to explicitly call retrieve(), saving will do so if necessary
parser.set_apikey('YOUR JCDECAUX API KEY').retrieve().save_raw('').save('')
# data is saved locally, done

# You can convert the UTC time to the local timezone using the timezome attribute in '/systems/lyon/categories/base/'
# Add to your DB
