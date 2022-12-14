# -*- coding: utf-8 -*-
"""Homework 2_Bhagyashri Patil
### MIS-515 Homework 2: Earthquake Data
"""

"""
* MIS-515 : Assignment 2
* Problem Statement: Use a combination of two APIs to collect and store realtime earthquake data.
(1) The United States Geological Survey (USGS) maintains a public JSON API with information on all earthquakes affecting the United States in 
the past hour, located at “https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson”.
(2) Use a second API to obtain more information about the location of each earthquake. The OpenCage API provides a free service the converts 
from latitude and longitude coordinates to county and state. After completing the OpenCage signup, you can obtain geographic data about each 
earthquake location using “https://api.opencagedata.com/geocode/v1/xml?q=lat+long&key=yourkey”.
Replace lat in the URL with the latitude of your earthquake; replace long in the URL with the longitude of your earthquake; and replace 
yourkey in the URL with your API key. The API will return results in XML format. For each earthquake, show a printout that reflects the 
complete information you have obtained.
-> Magnitude 0.51 earthquake on September 20, 2021 at 06:33:18 AM and located at (33.6101667, -116.7991667) in Riverside County, California.
Occasionally, an earthquake will not correspond to a location in the United States because it occurred in the Ocean off the coast of the 
United States. In these cases, the OpenCage API will not return a “county” or “state” field. Handle the potential error in your code 
(try-except is a good strategy) and instead show an appropriate printout; for example:
-> Magnitude 5.1 earthquake on September 20, 2021 at 06:12:03 AM and located at (-36.7685, -74.004) in the Ocean.
Finally, output the data for each earthquake to a CSV file named “earthquakes.csv”. The CSV file should have columns for time, magnitude, 
latitude, longitude, county, and state. Ensure that your program overwrites the output CSV file each time that it runs. 
"""

# Homework - 2: Solution
# Code Indent used : 4

# Importing the required libraries and installations
!pip install xmltodict
import xmltodict, json, requests, csv, datetime

# Over-writing the output to the csv file, every time the code gets executed
with open('earthquakes.csv','w') as file:
    writer = csv.writer(file, lineterminator = '\n')

    # Writing a header row to the csv file
    header = ['Time', 'Magnitude', 'Latitude', 'Longitude', 'County', 'State']
    writer.writerow(header)

    # Welcome message to user
    print("\n*** Welcome to the real-time Earthquake API Data! ***")

    # 1st API : JSON data
    # URL link and API Key
    earthquake_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"

    # Generated my API key by signing in to OpenCage website
    api_key = "1f734045b3db4b30b9e3ef1ec31d1665"

    earthquake_response = requests.get(earthquake_url)

    # JSON Connection Successful (Status code 200)
    if earthquake_response:

        # JSON parser
        earthquake_data = json.loads(earthquake_response.text)

        # Fetching total no. of earthquakes happened by using 'count' field
        total_count = earthquake_data["metadata"]["count"]
        print("\nTotal Earthquakes affecting the US in the past hour:", total_count, "\n")

        # Drill down to the 'magnitude', 'longitude' and 'latitude' and 'time' fields
        metrics = earthquake_data["features"]        

        # Loop through metrics one-by-one, for getting all metrics values
        for line in metrics:
            magnitude = line["properties"]["mag"]
            longitude = line["geometry"]["coordinates"][0]
            latitude = line["geometry"]["coordinates"][1]
            
            # Time is in Unix epoch time format
            orig_time = line["properties"]["time"]

            # Convert milliseconds to seconds
            orig_time_sec = orig_time / 1000

            # Convert Unix epoch time to datetime object
            datetime_timestamp = datetime.datetime.utcfromtimestamp(orig_time_sec)

            # Subtract 7 hours to adjust for time zone difference (UTC time zone to PDT time zone)
            datetime_adj_timestamp = datetime_timestamp - datetime.timedelta(hours = 7)

            # Convert to human-interpretable string
            # String would say: “September 01, 2022 at 12:00:00 AM”
            time_str = datetime_adj_timestamp.strftime("%B %d, %Y at %I:%M:%S %p")

            
            # 2nd API : XML data
            # Generating XML URL for fetching location details associated with latitude and longitude of each earthquake
            location_url = "https://api.opencagedata.com/geocode/v1/xml?q=" + str(latitude) + "+" + str(longitude) + "&key=" + api_key
            
            location_response = requests.get(location_url)

            # XML Connection Successful (Status code 200)
            if location_response:

                # If County/State details available
                try:

                    # XML Parser
                    location_data = xmltodict.parse(location_response.text)

                    # Drill down to the 'county' and 'state' fields
                    county = location_data["response"]["results"]["result"]["components"]["county"]
                    state = location_data["response"]["results"]["result"]["components"]["state"]

                    # Printing complete information as output
                    print(f"Magnitude {magnitude} earthquake on {time_str} and located at\n ({latitude} , {longitude}) in {county}, {state}.\n")

                    # CSV Result: All variables have respective data. 
                    # Write every earthquake's details as data rows in the csv file
                    row = [time_str, magnitude, latitude, longitude, county, state]
                    writer.writerow(row)

                
                # Exception: Potential Error Handling - County/State details NOT available for associated Latitude/Longitude.
                except Exception as e:

                    if county or state:
                        # For adding 'county' = 'state' = 'N/A' values in CSV file
                        county = "N/A"
                        state = "N/A"
                        print(f"Magnitude {magnitude} earthquake on {time_str} and located at\n ({latitude} , {longitude}) in the Ocean.\n")

                        # CSV Result: Either of 'county' or 'state' variable does NOT have required data.
                        # Thus, assign 'county' = 'state' = N/A
                        
                        # This will execute ONLY IF county OR state values are not available.
                        row = [time_str, magnitude, latitude, longitude, county, state]
                        writer.writerow(row)

                    else:
                        print('Sorry, an unexpected error occured.')

            # XML Connection Error (Status code other than 200)
            else:
                print("Sorry, XML API connection error.")


    # JSON Connection Error (Status code other than 200)
    else:
        print("Sorry, JSON API connection error.")


# Exit message to user
print("\n*** Thank you for using Earthquake Data APIs ***")
