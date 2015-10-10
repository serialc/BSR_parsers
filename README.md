# BSR_parsers
Bicycle sharing system data feed parsing schemas and code

## Conventions
Scripts/code should have a callable function named 'parse' which takes the raw contents of the file data feed file, passed as a string, and returns a formatted string in the format defined by a schema. No file I/O is handled by this code.

Directory structure is as follows:
+ Schemas
  + Schema names (Defining what data in what structure is desired, see specific README.md)
    + Name of parsing pattern (e.g., Motivate, Paris, Bob) (max 32 characters)
      + Files, named identically to the above directory with the extension indicating languages (e.g., Motivate.py, Motivate.pl)
