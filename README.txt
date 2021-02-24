*********************************************************************************
**************************PERSON GENERATOR***************************************
*********************************************************************************

This program generates a pseduo-randomly selected list of addresses
based on the desired state and the number of addresses to generate.

It has a command line functionality as well as a graphical user interface.

*********************************************************************************
******************************IMPORTANT******************************************
*********************************************************************************
The addresses are taken from the files in the state_data folder, which are from Kaggle OpenAddresses US West.  These csv files have been altered to only contain the information pertenant to this assignment (lat/long/unit/hash,etc have been removed for the sake of filesize).  Replacing them WILL cause issues with functionality, so please keep this in the state in which it was submitted.
*********************************************************************************
*********************************************************************************

*********************************************************************************
******Update*********************************************************************
*********************************************************************************
Program now sends and recieves data from life-generator.py.
Files for this program need to be located in the directory of person-generator.py
in a folder called "life_gen".

If running from command prompt with input.csv, the program will look for a
toys.csv file in the person-generator.py directory that contains appropriate input for life-generator.py

Format is:
input_item_type, input_item_category, input_number_to_generate

input_item_type is always "toys"

Valid categories are:

"Arts & Crafts",
"Baby & Toddler Toys",
"Characters & Brands",
"Die-Cast & Toy Vehicles",
"Educational Toys",
"Electronic Toys",
"Figures & Playsets",
"Games",
"Jigsaws & Puzzles",
"Musical Toy Instruments",
"Novelty & Special Use",
"Pretend Play",
"Sports Toys & Outdoor"

If using the GUI, the user will have a new drop down with these options as well
as a new entry box for number to generate.  When this data is submitted, person-generator.py will create a toys.csv for use by life-generator.py.  

In both cases, life-generator.py will create it's own output.csv which will then be appended to person-generator.py's output.csv.

The results of life-generator.py will also display in the GUI.
**********************************************************************************
**********************************************************************************

This program can be executed in two different ways:

If used in a command prompt please enter the following from the directory the program resides in:

python person-generatory.py input.csv

This will read an "input.csv" file that is located within the same directory 
as the program and create an "output.csv" file full of addresses.  

The "input.csv" file needs to be in the following format (including header):

State,Gen Number
state name or abr, # of addresses to generate

examples (state names and abbreviations are NOT case sensitive):

State,Gen Number
california,200

or

State,Gen Number
ca,200

I have included a sample input and output csv file that were created using this method.

If the program is run without an input.csv, it will launch a Graphical User Interface with options to pick a state and a desired number of addresses to generate.

After the fields have been entered, click submit and a drop down will appear to preview the addresses.   Click Restart to relaunch the program or "Output CSV" to create an output.csv file of these addresses in the same directory as the program.



