"""
Copyright (C) 2024  James Glynn

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.html.
"""

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Imports

import re
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
from markdownify import MarkdownConverter

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Main generators class

class generators:
    def generate_timetable(data: list):
        """
        Takes a list of the JSON data scraped from the backend timetable page and moulds it
        into a nice Python dictionary with only the information that is needed for most applications

        Args:
            data (list): A list of the data from scraping the JSON on the backend timetable page
            daily_timetable (list): A list of the daily timetable from the student_details scraper

        Returns:
            dict: A dictionary with the timetable
        """
        
        # IMPORTANT NOTE, if I or anyone else ends up needing or wanting to rewrite this at some point, they should
        # use this url instead: https://base_rul_here.sentral.com.au/s-Y7eXkn/portal2/timetable/getFullTimetableInDates/student_id_here/undefined/true
        # It's a much better formatted version of the timetable
        
        
        timetable = [] # This will store the timetable days and periods
        for week in range(2): # Two weeks are returned by the JSON
            for day in range(5): # Only five days in a school week, not seven!
                timetable.append({}) # Add the new day to the timetable
                
                # This is to add five days onto the day loop number for week B
                if week == 0:
                    timetable_day = day
                else:
                    timetable_day = day + 5
                    
                current_day_data = data[week]['dates'][str(day+1)] # This makes it easier to reference just the day we need
                timetable[timetable_day]['periods'] = [] # Add a blank space for this day in the list
                timetable[timetable_day]['date'] = parse(current_day_data['date_name']).strftime('%c') # Add the date to the day
                timetable[timetable_day]['is_today'] = current_day_data['is_today'] # Add is_today to the day
                
                for period in range(len(current_day_data['period'])): # Instead of asusuming it will be eleven periosd, this just returns however many periods there are
                    timetable[timetable_day]['periods'].append({}) # Make space for a new period on the day
                    
                    timetable[timetable_day]['periods'][period]['is_now'] = current_day_data['period'][period]['is_now'] # Add is_now to the period, a new parameter
                    if current_day_data['period'][period]['start_time'] != None: # Checking that Sentral igves th estart time
                        timetable[timetable_day]['periods'][period]['start'] = current_day_data['period'][period]['start_time'] # The generic hour:minute start time
                        timetable[timetable_day]['periods'][period]['end'] = current_day_data['period'][period]['end_time'] # The generic hour:minute end time
                        timetable[timetable_day]['periods'][period]['start_time_date'] = datetime( # This creates a datetime object with the full date and time of the start of the period
                                                                                        year=parse(timetable[timetable_day]['date']).year,
                                                                                        month=parse(timetable[timetable_day]['date']).month,
                                                                                        day=parse(timetable[timetable_day]['date']).day,
                                                                                        hour=int(current_day_data['period'][period]['start_time'].split(':')[0]),
                                                                                        minute=int(current_day_data['period'][period]['start_time'].split(':')[1])
                                                                                        ).strftime('%c')
                        timetable[timetable_day]['periods'][period]['end_time_date'] = datetime( # This creates a datetime object with the full date and time of the end of the period/
                                                                                        year=parse(timetable[timetable_day]['date']).year,
                                                                                        month=parse(timetable[timetable_day]['date']).month,
                                                                                        day=parse(timetable[timetable_day]['date']).day,
                                                                                        hour=int(current_day_data['period'][period]['end_time'].split(':')[0]),
                                                                                        minute=int(current_day_data['period'][period]['end_time'].split(':')[1])
                                                                                        ).strftime('%c')
                    else: # Sometimes, if it's a holiday, or Sentral wants to be annoying they don't give the start time or end time
                        timetable[timetable_day]['periods'][period]['start'] = None
                        timetable[timetable_day]['periods'][period]['end'] = None
                        timetable[timetable_day]['periods'][period]['start_time_date'] = None
                        timetable[timetable_day]['periods'][period]['end_time_date'] = None
                    
                    if current_day_data['period'][period]['lessons'] != []: # If it's a period without a lesson, then there's nothing in the lesson parameter
                        timetable[timetable_day]['periods'][period]['full_name'] = current_day_data['period'][period]['lessons'][0]['subject_name']
                        timetable[timetable_day]['periods'][period]['name'] = current_day_data['period'][period]['lessons'][0]['lesson_class_name']
                        try:
                            timetable[timetable_day]['periods'][period]['room'] = current_day_data['period'][period]['lessons'][0]['room_name']
                        except KeyError: # If there's not set it to None:
                            timetable[timetable_day]['periods'][period]['room'] = None
                        timetable[timetable_day]['periods'][period]['border_colour'] = current_day_data['period'][period]['lessons'][0]['class_border_colour']
                        timetable[timetable_day]['periods'][period]['background_colour'] = current_day_data['period'][period]['lessons'][0]['class_background_colour']
                        try: # This checks that there is a teacher during the lesson
                            timetable[timetable_day]['periods'][period]['teacher'] = current_day_data['period'][period]['lessons'][0]['teachers'][0] # The 0 at the end could be a mistake, if anyone knows, please open an issue
                        except KeyError: # If there's not set it to None
                            timetable[timetable_day]['periods'][period]['teacher'] = None
                    else: # If there isn't a lesson on, then it's not a proper period
                        timetable[timetable_day]['periods'][period]['full_name'] = None
                        timetable[timetable_day]['periods'][period]['name'] = None
                        timetable[timetable_day]['periods'][period]['room'] = None
                        timetable[timetable_day]['periods'][period]['teacher'] = None
                        timetable[timetable_day]['periods'][period]['border_colour'] = None
                        timetable[timetable_day]['periods'][period]['background_colour'] = None
                        
        return timetable

    
    def generate_notices(data):
        """
        Takes the notices' html page and forcibly scrapes all of the important data from it
        and puts it in a nice looking Python dictionary

        Args:
            data (html): The html from the notices page

        Returns:
            list: A list with the notices (the body of the messages are in markdown to retain formatting if you want it later)
        """
        
        soup = BeautifulSoup(data, 'html.parser') # Pull the html page into BeautifulSoup's parser
        
        results = soup.find(id="left-col") # Get the full html of all notices
        notices_raw = results.find_all("div", class_=["dash_collection", "ng-scope"]) # Get each nontice card individually
        
        notices = [] # Where the notices will be stored
        for notice in notices_raw:
            try: # Sometimes teachers just don't add a title on their notices, this deals with that by skipping the message entirely
                title = notice.find('h4', class_='ng-binding').text.strip()
                if title == '' or title == ' ' or title == '\n':
                    continue
                
            except AttributeError:
                continue
            
            date_posted = notice.find('p', class_=['small', 'right', 'ng-binding']).text.strip().split('/')
            
            posted_by = notice.find('p', string=re.compile("Posted by ")).text.strip().replace('Posted by ', '')
            
            text = notice.find('div', class_='ng-binding')
            
            if text != '' and text != ' ' and text != '\n':
                text = MarkdownConverter().convert_soup(text) # Turn the html into markdown instead, to retain the formatting
            else:
                text = 'This message has no content.'
                
            notices.append({'title': title,
                            'date': datetime(day=int(date_posted[0]), month=int(date_posted[1]), year=int(date_posted[2])).strftime('%c'),
                            'author': posted_by,
                            'content': text})
            
        return notices

    def generate_calendar(data):
        """
        Takes the calendar's html page and forcibly scrapes all of the important data from it
        and puts it in a nice looking Python dictionary

        Args:
            data (html): The html from the calendar page

        Returns:
            list: A list with the calendar events
        """
        
        soup = BeautifulSoup(data, 'html.parser') # Pulls the html into BeautifulSoups's parser
        
        results = soup.find_all('tbody')[1] # Find the right table of data
        calendar_raw = results.find_all(re.compile(''), id=re.compile('caltd')) # Find all of the events on the tbody
        
        events = [] # All the events
        for day in calendar_raw:
            date = day.find('div', class_='calendar-cell-date').text.strip()
            
            try: # We try to set the date, but because Fabruary 29th isn't a real day apparently, this accounts for that
                date = datetime(day=datetime.strptime(date, '%b %d').day, month=datetime.strptime(date, '%b %d').month, year=datetime.now().year).strftime('%c')
            except ValueError:
                date = datetime(day=29, month=2, year=datetime.now().year).strftime('%c')
                
            day = day.find_all('div', class_=['btn-small', 'event'])
            
            for event in day:
                title = event.text.strip()
                if title == '' or title == ' ' or title == '\n':
                    continue
                
                try: # Try and set the time
                    time = event.find('span', class_='tool-tip-time').text.strip()
                    title = title.replace(time, '')
                    
                    start = parse(time.split(' - ')[0])
                    start = start.replace(day=date.day)
                    start = start.replace(month=date.month)
                    start = start.replace(year = datetime.now().year)
                    start = start.strftime('%c')
                    
                    end = parse(time.split(' - ')[1])
                    end = end.replace(day=date.day)
                    end = end.replace(month=date.month)
                    end = end.replace(year=datetime.now().year)
                    end = end.strftime('%c')
                                        
                except Exception as e: # Sometimes there is no specific time for an event, so just set it to none
                    start = None
                    end = None
                
                events.append({'title': title,
                            'start': start,
                            'end': end,
                            'date': date})
                
        return events            

    def generate_student_details(data: dict):
        """
        Generates various details about the student includes:
        Student id, first name, last name, full name, school year, roll class, classes, attendance, activities, and awards

        Args:
            data (dict): Data scraped from various pages to get data about the user

        Returns:
            dict: A dictionary with various details about the user
        """
        
        # Creating a template details dictionary to fill in and return
        details = {'student_id': None,
                   'first_name': None,
                   'surname': None,
                   'name': None,
                   'school_year': None,
                   'rollclass': {},
                   'classes': [],
                   'attendance': {},
                   'activities': [],
                   'awards': []}
        
        details['student_id'] = int(data['classes']['student_id'])
        details['first_name'] = data['classes']['pref_name']
        details['surname'] = data['classes']['surname']
        details['name'] = details['first_name'] + ' ' + details['surname']
        details['school_year'] = int(data['classes']['schoolYear'])
        
        details['rollclass']['name'] = data['classes']['rollclass']['name']
        details['rollclass']['teacher'] = data['classes']['rollclass']['teacher']
        
        # Each class that a user has should be added to the list
        for rollclass in range(len(data['classes']['classes'])):
            class_details = data['classes']['classes'][rollclass]
            details['classes'].append({'name': class_details['name'],
                                       'subject': class_details['subject'],
                                       'teacher': class_details['teacher']})
        
        # We need to reformat the attendance data so that it is easier to use pythonically
        details['attendance'] = []
        for term in range(4):
            details['attendance'].append([])
            for week in range(len(data['attendance'][str(term+1)].keys())):
                details['attendance'][term].append([]) # Check 3
                for day in range(len(data['attendance'][str(term+1)][str(week+1)].keys())): # For some reason, they chose to make the backend start from 1 instead of 0.
                    details['attendance'][term][week].append({'date': None, 'status': None, 'description': None})
                    details['attendance'][term][week][day]['date'] = parse(data['attendance'][str(term+1)][str(week+1)][list(data['attendance'][str(term+1)][str(week+1)].keys())[day]]['date']).strftime('%c')
                    details['attendance'][term][week][day]['status'] = data['attendance'][str(term+1)][str(week+1)][list(data['attendance'][str(term+1)][str(week+1)].keys())[day]]['status']
                    try: # Future dates don't have a description
                        details['attendance'][term][week][day]['description'] = data['attendance'][str(term+1)][str(week+1)][list(data['attendance'][str(term+1)][str(week+1)].keys())[day]]['description']
                    except KeyError:
                        details['attendance'][term][week][day]['description'] = None
        
        # A quick reformatting of the attendance percentages so that it is easier to use pythonically
        details['attendance_percent'] = [data['attendance_percent']['terms']['1'], data['attendance_percent']['terms']['2'], data['attendance_percent']['terms']['3'], data['attendance_percent']['terms']['4']]

        # Gets all the activities the user is a part of and formats it and puts it in the details
        for activity in range(len(data['activities'])):
            activity_details = data['activities'][activity]
            details['activities'].append({'name': activity_details['name'],
                                          'start_date': parse(activity_details['start_date']).strftime('%c'),
                                          'end_date': parse(activity_details['end_date']).strftime('%c'),
                                          'start_time': parse(f"{activity_details['start_date']}-{activity_details['start_time']}").strftime('%c'),
                                          'end_time': parse(f"{activity_details['end_date']}-{activity_details['end_time']}").strftime('%c'),
                                          'points': activity_details['points'],
                                          'description': activity_details['description'],
                                          'category': activity_details['category']})
        
        details['awards'] = []

        for year in data['awards']["behavioural_summaries"].keys():
            current_year_data = data['awards']["behavioural_summaries"][year][0]
            details['awards'].append({
                'year': year,
                1: current_year_data["term"]["1"],
                2: current_year_data["term"]["2"],
                3: current_year_data["term"]["3"],
                4: current_year_data["term"]["4"],
                "total": current_year_data["total_count"]
            })

        return details
