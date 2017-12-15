# PythonUtils
A collection of useful python scripts for a variety of functions.

This is primarily as a place to store my useful scripts, but the scripts have a brief summary below and should be commented to the extent that they are self-documenting. If you have any questions about them just give me a shout,

Contributions are welcome

# Read ASDA Shopping #

This script will read a html file with the format of the ASDA shopping trolley summary, and output into an excel spreadsheet.
This script works as of August 2017, but obviously is dependent on the format of the webpage being compatible.
It does require the html file to be saved locally.

The script is commented sufficiently for use.

TODO: The script contains lots of hard coded things it would be nice if:
1. Provided with your ASDA credentials it would login and retrieve your trolley
2. Copes with products being out of stock
3. Writes to a variable excel file name
4. Log belongs to file not to class

# PDF Reader #

This script will read a pdf file and split out pages. This is specific to PDFs of a certain format, as an agenda for a meeting, with item numbers marked with 'Item'.
Uses pdfminer and pdfrw.

# ibuddy #

Contains the usbapi for the ibuddy, this only works for windows

# Expenditure Record #

TODO:
Add edit function.
Add option to open csv.
Add option to have user defined number of previous records (default 5)
When viewing all categories print nicely (not as a list but individually)
