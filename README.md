# BSR_parsers
Bicycle sharing system data feed parsing schemas and code

## Conventions
Scripts/code should have a callable function named 'parse' which takes the raw contents of the file data feed file, passed as a string, and returns a formatted string in the format defined by a schema. No file I/O is handled by this code.

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
+ schemas (definitions of schemas)
+ deprecated (similar to parsers but for schemas no longer)

## Deprecation
    In order to keep the structure somewhat clean, some schemas may be deprecated in time, these will be relocated to a similar tree structure as the *parsers* but named *deprecated*.
