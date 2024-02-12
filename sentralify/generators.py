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
    def generate_timetable(data: list, daily_timetable: list):
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
                current_day = {'date': datetime.strptime(data[week]['dates'][day]['date_name'], '%Y-%m-%d'), 'periods': [], 'is_today': None} # The variable for this iteration of the loop
                
                for period in range(11): # There are eleven periods in every day, because of before school, recess, period 2-3 break, lunch 1, lunch 2, and after school.
                    current_day['periods'].append({}) # Add a blank space for this period in the list
                    # If the current period is today, then draw from the daily timetble instead of the cyclical timetable
                    if current_day['date'].day == datetime.now().day and current_day['date'].month == datetime.now().month:
                        current_period = daily_timetable[period]
                        current_day['is_today'] = True
                    else: # Otherwise, ujst draw from the cyclical timetable's data
                        current_period = data[week]['periods'][period]['days'][str(day + 1)]
                        current_day['is_today'] = False
                    
                    try: # Because period 0, recess, etc. don't have lessons, we get an IndexError when trying to access them
                        current_day['periods'][period]['full_name'] = current_period['lessons'][0]['subject_name']
                        current_day['periods'][period]['name'] = current_period['lessons'][0]['lesson_class_name']
                        try: # If there are no teachers (or room), then we get a KeyError instead
                            current_day['periods'][period]['room'] = current_period['lessons'][0]['room_name']
                            current_day['periods'][period]['teacher'] = current_period['lessons'][0]['teachers'][0]
                        except KeyError:
                            current_day['periods'][period]['room'] = None
                            current_day['periods'][period]['teacher'] = None
                        current_day['periods'][period]['border_colour'] = current_period['lessons'][0]['class_border_colour']
                        current_day['periods'][period]['background_colour'] = current_period['lessons'][0]['class_background_colour']
                    except IndexError:
                        current_day['periods'][period]['full_name'] = None
                        current_day['periods'][period]['name'] = None
                        current_day['periods'][period]['room'] = None
                        current_day['periods'][period]['border_colour'] = None
                        current_day['periods'][period]['background_colour'] = None
                        current_day['periods'][period]['teacher'] = None
                            
                    try: # We can try to get the start and end for the period, but sometimes, Sentral doesn't add that either!
                        current_day['periods'][period]['start'] = current_period['period_start_time']
                        current_day['periods'][period]['end'] = current_period['period_end_time']
                    except KeyError:
                        current_day['periods'][period]['start'] = None
                        current_day['periods'][period]['end'] = None

                timetable.append(current_day) # Add all of today's periods to the timetable
                    
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
                            'date': datetime(day=int(date_posted[0]), month=int(date_posted[1]), year=int(date_posted[2])),
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
                date = datetime(day=datetime.strptime(date, '%b %d').day, month=datetime.strptime(date, '%b %d').month, year=datetime.now().year)
            except ValueError:
                date = datetime(day=29, month=2, year=datetime.now().year)
                
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

                    end = parse(time.split(' - ')[1])
                    end = end.replace(day=date.day)
                    end = end.replace(month=date.month)
                    end = end.replace(year=datetime.now().year)
                                        
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
   
        details['attendance'] = data['attendance'] # The attendance is so well formatted already, that we just dupllicate it ointo the details
        
        # Gets all the activities the user is a part of and formats it and puts it in the details
        for activity in range(len(data['activities'])):
            activity_details = data['activities'][activity]
            details['activities'].append({'name': activity_details['name'],
                                          'start_date': parse(activity_details['start_date']),
                                          'end_date': parse(activity_details['end_date']),
                                          'start_time': parse(f"{activity_details['start_date']}-{activity_details['start_time']}"),
                                          'end_time': parse(f"{activity_details['end_date']}-{activity_details['end_time']}"),
                                          'points': activity_details['points'],
                                          'description': activity_details['description'],
                                          'category': activity_details['category']})
        
        details['awards'].append({'total': data['awards']['behavioural_summaries'][0]['total_count'],
                                 'terms': {1: data['awards']['behavioural_summaries'][0]['term']['1'],
                                           2: data['awards']['behavioural_summaries'][0]['term']['2'],
                                           3: data['awards']['behavioural_summaries'][0]['term']['3'],
                                           4: data['awards']['behavioural_summaries'][0]['term']['4']}})
        
        return details