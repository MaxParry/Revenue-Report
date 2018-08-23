# Revenue Report
A simple python script to ingest monthly revenue CSVs with different formats, parse contents, and yield a combined revenue summary.

## Problem
In order to generate a financial analysis of a company, it is often necessary to compile reports from different departments. These departments often have different reporting standards, so there is a need to parse the information from each department in order to facilitate analysis.

## Data Structure
The two .csv files in the input_data folder both have just two columns:
* `date`
* `revenue`

In one .csv file, date is in the Mmm-yy format. In the other, date is in the Mmm-yyyy format.

## Project Goals
The goal of this analysis is to take monthly revenue files and provide a summary financial analysis. The two problems that need to be solved are:
* Overlap between some, but not all months between the two reports
* Different date formats between the two reports

The final financial analysis will consist of:
* Total number of months covered by the combined reports
* Total revenue in all months
* Average revenue change, month-to-month
* Greatest monthly increase in revenue, including the month and year
* Greatest monthly decrease in revenue, including the month and year

This information will be written to a .txt file.

## Scripting
### .csv Ingestion
#### User Input
In order to allow the script to compile an unlimited amount of reports, the user is asked to enter the number of files to be analyzed, using the `input` function. The resulting integer is stored for later iteration.

The user is then asked to enter the filepath of each source file to be included in the analysis. These filepaths are then appended to an empty list, `directories`. These are later used to successively read .csv contents.

#### Filepath Parsing and Reconstruction
After the number and location of input files is stored, the loop on lines 47 to 63 iterates through each filepath entered by the user, parsing the directory tree and reconstructing a proper filepath based on the operating system used by the user. This is done to ensure that the script works on both Windows and Linux machines, which have different directory seperators.

### Reading, Parsing, and Storing .csv Contents.
#### Extracting File Contents
Using `csv.reader()`, the reconstructed filepath is used to open the .csv file, and iterate through each line in the .csv.

While iterating through rows, the data in the first column, date, is read. If the data is either `date` or `Date`, the row is a header, and is skipped.

In all other cases, the date is split on the delimiter `-`, and components added to a list, `parselist`. The last (2nd) element of that list will be the year portion of the date, in either yy or yyyy format.

#### Year Lookup
The yy or yyyy year is used to lookup the year in a dictionary, `datedict`, which will return the corresponding yyyy format year.

#### Month and Revenue
The Mmm format month is the first element of `parselist`, and is retrieved and stored as `month`.

Revenue is read as the second element of the row being iterated over, and is stored as `revenue`.

#### Storing Transformed Data
The yyyy format `year`, Mmm format `month`, and integer-cast `revenue` are packaged into a list on line 62. That list is then appended to the list `array` for storage.

The loop will iterate through each row, finishing with a list of lists, each inner list representing one transformed row of the original .csv.

### Summating Revenue
 For many months, there is revenue coming from two departments, which will need to be added together. Now that the data has been ingested, parsed, and has a consistent format, it needs to be combined. In order to solve this problem, I decided to:
* Sort the data chronologically, then
* Sum the revenues of any year/month pairs that are the same
* Store a new, combined list with one revenue for each month

Because the data from each .csv has been read and stored in `array` line-by-line, it is not currently sorted chronologically.

#### Encoding Year and Month as Ordinal Integers
To give ordinality to both years and months for sorting, lines 65 through 89 contain two dictionaries. These contain either a year or month key, and a value corresponding to the year or month's chronological ordinality.

Lines 91-93 use a for loop to iterate through each element in `array` (again, each element can be thought of as a row of parsed data from the original .csv). The month and year strings are retrieved from the row, and used as keys to look up the corresponding ordinal value in the corresponding dictionary (`yeardict` or `monthdict`). The original month and year strings are then replaced by this ordinal in `array`.

#### Sorting Data
The `sorted()` function is then used to return the sorted array. The `operator` module's function `itemgetter()` is used to sort on the 0th element (year), then 1st element (month) of each list (row) in `array`.

#### Decoding
Lines 97-103 decode the ordinal values back into year and month strings by reverse-lookup in the corresponding dictionary (either `yeardict` or `monthdict`). The string is then stored in place of the ordinal. This is accomplished in the following way:
* For each element (row) in `array`:
    * Ordinal-encoded year (0th element of inner list) is compared to each value in dictionary. If a match is found, the key is extracted from the dictionary and is used to overwrite the ordinal integer.
    * Ordinal-encoded month (1st element of inner list) is compared to each value in dictionary. If a match is found, the key is extracted from the dictionary and is used to overwrite the ordinal integer.

#### Aggregating Revenue
Now that the data has been sorted, months for which there are two (or more) datapoints need to be added together.

To accomplish this, `array` is iterated over again using a for loop. During iteration, each element is subject to the following tests:
* Is the year different from the stored `thatyear` OR is the month different from the stored `thatmonth`? 
    * Initially `thatyear` and `thatmonth` are empty strings, so this will be true during the first pass through the loop
    * If true, that element is appended to `finalarray`
* If the above is false, is the year identical to `thatyear` AND the month identical to `thatmonth`?
    * If true, we have arrived on a year/month pair that is identical to the previous year/month pair
        * In this case, the revenue (2nd element in list) is added to the stored `thatrev` and the result used to overwrite the original read revenue.
            * Subsequently, the current row overwrites the last row in `finalarray`, as it has the most updated revenue.

Following these tests, the current row's year, month, and revenue are stored as `thatyear`, `thatmonth`, and `thatrev`, respectively, to serve as the comparitors for the next pass through the loop.

Overall, this loop serves to check if the current row is unique (in which case it is added to `finalarray`), or from the same time period as the previous row (in which case its revenue is added to the previous row's revenue and used to overwrite the previous row). Said simply, it adds together duplicate year/month pairs.

### Financial Analysis
Now that the data has been cleaned, the analysis can be produced.

#### 