import csv, folium, os

import csv, folium, os

# Get the absolute path of the project root (Mr_Bin folder)
# This ensures it finds output.csv regardless of where you run the script from
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
CSV_PATH = os.path.join(PROJECT_ROOT, "output.csv")
SAVE_PATH = os.path.join(PROJECT_ROOT, "Dashboard/admin/public/Maps/locationMap.html")

with open(CSV_PATH, 'r') as locationFile: # Use the absolute path
    csv_reader = list(csv.reader(locationFile))

    if len(csv_reader) > 0:
        last_location = eval(csv_reader[-1][3]) 
        my_map = folium.Map(location=last_location, zoom_start=15)
        
        for row in csv_reader:
            location = eval(row[3])
            folium.Marker(location, popup="Detected Location").add_to(my_map)
        
        my_map.save(SAVE_PATH) # Save directly to dashboard folder
        print(f"Map saved to: {SAVE_PATH}")
    else:
        print("No location data found.")

    # Ensure there's data in the CSV
    if len(csv_reader) > 0:
        last_location = csv_reader[-1][3]  # Get the last recorded location (lat,lng)
        last_location = eval(last_location)  # Convert string to list
        
        # Create a map centered on the last recorded location
        my_map = folium.Map(location=last_location, zoom_start=15)
        
        # Add markers for all recorded locations
        for row in csv_reader:
            location = eval(row[3])  # Convert string to list
            folium.Marker(location, popup="Detected Location").add_to(my_map)
        
        # Save the map to an HTML file
        my_map.save("locationMap.html")
        print("Map has been saved as locationMap.html")
    else:
        print("No location data found in the CSV file.")