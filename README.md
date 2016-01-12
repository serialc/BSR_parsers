# BSR_parsers
These parsing protocols allow the simple collection of data directly from Bicycle Sharing System (BSS) operator servers. In combination with the BSR API, downloading structured data is as simple as knowing the BSR id for the bicycle sharing system you desire data for.

## Conventions
Parsers simply need to be passed the bikeshare-research.org data feed item containing all the necessary information (except when operator site apikeys are required, then those need to be specified as well).

## Directory structure is as follows:
+ parsers (container of parsers)
  + Programming language of parser
    + Code to facilitate data retrieval
      + Name of parser modules protocols (e.g., motivate, paris, bob)
+ schemas (container of schema definitions)
  + Markdown files describing the schema (schema name in all lower case characters)

## A short discussion of BSS types
Not all BSS use stations as trip start/end points. Some systems allow free floating bicycles, which can be locked to any bicycle rack. The location is shared/specified by GPS or in some cases an SMS message by the user. These bikes typically need to still be kept within a zone called a FlexZone (nextbike) or service area (SOBI). Simply providing the number of bikes and spaces at a station is no longer sufficient. Individual bikes and locations need to be specified as well as station statuses. We're still working on what form this data should take.

## Python example
```python
# See parsers/demo.py
```
