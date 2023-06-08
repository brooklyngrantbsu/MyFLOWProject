# stdlib imports
import json


# third-party imports (may need installing)
import requests
import csv

# Creating csv file
myfile = open('BikeStations.csv', 'w', newline='')
csvwriter = csv.writer(myfile) # 2. create a csvwriter object
csvwriter.writerow(['ID','totalSlotNumber','City','Street','lon','lat']) ## 4. write the header
    


#Looping on every dock station (57 known)
for i in range(1,60): 
    # Formating URL
    addedstr=str(i)
    if i < 9:
        addedstr = '0'+addedstr
    url='https://portail-api-data.montpellier3m.fr/bikestation?id=urn%3Angsi-ld%3Astation%3A0'+addedstr+'&limit=1'
    # Sending request
    response = requests.get(url)

    # Translating byte response to Python data structures
    response_json = response.json()
    if len(response_json)>0:
        ## Print Raw Data
        #print(response_json)

        # Extracting data from Json
        data=[response_json[0]['id'].replace(":","%3"),
            response_json[0]['totalSlotNumber']['value'],
            response_json[0]['address']['value']['addressLocality'],
            response_json[0]['address']['value']['streetAddress'],
            response_json[0]['location']['value']['coordinates'][0],
            response_json[0]['location']['value']['coordinates'][1]
            ]
   
        # Print Extracted data
        print(data)

        # Wrinting Values in csv
        csvwriter.writerow(data) # 5. write the rest of the data

myfile.close()