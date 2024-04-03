# sentralify
Scrape Sentral data and use it!

Sentralify was designed to be an **unofficial** replacement for [get-sentral](https://github.com/J-J-B-J/get-sentral) a ***fantastic*** package developed by J-J-B-J and SuperHarmony910.
Sentralify can scrape data from the new Sentral frontend. So far it can scrape:
 - Timetable
 - Awards
 - Attendance
 - Activites
 - Notices
 - Calendar
 - Classes
 - Student Details such as name, student id etc.

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

This is rather impressive, and if you want to know more about how to use it, then you can have a look at the documentation below.

Sentralify has plans to add lots more features, such as:
 - Incidents scraping
 - Downloading reports
 - Downloading attachments from notices and activities
 - Downloading files from the school resources page
 - Generating barcode for use in library (idea from get-sentral)

## Documentation
sentralify is quite simple from the user's perspective, all you have to do is call ```sentralify(config)```, and it will magically scrape sentral for you and give you all the data you could ever want.
If you want to understand in more detail how this works, then read on!

### sentralify()
```sentralify()``` needs only 1 argument but accepts a total of 6. These arguments are ```config, timetable, notices, calendar, persistent, check_login```; the last 5 are optional, and will all be ```True``` if not disabled, except for ```check_login``` which will be ```False```. ```config``` is required, and accepts a python dictioary formatted as follows:

```
config = {"username": "your_username",
          "password": "your_password",
          "base_url": "base_url_here_eg_caringbahhs",
          "state": "your_state_here_eg_nsw",
          "headless": False}
```

```headless``` in the config, will dictate, whether a chromium window opens, or whether it does it all invisibly. ```timetable, notices, calendar``` are all pretty self-explanatory, if you enable them, then sentralify, will scrape the selected web pages, and format their output. ```persistent``` makes sentralify open Sentral in a normal chromium window (as opposed to an incognito window), this makes it a lot faster after the first sign in, as Sentral can just use the cookies saved to the contexts folder, and not require you to sign in again. On average, incognito mode takes around 20 seconds each time, and (after the first login), persistent takes around 3-10 seconds.

```check_login``` added in v1.1.0 is used to check the user's login, ie. check if they spelled their password and email correctly, if used, it will return a value of ```True``` or ```False```.

### sentralify() return data
sentralify returns a lot of data! Below is a documentation of what it returns

##### Timetable
The timetable that sentralify returns can be accessed by using ```sentralify(config)['timetable']```
Below is the general structure of one day, in one week that timetable returns:
```
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
Yes, that is actually my timetable for one day, no I am not in year 13, no I am not telling you what year I am in.
The general gist of how sentralify returns your timetable is 14 dictionaries in a list, each containing the date, and another list of 11 periods, with various values shown above. In each day, it also incudes the ```"is_today"``` key, which indicated whether the data was pulled from the cyclical timetable (False), or the daily timetable (True). If you wanted to access Period 1's room for example, you would run ```sentralify(config)['timetable'][0]['periods'][1]['room']```

#### Notices
The notices that sentralify returns can be accessed by using ```sentralify(config)['notices']```
Below is an example of one notice that it returns:
```
[
    {
        'title': 'Volleyball Team Trials',
        'date': "Mon Feb 12 00:00:00 2024",
        'author': 'teacher_name',
        'content': 'Any students interested in trialing for the Open Boys or the Open Girls Volleyball Teams, can you please register your name outside the B Block staffroom.\xa0  \n  \nThe Open Boys Trial will be held Monday 19/2/24, prior to school starting at 7:15 am. Doors will be closed at 7:30 so please be prompt.  \n  \nThe Open Girls will be held Monday 19/2/24, after school until 4:30 pm.\xa0  \n  \nIf you are interested but cannot attend the trial sessions please indicate on the sign on sheet.  \n  \nThere will also be beginner/development squads running in the near future. If you are interested please sign on the beginner squad register.\n\n'
    }
]
```
Yes, if you're the teacher that posted this who is reading this, then I can take it down if you want me to, no I will not bother asking for verification if it is really you, yes I will just make up a notice about school ending 5 weeks before the summer holidays, and this is definitely official.
The general gist of how sentralify returns your notices is multiple dictionaries in a list, each containing the title, date, author, and content. The content is in markdown formatting, to retain the formatting that is added by teachers on Sentral. If you wanted to access the first notice's author, then you would run ```sentralify(config)['notices'][0]['author']```

#### Calendar
The events from the school calendar that sentralify returns can be accessed by using ```sentralify(config)['calendar']```
Below is an example of one events that it returns:
```
[
    {
        "title": "Events: All Day - Duke of Ed Qualifying AJ - Camp Coutts (McCann)",
        "start": None,
        "end": None,
        "date": "Wed Apr 10 00:00:00 2024",
    }
]
```

Yes, I'm tired of writing this dcoumentation, no I will not stop prematurely.
The general gist of how sentralify returns your celendar is multiple dictionaries in a list, each containing the title, start, end, and date. If you wanted to access the first events's date, then you would run ```sentralify(config)['calendar'][0]['date']```. Please note that not all events have the start and end fields filled out, as sometimes events just run all day instead.

#### Student Details
Okay, this one is not as structured as the others, because it's a big collection of other details about the student, so I'm just gonna copy-past my one over, and censor my personal details.
```
{
    "student_id": not_telling_you_bt_its_an_int,
    "first_name": "mario872",
    "surname": "I_have_no_surname",
    "name": "mario872 I_have_no_surname",
    "school_year": 13,
    "rollclass": {"name": "13R1", "teacher": ""},
    "classes": [
        {"name": "13ART13", "subject": None, "teacher": "not_telling_you"},
        {"name": "13TEC13I", "subject": None, "teacher": None},
        {"name": "13MUSY", "subject": None, "teacher": "still_not"},
        {"name": "13ENGY", "subject": None, "teacher": None},
        {"name": "13GEOY", "subject": None, "teacher": "I_will_not_tell_you"},
        {"name": "13LAY", "subject": None, "teacher": None},
        {"name": "13MATG", "subject": None, "teacher": "the_answers_still_no"},
        {"name": "13GIFTY", "subject": None, "teacher": "oh_this_was_actually_one_of_my_favourite_teahcers_too_bad_I_wont_tell_you_who"},
        {"name": "13PDHY", "subject": None, "teacher": None},
        {"name": "13SCIY", "subject": None, "teacher": "this_teacher_is_also_pretty_cool"},
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
    "awards": [{"total": "0", "terms": {1: "1", 2: "0", 3: "0", 4: "0"}}],
}

```
Yes I'm doing Bowling for sport, yes all my friends are doing it too, yes, I'm a coder, so no, I do not like doing proper sport.
This is a lot of data, but having it nicely formatted and laid out here, should make it easier to understand. If I wanted to access the third class's teacher, then I would use ```sentralify(config)['student_details']['classes'][2]['teacher']```

#### Attendance
Okay, the attendance (added in v1.2.0) is really long, but I did it for you, you're welcome!
Below is a small snippet of one day of data
```
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
To get the your attendance status on the first day of the school year, you would call ```sentralify(config)['student_details']['attendance'][0][0][0]['status']```. The three zeros are the term, the week number in the term, and the day of the week.

### That's all folks!
That's all of my documentation for now, I think I've covered everything, now it's up to you to take this project places!


#### Why this doesn't use get-sentral's license
I didn't use get-sentral's license, because although the idea for me to make this came from their archiving of get-sentral, I used no code from get-sentral, and implemented and researched all of the code myself. So, in my opinion this was made from the ground up, and I did not ['remix, transform, and build upon the material'](https://creativecommons.org/licenses/by-nc-sa/4.0/) provided by get-sentral.
