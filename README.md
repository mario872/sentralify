# sentralify
Scrape Sentral data and use it!

Sentralify was designed to be a replacement for [get-sentral](https://github.com/J-J-B-J/get-sentral) a ***fantastic*** package developed by J-J-B-J and SuperHarmony910.
Sentralify, can scrape data from the new Sentral frontend. So far, it can scrape:
 - Timetable
 - Awards
 - Attendance
 - Activites
 - Notices
 - Calendar
 - Classes

A quick sample to feed your coding addicted brain, so you can get started quickly:

```
from sentralify import sentralify

config = {"username": "your_username",
          "password": "your_password",
          "base_url": "base_url_here_eg_caringbahhs",
          "state": "your_state_here_eg_nsw",
          "headless": False}

data = sentralify(config)

# A LOT of data comes out of this sentralify function, get ready!
print(f"Timetable: {data['timetable']}")
print(f"Notices: {data['notices']}")
print(f"Calendar Events: {data['calendar']}")
print(f"Student Details (awards, attendance, classes etc): {data['student_details']}")
print(f"It took: {data['time_elapsed']} seconds to scrape that data from Sentral, and format it!")
```

This is rather impressive, and if you want to know more about how to use it, then you can visit the docs when they've been written.

Sentralify has plans to add lots more features, such as:
 - Incidents scraping
 - Downloading reports
 - Downloading attachments from notices and activities
 - Downloading files from the school resources page
 - Downloading school photo of yourself
 - Generating barcode for use in library (idea from get-sentral)

## Why does this not use get-sentral's license
I didn't use get-sentral's license, because although the idea for me to make this came from their archiving of get-sentral, I used no code from get-sentral, and implemented and researched all of the code myself. So, in my opinion this was made from the ground up, and I did not ['remix, transform, and build upon the material'](https://creativecommons.org/licenses/by-nc-sa/4.0/) provided by get-sentral.
