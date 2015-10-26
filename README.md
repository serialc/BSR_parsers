# BSR_parsers
Bicycle sharing system data feed parsing schemas and code

## Conventions
Parsers simply need to be passed the bikeshare-research.org data feed item containing all the necessary information - except for apikeys.

Additional attributes such as the directory to store formatted data, saving of raw data can be specified.

## Directory structure is as follows:
+ parsers (container of parsers)
  + Name of parser (e.g., motivate, paris, bob) (max 32 characters)
    + Files, named according to the following and in this order:
      1. Name of parser (identically to the directory)
      2. '_'
      3. Schema (identical to a schema in the schemas directory)
      4. '.'
      5. File extension, dictating programming language
    + Example: motivate\_llstatus.py
+ schemas (container of schema definitions)
  + Markdown files describing the schema (schema name in all lower case characters)

## Feed types
There exist two main types of BSS data feeds but it isn't necessary to know about these as the code handles the retrieval independently:
+ Those that provide the location and status attributes in one file, (e.g., [https://www.thehubway.com/data/stations/bikeStations.xml](Boston)) and 
+ Those that provide the station location and name, and in individual files, requiring individual requests, the status of each station. (e.g., [http://www.citycycle.com.au/service/carto](Brisbane) [http://www.citycycle.com.au/service/stationdetails/brisbane/1](station 1))

## To do
* [ ] Create handlers to further simplify retrieval
