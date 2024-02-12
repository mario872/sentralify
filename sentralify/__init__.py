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

from playwright.sync_api import sync_playwright
import json
import time

from sentralify.scrapers import scrapers
from sentralify.generators import generators

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

def sentralify(config: dict, timetable: bool = True, notices: bool = True, calendar: bool = True, persistent: bool = True):
    """
    Function to scrape Sentral
        
    Args:
        config (dict): A dictionary with the fields: username, password, base_url, state, and headless
        timetable (bool | True): Whether or not to scrape the timetable
        notices (bool | True): Whether or not to scrape the notices
        calendar (bool | True): Whether or not to scrape the calendar
        student_details (bool | True): Whether or not to scrape the student details
        persistent (bool | True): Whether or not to make the browser instance consistent pros: makes logging in faster, cons: stores data on computer

    Returns:
        dict: A dictionary with the timetable, notices, calendar, student details, and the amount of time it took to gather the data
    """
    
    start = time.time() # So that we can know how long it took to scrape the Sentral data
    
    p = sync_playwright().start() # Start a playwright instance
    
    # Initialise the generators and scrapers
    Sentral = generators
    scraper = scrapers(config)
    
    if persistent: # If this should be a persistent browser context, then launch it as persistent, otherwise launch in incognito mode
        browser = p.chromium.launch_persistent_context(f"contexts/{config['username']}", headless=config['headless'])
    else:
        browser = p.chromium.launch(headless=config['headless'])
        
    page = scraper.login(browser) # Login to Sentral
    
    # Set up the variable for the data we have to return to the user
    data = {'notices': None,
            'timetable': None,
            'calendar': None,
            'student_details': None,
            'time_elapsed': None}
    
    student_details = scraper.save_student_details(page) # Save the student details (mandatory)
    daily_timetable = student_details['daily_timetable'] # Save the daily_timetable
    
    data['student_details'] = Sentral.generate_student_details(student_details) # Save the formatted student details in the return data
        
    # A bunch of if blocks to determine whether or not to scrape parts of sentral
    if notices:
        notices = Sentral.generate_notices(scraper.save_notices(page))
        data['notices'] = notices
    if timetable:
        timetable = Sentral.generate_timetable(scraper.save_timetable(page), daily_timetable)
        data['timetable'] = timetable
    if calendar:
        calendar = Sentral.generate_calendar(scraper.save_calendar(page))
        data['calendar'] = calendar
        
    browser.close() # Close the browser, as  our work is done
    
    data['time_elapsed'] = time.time() - start # Add how long it took to do all of that scraping and generating
    
    return data