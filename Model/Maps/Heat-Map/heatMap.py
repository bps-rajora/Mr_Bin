import csv, folium, os
from folium.plugins import HeatMap

import csv, folium, os
from folium.plugins import HeatMap

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
CSV_PATH = os.path.join(PROJECT_ROOT, "output.csv")
SAVE_PATH = os.path.join(PROJECT_ROOT, "Dashboard/admin/public/Maps/heatMap.html")

with open(CSV_PATH, 'r') as locationFile: # Use the absolute path
    csv_reader = list(csv.reader(locationFile))

    if len(csv_reader) > 0:
        last_location = eval(csv_reader[-1][3])
        my_map = folium.Map(location=last_location, zoom_start=15)
        
        heatData = [eval(row[3]) for row in csv_reader]
        HeatMap(heatData).add_to(my_map)
        
        my_map.save(SAVE_PATH) # Save directly to dashboard folder
        print(f"Heat Map saved to: {SAVE_PATH}")
    else:
        print("No location data found.")
    # Ensure there's data in the CSV
    if len(csv_reader) > 0:
        last_location = eval(csv_reader[-1][3])  # Get the last recorded location (lat,lng)
        
        # Create a map centered on the last recorded location
        my_map = folium.Map(location=last_location, zoom_start=15)
        
        heatData = [eval(row[3]) for row in csv_reader]
        HeatMap(heatData).add_to(my_map)
        
        # Save the map to an HTML file
        my_map.save("heatMap.html")
        print("Map has been saved as heatMap.html")
    else:
        print("No location data found in the CSV file.")