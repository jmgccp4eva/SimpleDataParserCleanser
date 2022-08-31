# SimpleDataParserCleanser
Cleanses downloaded data set for future use

1. Downloads a data set of 3 files
2. Reads through akas file to locate only the U.S. titles
3. Reads through basics file to:
   1. Compare and make sure it is U.S. title
   2. Is not pornographic
   3. Is a movie
   4. Movie made 1980 or later.  Can easily change the year
4. Reads through the names file and removes all information except:
   1. Code
   2. Name
   3. Birth Year
   4. Death Year
5. Writes both movies and actors to .tsv files

NOTE: movies.tsv will be used in SimpleWebScraper
to determine the actors and their character names
for each movie.  As of August 2022 there was ~137K actors

NOTE: actors.tsv will be used in a future project
As of August 2022, there are 11M+ actors