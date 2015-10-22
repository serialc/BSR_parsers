# A few things we need to know generally
# - path to store raw and cleaned data, perhaps related to bssid
# - error log file
# - do we want to delete raw file

# And for each BSS 
# - url
# - second url - and whether it exists

import os

# let's retrieve the data feeds available for Chicago

# chicago
from motivate import motivate_llstatus as mot
fn = mot.scrape("http://www.divvybikes.com/stations/json", '.', 'error_log.txt')
if fn:
    mot.parse(fn, os.path.basename(fn).split('.')[0] + '_chicago.txt', 'error_log.txt', True)

# lyon
from jcdecaux import jcdecaux_llstatus as jcd
fn = jcd.scrape("http://www.divvybikes.com/stations/json", '.', 'error_log.txt')
if fn:
    mot.parse(fn, os.path.basename(fn).split('.')[0] + '_chicago.txt', 'error_log.txt', True)

