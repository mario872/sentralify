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

import json
import re
from playwright.sync_api import expect
from bs4 import BeautifulSoup
import os

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Main scrapers class

class scrapers:
    def __init__(self, config: dict, timeout: int):
        """
        Run on creation of scrapers class, initiates
        config variable for the rest of the class

        Args:
            config (dict): Config dictionary with username, passwd, base_url, and state
        """
        
        self.config = config
        self.timeout = timeout
    
    def check_login(self, browser):
        
        try:
        
            page = browser.new_page()
            
            try:
                page.goto(f"https://{self.config['base_url']}.sentral.com.au/portal?action=login_student") # Go to main Sentral v2 portal login page
            except Exception as e:
                print(Exception)
                return False
            
            #page.get_by_label("Email or Username*").fill(self.config['username'])
            #page.get_by_label("Password*").fill(self.config['password'])
            #page.get_by_role("button", name="Log in").click()
            
            try:
                expect(page).to_have_title('Portal Login', timeout=1000)
                print('After portal login')
                return False
            except AssertionError:
                pass
            
            # Logging in using Microsoft account
            page.get_by_placeholder("Use your email address").fill(f'{self.config["username"]}@education.{self.config["state"]}.gov.au')
            page.get_by_role("button", name="Next").click()
            
            page.wait_for_timeout(5000)
            
            try:
                expect(page).not_to_have_title(re.compile('Sign in to your account'), timeout=5000)
            except AssertionError:
                return False
            
            page.get_by_placeholder("Enter your password").fill(self.config['password'])
            page.get_by_role("button", name="Sign in").click()
            
            try:
                expect(page).not_to_have_title('Sign In', timeout=1000)
                return True
            except AssertionError:
                return False

        except Exception as e:
            print('Uhoh! There\'s an error in check_login!')
            print(e)
            print(page.title)
            print(page.content())
            exit()
    
    def login(self, browser):
        """
        Logs into the Sentral portal using the login info from the config.json file

        Args:
            browser (playwright browser instance): A browser instnce created that playwright controls

        Returns:
            playwright page: The current page / tab object the playwright is working in, for continuity between functions
        """
        
        try:
        
            page = browser.new_page()
            
            page.goto(f"https://{self.config['base_url']}.sentral.com.au/portal?action=login_student") # Go to main Sentral v2 portal login page
            
            try: # If we have already signed in before, and the cookies haven't expired, then we will be redirected to the portal page automatically
                expect(page).to_have_title(re.compile(f"Portal - {self.config['username'].split('.')[0]}", re.IGNORECASE), timeout=self.timeout)
                return page
            except AssertionError: # Okay, we haven't logged in recently enough
                pass
            
            #page.get_by_label("Email or Username*").fill(self.config['username'])
            #page.get_by_label("Password*").fill(self.config['password'])
            #page.get_by_role("button", name="Log in").click()
            
            #try: # Hey, maybe we won't have to use a microsoft login at least?
            #    expect(page).to_have_title(re.compile(f"Portal - {self.config['username'].split('.')[0]}", re.IGNORECASE), timeout=1000)
            #    return page
            #except AssertionError: # Okay, never mind we do have to
            #    pass
            
            #found_email_address = False
            
            #try:
            #    expect(page.get_by_text(re.compile(f'{self.config["username"]}', re.IGNORECASE))).to_be_visible(timeout=3000)
            #    page.get_by_text(re.compile(f'{self.config["username"]}', re.IGNORECASE)).click()
            #    found_email_address = True
            #except AssertionError:
            #    pass
            
            # Logging in using Microsoft account
            #if not found_email_address:
            page.get_by_placeholder(re.compile("Use your email address")).fill(f'{self.config["username"]}@education.{self.config["state"]}.gov.au')
            page.get_by_role("button", name="Next").click()
                
            page.get_by_placeholder("Enter your password").fill(self.config['password'])
            page.get_by_role("button", name="Sign in").click()
            page.get_by_role("button", name="Yes").click()
            
            try: # We expect that we will be logged into Sentral by now
                expect(page).to_have_title(re.compile(f"Portal - {self.config['username'].split('.')[0].capitalize()}", re.IGNORECASE), timeout=3000)
            except AssertionError: # But sometimes, Sentral decides that EVEN A MICROSOFT ACCOUNT isn't enough veriication, and we have to log in again!
                try:
                    expect(page).to_have_title(re.compile('Portal - Login'))
                    page.get_by_label("Email or Username*").fill(self.config['username'])
                    page.get_by_label("Password*").fill(self.config['password'])
                    page.get_by_role("button", name="Log in").click()
                except AssertionError:
                    expect(page).to_have_title(re.compile(f"Portal - {self.config['username'].split('.')[0].capitalize()}", re.IGNORECASE), timeout=3000)

                    
            return page
        
        except Exception as e:
            try:
                expect(page).to_have_title(re.compile(f"Portal - {self.config['username'].split('.')[0]}", re.IGNORECASE), timeout=1000)
                return page
            except AssertionError:
                print('Uhoh! There\'s an error in login!')
                print(e)
                print(page.title)
                print(page.content())
                exit()
    
    def save_student_details(self, page):
        """
        Goes to the student details page after login, to get the student id for the timetable,
        AND get your classes, attendance, daily timetable, activites, and awards

        Args:
            page (playwright page): The current page / tab object the playwright is working in, for continuity between functions

        Returns:
            dict: A dictionary with the all the student's details from json on all the pages
        """

        self.portal_ver = 'portal' # or portal2

        # Student ID
        page.goto(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/{self.portal_ver}/user?action=getUserDetails")
        self.student_id = int(json.loads(BeautifulSoup(page.content(), "lxml").text)['student_id'])
        
        # Student's classes
        page.goto(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/{self.portal_ver}/user?action=get_student_info&student_id={str(self.student_id)}")
        classes = json.loads(BeautifulSoup(page.content(), "lxml").text)
        
        # Student's attendance record
        page.goto(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/{self.portal_ver}/attendance?action=getStudentHeatmapData&student_id={str(self.student_id)}")
        attendance = json.loads(BeautifulSoup(page.content(), "lxml").text)
        
        # Student's Attendaance Percent
        page.goto(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/{self.portal_ver}/attendance?action=getStudentTermAttendance&student_id={str(self.student_id)}")
        attendance_percent = json.loads(BeautifulSoup(page.content(), "lxml").text)
        
        #Student's daily timetable
        page.goto(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/{self.portal_ver}/timetable/getDailyTimetable/{str(self.student_id)}")
        daily_timetable = json.loads(BeautifulSoup(page.content(), "lxml").text)
        
        #Student's activites
        page.goto(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/{self.portal_ver}/activity/getStudentActivities/{str(self.student_id)}")
        activites = json.loads(BeautifulSoup(page.content(), "lxml").text)
        
        #Students awards
        #AWARDS ARE BROKEN
        #page.goto(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/{self.portal_ver}/wellbeing/overview/{str(self.student_id)}")
        #awards = json.loads(BeautifulSoup(page.content(), "lxml").text)
        awards = None

        return {'classes': classes,
                'attendance': attendance,
                'attendance_percent': attendance_percent,
                'daily_timetable': daily_timetable,
                'activities': activites,
                'awards': awards}
        

    def save_timetable(self, page):
        """
        Saves the timetable using a backend url to get JSON, instead of having to use BeautifulSoup on this too.
        
        Args:
            page (playwright page): The current page / tab object the playwright is working in, for continuity between functions

        Returns:
            dict: A dictionary with the timetable from the json on the page
        """
        
        # This just scrapes the page for the json, and converts it to a dictionary that python can acess.
        # I found this url after watching some kids at my school go into the network tab in dev tools in Chrome, and look at what Sentral was accessing. Thank you!
        
        page.goto(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/{self.portal_ver}/timetable/getFullTimetableInDates/{str(self.student_id)}/undefined/true")
        return json.loads(BeautifulSoup(page.content(), "lxml").text)

    def save_ics(self, page):
        """
        Saves the ics page and returns the html

        Args:
            page (playwright page): The current page / tab object the playwright is working in, for continuity between functions

        Returns:
            html: The html content on the page
        """
        
        ics_downloaded = False
        
        for i in range(3):
            try:
                #print(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/{self.portal_ver}/#!/timetable/{str(self.student_id)}")
                page.goto(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/{self.portal_ver}/#!/timetable/{str(self.student_id)}")
                with page.expect_download() as download_info:
                    page.get_by_text("Export as ICS").first.click()
                download = download_info.value

                download.save_as("timetable.ics")
                with open('timetable.ics', 'r') as timetable_ics:
                    timetable_ics_contents = timetable_ics.read()
                    
                os.remove("timetable.ics")
                ics_downloaded = True
                break
            except:
                pass
        if ics_downloaded:
            return timetable_ics_contents
        else:
            print('Welp, looks like there is an error in scrapers.save_ics')
            return None
        
    def save_notices(self, page):
        """
        Saves the notices page and returns the html

        Args:
            page (playwright page): The current page / tab object the playwright is working in, for continuity between functions

        Returns:
            html: The html content on the page
        """
        page.goto(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/{self.portal_ver}/#!/news/notices")
        page.get_by_role("button", name="Filter").click()
        page.get_by_text('Title Published after').click()
        page.get_by_role("button", name="Today").click()
        page.wait_for_timeout(500)
        return page.content()
    
    def save_calendar(self, page):
        """
        Saves the calendar page and returns the html

        Args:
            page (playwright page): The current page / tab object the playwright is working in, for continuity between functions

        Returns:
            html: The html content on the page
        """
        
        page.goto(f"https://{self.config['base_url']}.sentral.com.au/{self.config['unique_path']}/webcal/")
        return page.content()