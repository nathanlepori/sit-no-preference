import csv
from datetime import datetime
import os
import sqlite3 as sq

import configparser


def getChromeHistoryFolder():  # Getting the path location of chrome history file
    try:
        data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        files = os.listdir(data_path)
        history_db = os.path.join(data_path, 'history')
        return history_db  # Return the path for chrome history
    except Exception as ex:
        print 'An error occurred. Please contact the administrator!'


def retrieveChromeHistory():  # Retrieve chrome history from the history file
    try:
        with sq.connect(getChromeHistoryFolder()) as conn:  # Connect to the chrome history database
            conn.text_factory = str
            c = conn.cursor()
            output_file_path = 'chromeHistory.csv'  # Defining file to store chrome history
            with open(output_file_path, 'wb') as chromeHistoryOutput:  # Open the file to write chrome history
                csv_writer = csv.writer(chromeHistoryOutput, quoting=csv.QUOTE_ALL)
                # Defining header to store the respective fields
                headers = ['URL', 'Title', 'Visit Count', 'Last Accessed Date-Time (GMT+8)']
                csv_writer.writerow(headers)  # Write headers to csv file

                print "\nStarting job at " + str(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")) + \
                      "\nWriting data from chrome database to file..."

                # Retrieve specific columns in the database table and write to file
                for row in (c.execute(
                        'SELECT urls.url, urls.title, urls.visit_count, '
                        'datetime((urls.last_visit_time/1000000)-11644473600,\'unixepoch\', \'localtime\') '
                        'FROM urls '
                        'order by urls.last_visit_time desc;')):
                    row = list(row)
                    csv_writer.writerow(row)

            # Close csv file
            chromeHistoryOutput.close()

            print "Finished writing chrome history data to file at " + \
                  str(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S") + "\n")

    except Exception as ex:
        print 'An error occurred. Please contact the administrator!'


def getFirefoxHistoryFile():  # Getting the path location of firefox history file
    try:
        # the following 5 lines of code will retrieve the profile of firefox
        mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
        mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
        profile = configparser.ConfigParser()
        profile.read(mozilla_profile_ini)
        data_path = os.path.normpath(os.path.join(mozilla_profile, profile.get('Profile0', 'Path')))
        # places.sqlite is the file that store the history of firefox
        mozilla_history_file = data_path + '\\places.sqlite'
        return mozilla_history_file  # Return the path for firefox history
    except Exception as ex:
        print 'An error occurred. Please contact the administrator!'


def retrieveFirefoxHistory():  # Retrieve firefox history from the history file
    try:
        with sq.connect(getFirefoxHistoryFile()) as conn:  # Connect to the firefox history database
            conn.text_factory = str
            c = conn.cursor()
            output_file_path = 'firefoxHistory.csv'  # Defining file to store firefox history
            with open(output_file_path, 'wb') as firefoxHistoryOutput:  # Open file to write firefox history
                csv_writer = csv.writer(firefoxHistoryOutput, quoting=csv.QUOTE_ALL)
                # Defining header to store the respective fields
                headers = ['URL', 'Title', 'Visit Count', 'Last Accessed DAte-Time (GMT+8)']
                csv_writer.writerow(headers)  # Write headers to file

                print "Starting job at " + str(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")) + \
                      "\nWriting data from firefox database to file..."

                # Retrieve specific columns in the database table and write to file
                for row in (c.execute(
                        'select moz_places.url, moz_places.title, moz_places.visit_count, '
                        'datetime(moz_places.last_visit_date/1000000,\'unixepoch\', \'localtime\') '
                        'from moz_places '
                        'order by last_visit_date desc')):
                    row = list(row)
                    csv_writer.writerow(row)

            # Close csv file
            firefoxHistoryOutput.close()

            print "Finished writing firefox history data to file at " + \
                  str(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S"))

    except Exception as ex:
        print 'An error occurred. Please contact the administrator!'


retrieveChromeHistory()
retrieveFirefoxHistory()
