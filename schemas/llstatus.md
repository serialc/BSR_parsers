# Schema llstatus

## Description
Provides the location (lat, long), available/functional number of bikes, docks and station identifier (id)

### Array format
- Each element contains a sub array with [station id, latitude, longitude, # of available bikes, # of available docks]

### String or file format
The string and file have the following characteristics:
- First line has the headings: id  lat long    bikes   spaces
- Tab separated values

### File output name
- Parsed filenames take the form [bssid]_[UTC date time].txt. E.g., "boston_2015-10-31_13:26:52.txt"
- Raw downloaded files, if requested, are prefixed with 'raw_'. E.g., "raw_boston_2015-10-31_13:26:52.txt"

### Other
- Any station that is declared/determined to be out of service/down is omitted from results
- In the situation where a BSS does not use/have an id the field is left blank (while maintaining the tab spacing)
- Number of docks, spaces and free docks are not always available - but two always are, we use these to reconstitute the third if necessary
