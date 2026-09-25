# Sentralify
Scrape Sentral data and use it!

## Version 2.0

Version 2.0 introduces the `Sentralify` client class. The former
`sentralify(config, ...)` function and configuration dictionary are no longer
part of the public API.

Sentralify was designed to be an **unofficial** replacement for [get-sentral](https://github.com/ryftjet/get-sentral) a ***fantastic*** library developed by ryftjet and SuperHarmony910.

Sentralify can scrape data from the new Sentral frontend. So far it can scrape:
 - Timetable
 - ICS Timetable
 - Awards
 - Attendance
 - Activities
 - Notices
 - Calendar
 - Classes
 - Student Details such as name, student id etc.

Example code:
```python
from sentralify import Sentralify
import json

sentralify = Sentralify(
    username="your.username",
    password="your_password",
    prefix="caringbahhs",
    state="nsw",
    headless=False,
    persistent=True,
)

# Check credentials without scraping data.
# print(sentrallify.verify_login())

data = sentralify.sentralify(scrape_ics=True)

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

# A LOT of data comes out of this sentralify function
print(f"Timetable: {data['timetable']}")
print(f"Notices: {data['notices']}")
print(f"Calendar Events: {data['calendar']}")
print(f"Student Details (awards, attendance, classes etc): {data['student_details']}")
print(f"It took: {data['time_elapsed']} seconds to scrape that data from Sentral, and format it!")
```

Sentralify has plans to add lots more features, such as:
 - Incidents scraping
 - Downloading reports
 - Downloading attachments from notices and activities
 - Downloading files from the school resources page

## Documentation
To use Sentralify, first instantiate the class with the user's details, then scrape the data.

### Create a client

Create one `Sentralify` instance for a student's Sentral account:

```python
sentralify = Sentralify(
    username="your.username",
    password="your_password",
    prefix="caringbahhs",
    state="nsw",
    headless=True,
    persistent=False,
    persistent_dir="sentralify_data",
)
```

`prefix` is the portion before `.sentral.com.au` in the school's address, and
`state` is the state's abbreviation (for example, `nsw`). `headless` controls
whether Playwright shows a browser window. Set `persistent=True` to reuse a
browser profile at `persistent_dir`; this can avoid signing in on later runs.

### `Sentralify.sentralify()`

Call `sentralify.sentralify()` to scrape data. `scrape_timetable`,
`scrape_notices`, and `scrape_calendar` default to `True`; set any to `False`
to omit that collection. Set `scrape_ics=True` to include the timetable's ICS
text in `data["ics"]`. `timeout` is in milliseconds and defaults to `5000`.

Use `sentralify.verify_login(timeout=5000)` when only credential validation is
needed. It returns `True` or `False`.

### Return data

`sentralify.sentralify()` returns a dictionary containing the requested collections,
student details, and `time_elapsed`.

##### Timetable
The timetable that sentralify returns can be accessed by using `sentralify(config)['timetable']`
Below is the general structure of one day, in one week that timetable returns:
```python
[
    {
        "periods": [
            {
                "is_now": False,
                "start": "7:30",
                "end": "8:50",
                "start_time_date": "Fri Apr  5 07:30:00 2024",
                "end_time_date": "Fri Apr  5 08:50:00 2024",
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
            },
            {
                "is_now": False,
                "start": "8:50",
                "end": "10:08",
                "start_time_date": "Fri Apr  5 08:50:00 2024",
                "end_time_date": "Fri Apr  5 10:08:00 2024",
                "full_name": "Art Yr8",
                "name": "8ART8",
                "room": "DF.09",
                "border_colour": "FF7FFF",
                "background_colour": "FFDFFF",
                "teacher": "Miss T. Glennan",
            },
            {
                "is_now": True,
                "start": "10:08",
                "end": "10:28",
                "start_time_date": "Fri Apr  5 10:08:00 2024",
                "end_time_date": "Fri Apr  5 10:28:00 2024",
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
            },
            {
                "is_now": False,
                "start": "10:28",
                "end": "11:45",
                "start_time_date": "Fri Apr  5 10:28:00 2024",
                "end_time_date": "Fri Apr  5 11:45:00 2024",
                "full_name": "PDHPE Yr8",
                "name": "8PDHY",
                "room": "COLA1",
                "border_colour": "85EE88",
                "background_colour": "E0FAE1",
                "teacher": "Mr P. Littlejohn",
            },
            {
                "is_now": False,
                "start": "11:45",
                "end": "11:50",
                "start_time_date": "Fri Apr  5 11:45:00 2024",
                "end_time_date": "Fri Apr  5 11:50:00 2024",
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
            },
            {
                "is_now": False,
                "start": "11:55",
                "end": "13:08",
                "start_time_date": "Fri Apr  5 11:55:00 2024",
                "end_time_date": "Fri Apr  5 13:08:00 2024",
                "full_name": "LAN Yr8",
                "name": "8LAY",
                "room": "GF.16",
                "border_colour": "FFBF7F",
                "background_colour": "FFEFDF",
                "teacher": "Mr A. Gollan",
            },
            {
                "is_now": False,
                "start": "13:08",
                "end": "13:28",
                "start_time_date": "Fri Apr  5 13:08:00 2024",
                "end_time_date": "Fri Apr  5 13:28:00 2024",
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
            },
            {
                "is_now": False,
                "start": "13:28",
                "end": "13:48",
                "start_time_date": "Fri Apr  5 13:28:00 2024",
                "end_time_date": "Fri Apr  5 13:48:00 2024",
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
            },
            {
                "is_now": False,
                "start": "13:48",
                "end": "15:05",
                "start_time_date": "Fri Apr  5 13:48:00 2024",
                "end_time_date": "Fri Apr  5 15:05:00 2024",
                "full_name": "Science Yr8",
                "name": "8SCIY",
                "room": "DG.04",
                "border_colour": "84E6DD",
                "background_colour": "E0F8F6",
                "teacher": "Mr A. Vamvakaris",
            },
            {
                "is_now": False,
                "start": "15:05",
                "end": "16:25",
                "start_time_date": "Fri Apr  5 15:05:00 2024",
                "end_time_date": "Fri Apr  5 16:25:00 2024",
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
            },
            {
                "is_now": False,
                "start": "15:05",
                "end": "15:15",
                "start_time_date": "Fri Apr  5 15:05:00 2024",
                "end_time_date": "Fri Apr  5 15:15:00 2024",
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
            },
        ],
        "date": "Fri Apr  5 00:00:00 2024",
        "is_today": False,
    }
]

```
The timetable is a list of ten school-day dictionaries (two weeks). Each day contains its date and a list of periods. The `"is_today"` key indicates whether Sentral identifies that day as today. To access Period 1's room, use `data['timetable'][0]['periods'][1]['room']`.

#### Notices
The notices returned by Sentralify are available at `data['notices']`.
Below is an example of one notice that it returns:
```python
[
    {
        'title': 'Volleyball Team Trials',
        'date': "Mon Feb 12 00:00:00 2024",
        'author': 'Mr. Smith',
        'content': 'Any students interested in trialing for the Open Boys or the Open Girls Volleyball Teams, can you please register your name outside the B Block staffroom.\xa0  \n  \nThe Open Boys Trial will be held Monday 19/2/24, prior to school starting at 7:15 am. Doors will be closed at 7:30 so please be prompt.  \n  \nThe Open Girls will be held Monday 19/2/24, after school until 4:30 pm.\xa0  \n  \nIf you are interested but cannot attend the trial sessions please indicate on the sign on sheet.  \n  \nThere will also be beginner/development squads running in the near future. If you are interested please sign on the beginner squad register.\n\n'
    }
]
```
Sentralify returns notices as dictionaries containing the title, date, author, and content. Content uses Markdown to retain teacher formatting. For example, access the first notice's author with `data['notices'][0]['author']`.

#### Calendar
The school-calendar events are available at `data['calendar']`.
Below is an example of one events that it returns:
```python
[
    {
        "title": "Events: All Day - Duke of Ed Qualifying AJ - Camp Coutts (McCann)",
        "start": None,
        "end": None,
        "date": "Wed Apr 10 00:00:00 2024",
    }
]
```

Sentralify returns calendar events as dictionaries containing title, start, end, and date. Access the first event's date with `data['calendar'][0]['date']`. All-day events have `None` for start and end.

#### Student Details
Okay, this one is not as structured as the others, because it's a big collection of other details about the student, so I'm just gonna copy-past my one over, and censor my personal details.
```python
{
    "student_id": 1234,
    "first_name": "John",
    "surname": "Smith",
    "name": "John Smith",
    "school_year": 12,
    "rollclass": {"name": "12R1", "teacher": ""},
    "classes": [
        {"name": "12ART13", "subject": None, "teacher": "Mr. Smith"},
        {"name": "12TEC13I", "subject": None, "teacher": "Mr. Doe"},
        {"name": "12MUSY", "subject": None, "teacher": "Mrs. J Doe"},
        {"name": "12ENGY", "subject": None, "teacher": None},
        {"name": "12GEOY", "subject": None, "teacher": "Mr. M Man"},
        {"name": "12LAY", "subject": None, "teacher": None},
        {"name": "12MATG", "subject": None, "teacher": "Mr. PARR"},
        {"name": "12GIFTY", "subject": None, "teacher": "Ms. E Staples"},
        {"name": "12PDHY", "subject": None, "teacher": None},
        {"name": "12SCIY", "subject": None, "teacher": "Mr. A Go"},
        {"name": "Bowling01", "subject": None, "teacher": None},
    ],
    "attendance": None, # See the snippet after this explainer
    "attendance_percent": [97, 0, 0, 0],
    "activities": [
        {
            "name": "Year 13 Art Gallery NSW",
            "start_date": datetime.datetime(2024, 6, 17, 0, 0),
            "end_date": datetime.datetime(2024, 6, 17, 0, 0),
            "start_time": datetime.datetime(2024, 6, 17, 10, 8),
            "end_time": datetime.datetime(2024, 6, 17, 15, 5),
            "points": None,
            "description": "In alignment with Year 13's Metaphorical Self Portrait assessment, students will attend the Art Gallery of New South Wales North and South buildings to identify and learn about works of art that will then be used as inspiration for their Skateboard Deck painting. In class, students will have explored the 'ism' art movements (impressionism, post-modernism, cubism, pop-art and surrealism). This excursion offers students the opportunity to engage with some of these artworks and appreciate their scale and grandeur up close and personal.",
            "category": "Excursion / Incursion Request",
        }
    ],
    "awards": [
                {
                    'year': '2024',
                    1: '1',
                    2: '1',
                    3: '0',
                    4: '0',
                    'total': '2'
                },
                {
                    'year': '2023',
                    1: '2',
                    2: '8',
                    3: '1',
                    4: '3',
                    'total': '14'
                },
                {
                    'year': '2022',
                    1: '0',
                    2: '0',
                    3: '0',
                    4: '0',
                    'total': '0'
                }
               ]
}

```
This is a lot of data, but having it nicely formatted and laid out here should make it easier to understand. To access the third class's teacher, use `data['student_details']['classes'][2]['teacher']`.

#### Attendance
The attendance (added in v1.2.0) is really long, below is a small snippet of one day of data.
```python
[
    [
        [
            {
                "date": "Mon Jan 29 00:00:00 2024",
                "status": "holiday",
                "description": "Public Holiday",
            }
        ]
    ]
]
```
To get the attendance status on the first day of the school year, call `data['student_details']['attendance'][0][0][0]['status']`. The three indexes are the term, week number in that term, and day of the week.

#### ICS Timetable
If you, for example, wanted to import your timetable into your calendar, then you would export your timetable as an ICS file, and import it into, say, Google Calendar.
This is how you can, for whatever reason, access your timetable in an ICS format using Sentralify.
To parse the ICS data in python, you can use the [ics PyPi library](https://pypi.org/project/ics/).
Call `sentralify.sentralify(scrape_ics=True)` and access the ICS data with `data['ics']`.
