import sys
sys.path.append("..")
sys.path.append(".")

from sentralify import Sentralify
import json


sentralify = Sentralify("james.glynn", "D0ct0rWh0812", "caringbahhs", "nsw", headless=False, persistent=True)

#sentralify.verify_login() # Check if the login credentials are valid, and print the result

#exit()

data = sentralify.sentralify(scrape_ics=True)
#print(data)
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)