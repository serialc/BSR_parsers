# Schema fullset

## Description
Provides the location (lat, long), total docks, available/functional number of bikes, docks/spaces, station identifier (id), name of station and whether the station is active/functional ('yes'/'no')

### Array format
- Each element contains a sub array with [station id, latitude, longitude, # of docks at station, # of available bikes, # of available docks, station name, active]

### String or file format
The string and file have the following characteristics:
- First line has the headings: id  lat long    docks    bikes   spaces   name   active
- Tab separated values

### File output name
- Parsed filenames take the form [bssid]_[UTC date time].txt. E.g., "boston_2015-10-31_13:26:52.txt"
- Raw downloaded files, if requested, are prefixed with 'raw_'. E.g., "raw_boston_2015-10-31_13:26:52.txt"

### Other
- In the situation where a BSS does not use/have an id the field is left blank (while maintaining the tab spacing)
- Number of docks, spaces and free docks are not always available - but two always are, we use these to reconstitute the third.
