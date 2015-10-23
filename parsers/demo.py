# A few things we need to know generally
# - path to store raw and cleaned data, perhaps related to bssid
# - error log file
# - do we want to delete raw file

# And for each BSS 
# - url
# - second url - and whether it exists

import urllib2, json

# CHICAGO - doing it slowly
###########################
# let's retrieve the data feeds available for Chicago
chicago = urllib2.urlopen('http://bikeshare-research.org/api/v1/systems/chicago/categories/data')
# read the data
chicago_feeds = chicago.read()
# '[{"rid":"9","bssid":"chicago","feedname":"Divvy JSON","feedurl":"http://www.divvybikes.com/stations/json","feedurl2":"","format":"json","keyreq":"no","parsername":"motivate"}]'

# We can see no apikey is necessary and we have the url - not much more is needed. We could save this locally and not retrieve it from BSR again. 

# Alternatively, if we want to dynamically reload this we should keep in mind that new feeds may be added to this list, an XML one for example, and our feed may no longer be the first element in the list.
# We can modify the API request to this specific rid which will return only this row in this state indefinitely.
chicago = urllib2.urlopen('http://bikeshare-research.org/api/v1/categories/data/records/9/')
chicago_feeds = chicago.read()
# '[{"rid":"9","bssid":"chicago","feedname":"Divvy JSON","feedurl":"http://www.divvybikes.com/stations/json","feedurl2":"","format":"json","keyreq":"no","parsername":"motivate"}]'

# An updated url may be provided at some point however, so we may want to keep track of this feed's lineage/evolution.
chicago = urllib2.urlopen('http://bikeshare-research.org/api/v1/categories/data/lineages/9/')
chicago_feeds = chicago.read()
# [{"rid":"7","bssid":"chicago","feedname":"Divvy JSON","feedurl":"http://www.divvybikes.com/stations/json","feedurl2":"","format":"json","keyreq":"no","parsername":null},
#  {"rid":"9","bssid":"chicago","feedname":"Divvy JSON","feedurl":"http://www.divvybikes.com/stations/json","feedurl2":"","format":"json","keyreq":"no","parsername":"motivate"}]
# We see that the parsername was specified in the last update.

# Let's assume we trust BSR's live data, every month perhaps I could update my data using:
chicago_feeds_json = json.loads(chicago_feeds)
chicago_data_feed = chicago_feeds_json[len(chicago_feeds_json)-1]
# save chicago_data_feed

# Let's move on and get some parsers so we can easily retrieve data
# We have ahead of time cloned the BSR_parsers repository locally:
# git clone https://github.com/serialc/BSR_parsers.git
# Make sure you've added the necessary '__init__.py' to your BSR_parsers path if necessary

# All we need to do now is:
# 1. import the module
# 2. call the scrape function with the provided
# 3. parse functions

# Given chicago_data_feed['parsername'] defines the module to use as 'motivate' we could automate the loading of the parser module, but do it manually here
from motivate import motivate_llstatus as mot
mot.get(chicago_data_feed, save_raw=True)
# data is saved locally, done

# LYON
#########################
# For lyon we have already identified the feed we would like:
lyon = urllib2.urlopen('http://bikeshare-research.org/api/v1/categories/data/records/10')
lyon_data_feed = json.loads(lyon.read())[0]

from jcdecaux import jcdecaux_llstatus as jcd
jcd.get(lyon_data_feed, apikey='') # provide your key! See https://developer.jcdecaux.com
# data is saved locally, done

# You could convert the UTC time to the local timezone using the timezome attribute in '/systems/lyon/categories/base/'
# Add to your DB
