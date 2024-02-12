# sentralify
Scrape Sentral data and use it!

Sentralify was designed to be a replacement for [get-sentral](https://github.com/J-J-B-J/get-sentral) a ***fantastic*** package developed by J-J-B-J and SuperHarmony910.
Sentralify can scrape data from the new Sentral frontend. So far it can scrape:
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

## Docs
sentralify is quite simple from the user's perspective, all you have to do is call ```sentralify(config)```, and it will magically scrape sentral for you and give you all the data you could ever want.
If you want to understand in more detail how this works, then read on!

### sentralify()
```sentralify()``` needs only 1 rgument but accepts 5. These five are ```config: dict, timetable: bool = True, notices: bool = True, calendar: bool = True, persistent: bool = True```; the last 4 are optional, and will all be ```True``` is not disabled. ```config``` is required, and accepts a python dictioary formatted as follows:

```
config = {"username": "your_username",
          "password": "your_password",
          "base_url": "base_url_here_eg_caringbahhs",
          "state": "your_state_here_eg_nsw",
          "headless": False}
```

```headless``` in the config, will dictate, whether a chromium window opens, or whether it does it all invisibly. ```timetable, notices, calendar``` are all pretty self-explanatory, if you enable them, then sentralify, will scrape the selected web pages, and format their output. ```persistent``` makes sentralify open Sentral in a normal chromium window (as opposed to an incognito window), this makes it a lot faster after the first sign in, as Sentral can just use the cookies saved to the contexts folder, and not require you to sign in again. On average, incognito mode takes around 20 seconds each time, and (after the first login), persistent takes around 3-10 seconds.

### sentralify() return data
sentralify returns a lot of data! Below is a documentation of what it returns
##### Timetable
The timetable that sentralify returns can be accessed by using ```sentralify(config)['timetable']```
Below is the general structure of one day, in one week that timetable returns:
```
[
    {
        "date": datetime.datetime(2024, 2, 12, 0, 0),
        "periods": [
            {
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
                "start": None,
                "end": None,
            },
            {
                "full_name": "PDHPE Yr13",
                "name": "13PDHY",
                "room": "GF.05",
                "teacher": "teacher_name",
                "border_colour": "85EE88",
                "background_colour": "E0FAE1",
                "start": None,
                "end": None,
            },
            {
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
                "start": None,
                "end": None,
            },
            {
                "full_name": "Mathematics Yr13",
                "name": "13MATG",
                "room": "EG.04",
                "teacher": "teacher_name",
                "border_colour": "FF7F7F",
                "background_colour": "FFDFDF",
                "start": None,
                "end": None,
            },
            {
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
                "start": None,
                "end": None,
            },
            {
                "full_name": "LAN Yr13",
                "name": "13LAY",
                "room": "GF.16",
                "teacher": "teacher_name",
                "border_colour": "FFBF7F",
                "background_colour": "FFEFDF",
                "start": None,
                "end": None,
            },
            {
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
                "start": None,
                "end": None,
            },
            {
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
                "start": None,
                "end": None,
            },
            {
                "full_name": "English Yr13",
                "name": "13ENGY",
                "room": "FF.06",
                "teacher": "teacher_name",
                "border_colour": "FFF884",
                "background_colour": "FFFDE0",
                "start": None,
                "end": None,
            },
            {
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
                "start": None,
                "end": None,
            },
            {
                "full_name": None,
                "name": None,
                "room": None,
                "teacher": None,
                "border_colour": None,
                "background_colour": None,
                "start": None,
                "end": None,
            },
        ],
        "is_today": True
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
        'date': datetime.datetime(2024, 2, 12, 0, 0),
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
        'title': 'Events: 12.30-1.45pm - Yr 11 Life Ready - Butterfly - Gym (teacher_name)',
        'start': datetime.datetime(2024, 2, 21, 12, 30),
        'end': datetime.datetime(2024, 2, 21, 13, 45),
        'date': datetime.datetime(2024, 2, 21, 0, 0)
    }
]
````

Yes, I'm tired of writing this dcoumentation, no I will not stop prematurely.
The general gist of how sentralify returns your celendar is multiple dictionaries in a list, each containing the title, start, end, and date. If you wanted to access the first events's end, then you would run ```sentralify(config)['calendar'][0]['end']```. Please note that not all events have the start and end fields filled out, as sometimes events just run all day instead.

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
    "attendance": {"terms": {"1": 100, "2": 0, "3": 0, "4": 0}, "overall": 100},
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
    "awards": [{"total": "0", "terms": {1: "0", 2: "0", 3: "0", 4: "0"}}],
}

```
Yes I'm doing Bowling for sport, yes all my friends are doing it too, yes, I'm a coder, so no, I do not like doing proper sport.
This is a lot of data, but having it nicely formatted and laid out here, should make it easier to understand. If I wanted to access the third class's teacher, then I would use ```sentralify(config)['student_details']['classes'][2]['teacher']```

### That's all folks!
That's all of my documentation for now, I think I've covered everything, now it's up to you to take this project places!


#### Why this doesn't use get-sentral's license
I didn't use get-sentral's license, because although the idea for me to make this came from their archiving of get-sentral, I used no code from get-sentral, and implemented and researched all of the code myself. So, in my opinion this was made from the ground up, and I did not ['remix, transform, and build upon the material'](https://creativecommons.org/licenses/by-nc-sa/4.0/) provided by get-sentral.
