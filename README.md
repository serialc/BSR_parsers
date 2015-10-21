# BSR_parsers
Bicycle sharing system data feed parsing schemas and code

## Conventions
There exist two main types of BSS data feeds:
+ Those that provide the location and status attributes in one file, (e.g., [https://www.thehubway.com/data/stations/bikeStations.xml](Boston)) and 
+ Those that provide the station location and name, and in individual files, requiring individual requests, the status of each station. (e.g., [http://www.citycycle.com.au/service/carto](Brisbane) [http://www.citycycle.com.au/service/stationdetails/brisbane/1](station 1))

Parsers, given the URL of the primary, and if needed, secondary URLs should retrieve the files and store them an absolute path provided, then parse these to create a file, again located in another path provided, containing the data defined in the schema. Output file names are standardized by the schema as well.


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

## Deprecation
    In order to keep the structure somewhat clean, some schemas may be deprecated in time, these will be relocated to a similar tree structure as the *parsers* but named *deprecated*.
