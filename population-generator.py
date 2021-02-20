#Bryan DiStefano
#Population generator for US States using Census data API
import tkinter as tk
import requests
import csv
import sys
import os.path

#My key for the API
key = "10f867ce2c11e35ea4c43d1791b62f456ed2309c"

#Dataset of all the abbrieviated states for use in the GUI
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
#Datasaet of all the years for use in the GUI
years = ["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
#Dictionary of states abbrieviations and full names to swap between as needed
statesFullNames = {
    "AK": "Alaska",
    "AL": "Alabama",
    "AR": "Arkansas",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "IA": "Iowa",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "MA": "Massachusetts",
    "MD": "Maryland",
    "ME": "Maine",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MO": "Missouri",
    "MP": "Northern Mariana Islands",
    "MS": "Mississippi",
    "MT": "Montana",
    "NA": "National",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NE": "Nebraska",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NV": "Nevada",
    "NY": "New York",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VA": "Virginia",
    "VI": "Virgin Islands",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming"
}
#The FIPS of all states for use in the Census API
stateFips = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
    'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}

#Uses the Census API to find the population for the given year and state
#Also is sent the Full Name of the state, it then writes all the information to a
#csv file
def getPopulation(stateFips, year, stateName):
    baseUrl = "https://api.census.gov/data/"
    dataset = "/acs/acs1?get=NAME,"
    searchAndError = "B01003_001E"
    url = str(baseUrl + year + dataset + searchAndError + "&for=" + "state:" + stateFips + "&key=" + key)
    response = requests.get(url)
    data = response.json()
    dirpath = os.path.dirname(os.path.realpath(__file__))
    output_filepath = os.path.join(dirpath, "output.csv")
    with open(output_filepath, mode='w', newline='', encoding='utf-8') as outputFile:
        outputWriter = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        outputWriter.writerow(['input_year', 'input_state', 'output_population_size'])
        outputWriter.writerow([year, stateName, data[1][1]])
    return data[1][1]


#Shows the results in the GUI
def showResults(state, year, pop):
    tk.Label(window, text="Search Results:").grid(columnspan=2, row=4, column=0)
    tk.Label(window, text=state + "," + year + "," + pop).grid(columnspan=2, row=5, column=0)


#Defines the searchButton's behavior when clicked
def searchButtonBehavior():
    stateKey = stateFips.get(searchAbv.get())
    yearKey = searchYear.get()
    stateName = statesFullNames.get(searchAbv.get())
    showResults(stateName, yearKey, getPopulation(stateKey, yearKey, stateName))


#reads through the CSV input file and gets the year and state and then
#changes them to be used in getPopulation()
def parseCSV():
    with open(sys.argv[1]) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        rowcounter = 0
        for row in readCSV:
            if rowcounter == 0:
                rowcounter += 1
            inputYear = row[0]
            inputState = row[1]
            rowcounter += 1
        stateAbv = list(statesFullNames.keys())[list(statesFullNames.values()).index(inputState)]
        yearKey = inputYear
        stateKey = stateFips.get(stateAbv)
        getPopulation(stateKey, yearKey, inputState)



if __name__ == '__main__':
    #if there is a csv file input then it parses the file
    if len(sys.argv) > 1:
        parseCSV()
    else:
        #if not then the gui is created and used instead
        window = tk.Tk()
        window.geometry('500x500')
        window.title("Population Generator")

        searchAbv = tk.StringVar(window)
        searchAbv.set(states[0])

        searchYear = tk.StringVar(window)
        searchYear.set(years[0])

        tk.Label(window, text="Choose State:").grid(row=0, column=0)
        w = tk.OptionMenu(window, searchAbv, *states)
        w.grid(row=0, column=1)

        tk.Label(window, text="Choose Year:").grid(row=1, column=0)
        y = tk.OptionMenu(window, searchYear, *years)
        y.grid(row=1, column=1)

        searchButton = tk.Button(window, text="Search", command=searchButtonBehavior)
        searchButton.grid(columnspan=2, row=2, column=0)

        window.mainloop()