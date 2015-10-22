# llstatus

## Description
Provides the location (lat, long), available/functional number of bikes and docks identified by a provided id.

## Details
- First line has the headings: id  lat long    bikes   spaces
- Parsed filenames take the form [bssid]_[UTC date time].txt
- Raw downloaded files, if requested, are named [bssid]_raw_[UTC date time].txt
- Tab separated values
- Any station that is declared/determined to be out of service/down is omitted from results
- In the situation where a BSS does not use id the field is left blank (while maintaining the tab spacing)
