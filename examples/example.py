import sys            # For local development
sys.path.append("..") # For local development
sys.path.append(".")  # For local development

from sentralify import Sentralify
import json


sentralify = Sentralify("james.glynn", "poop", "caringbahhs", "nsw", headless=False, persistent=True)

# print(sentralify.verify_login()) # Check if the login credentials are valid, and print the result

data = sentralify.sentralify(scrape_ics=True)

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
    
print(f"Timetable: {data['timetable']}")
print(f"Notices: {data['notices']}")
print(f"Calendar Events: {data['calendar']}")
print(f"Student Details (awards, attendance, classes etc): {data['student_details']}")
print(f"It took: {data['time_elapsed']} seconds to scrape that data from Sentral, and format it!")