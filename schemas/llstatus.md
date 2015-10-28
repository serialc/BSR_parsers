# Schema llstatus

## Description
Provides the location (lat, long), available/functional number of bikes and docks identified by a provided id.

## Inputs
Here are the programming language independent parameters. Defaults should be the following, if programming language allows.

Function get():
  1. bsr_df - An object (depending on the language) containing the parsed JSON contents of a BSR request for a data feed
  2. output - The output of the function, can be either *file*, *array*, or *string*. *file* is the default.
  3. save_dir - The save location, if output is set to *file*.
  4. timeout_sec - How long do we wait to retrieve results? 20 is the default.
  5. apikey - Your personal API key required to retrieve this data feed (e.g., JCDecaux, Motivate APIs). The formatting may vary.
  6. save_raw - Do you want to save the intermediary results - the raw contents of the data feed? *True*, *False*
  7. save_raw_dir - The location to save the raw data feed.

Here are the parameter definitions in python:

`def get(bsr_df, output='file', save_dir='', timeout_sec=20, apikey='', save_raw=False, save_raw_dir='')`

## Outputs
- Can return an array, string or save output to a file
- Returns True (if not returning array or string) and successful, False otherwise.

#### Array
- Each element contains a sub array with [station id, latitude, longitude, # of available bikes, # of available docks]

#### String and file options
- The string and file options have the following characteristics
- First line has the headings: id  lat long    bikes   spaces
- Tab separated values

#### File output
- Parsed filenames take the form [bssid]_[UTC date time].txt

### Other
- Raw downloaded files, if requested, are named [bssid]\_raw\_[UTC date time].txt
- Any station that is declared/determined to be out of service/down is omitted from results
- In the situation where a BSS does not use id the field is left blank (while maintaining the tab spacing)
