"""
Sentralify scrapes Sentral user data, such as timetables, notices, calendar events, and student details.

Copyright (C) 2026  James Glynn

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
from pathlib import Path
import time

from .scrapers import scrapers
from . import generators

class Sentralify:
    def __init__(self, username: str, password: str, prefix: str, state: str, headless: bool=True, persistent: bool=False, persistent_dir: str|Path=Path("./sentralify_data/")) -> None:
        """Assign this class to a variable and instantiate it to use the scraping functions.

        Args:
            username (str): The user's user name, e.g. john.smith, jane.doe, etc.
            password (str): The user's password
            prefix (str): (Previously base_url) The prefix before .sentral.com.au in the Sentral URL, e.g. caringbahhs, stpauls, etc.
            state (str): The abbreviated state of the school, e.g. nsw / NSW instead of New South Wales, vic / VIC instead of Victoria, etc.
            headless (bool, optional): Whether or not to run the browser in headless mode. Defaults to True.
            persistent (bool, optional): Whether or not to make the browser instance consistent pros: makes logging in faster, cons: stores data on computer. Defaults to False.
            persistent_dir (str | Path, optional): The path to the persistent browser context. Defaults to Path("./sentralify_data/").
        """
        
        self.user_name = username
        self.password = password
        self.prefix = prefix
        self.state = state
        self.headless = headless
        self.persistent = persistent
        self.persistent_dir = persistent_dir

        self.config = {
            "username": self.user_name,
            "password": self.password,
            "prefix": self.prefix,
            "state": self.state,
            "headless": self.headless,
        }

    def verify_login(self, timeout=5000) -> bool:
        """Checks if the login credentials are valid, returns a boolean. This is used for the check_login parameter in the sentralify function, but can also be used on its own if you just want to check if the login credentials are valid without scraping any data.

        Args:
            timeout (int, optional): The timeout for the scraper, in milliseconds. Default is 5 seconds.
        Returns:
            bool: Whether or not the login credentials are valid
        """

        p = sync_playwright().start() # Start a playwright instance
        
        # Initialise scraper
        scraper = scrapers(self.config, timeout=timeout)

        browser = p.chromium.launch(headless=self.headless)

        value = scraper.check_login(browser)
        browser.close()
        p.stop()
        return value

    def sentralify(self, scrape_timetable: bool=True, scrape_notices: bool=True, scrape_calendar: bool=True, scrape_ics: bool=False, timeout=5000) -> dict:
        """Scrapes the Sentral data, returns a dictionary with the timetable, notices, calendar, student details, and the amount of time it took to gather the data.

        Args:
            scrape_notices (bool, optional): Scrape the school notices. Defaults to True.
            scrape_timetable (bool, optional): Scrape the timetable. Defaults to True.
            scrape_calendar (bool, optional): Scrape the school calendar. Defaults to True.
            scrape_ics (bool, optional): Scrape the ICS file. Defaults to False.
            timeout (int, optional): The timeout for the scraper, in milliseconds. Default is 5000 milliseconds (5 seconds).
        """

        start = time.time() # So that we can know how long it took to scrape the Sentral data

        p = sync_playwright().start() # Start a playwright instance
    
        # Initialise the generators and scrapers
        scraper = scrapers(self.config, timeout=timeout)
        
        if self.persistent: # If this should be a persistent browser context, then launch it as persistent, otherwise launch in incognito mode
            browser = p.chromium.launch_persistent_context(self.persistent_dir, headless=self.headless)
        else:
            browser = p.chromium.launch(headless=self.headless)
        
        page = scraper.login(browser) # Login to Sentral
        
        # Set up the variable for the data we have to return to the user
        data = {'notices': None,
                'timetable': None,
                'calendar': None,
                'student_details': None,
                'time_elapsed': None}
        
        student_details = scraper.save_student_details(page) # Save the student details (mandatory)
        daily_timetable = student_details['daily_timetable'] # Save the daily_timetable
        
        data['student_details'] = generators.generate_student_details(student_details) # Save the formatted student details in the return data
            
        # A bunch of if blocks to determine whether or not to scrape parts of sentral
        if scrape_notices:
            notices = generators.generate_notices(scraper.save_notices(page))
            data['notices'] = notices
        if scrape_timetable:
            timetable = generators.generate_timetable(scraper.save_timetable(page))
            data['timetable'] = timetable
        if scrape_ics:
            ics = scraper.save_ics(page)
            data['ics'] = ics
        if scrape_calendar:
            calendar = generators.generate_calendar(scraper.save_calendar(page))
            data['calendar'] = calendar
            
        browser.close() # Close the browser, as  our work is done
        p.stop() # Stopping playwright instance
        
        data['time_elapsed'] = time.time() - start # Add how long it took to do all of that scraping and generating
        
        return data