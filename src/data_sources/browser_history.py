import csv
import os
import sqlite3 as sq

import configparser


def get_chrome_history_folder():  # getting the path location of chrome history file
    data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    files = os.listdir(data_path)
    history_db = os.path.join(data_path, 'history')
    return history_db


# TODO: Do not write file directly
def get_chrome_history():
    with sq.connect(get_chrome_history_folder()) as conn:
        conn.text_factory = str
        c = conn.cursor()
        output_file_path = 'chrome_history.csv'
        with open(output_file_path, 'wb') as output_file:
            csv_writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
            headers = ['URL', 'Title', 'Visit Count', 'Last Accessed Date-Time (GMT+8)']
            csv_writer.writerow(headers)
            for row in (c.execute(
                    'SELECT urls.url, urls.title, urls.visit_count, '
                    'datetime((urls.last_visit_time/1000000)-11644473600,\'unixepoch\', \'localtime\') '
                    'FROM urls '
                    'order by urls.last_visit_time desc;')):
                row = list(row)
                csv_writer.writerow(row)


# TODO: Not portable: only works on Windows
def get_mozilla_history_file():  # getting the path location of firefox history file
    # the following 5 lines of code will retrieve the profile of firefox
    mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
    mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
    profile = configparser.ConfigParser()
    profile.read(mozilla_profile_ini)
    data_path = os.path.normpath(os.path.join(mozilla_profile, profile.get('Profile0', 'Path')))
    mozilla_history_file = data_path + '\\places.sqlite'  # places.sqlite is the file that store the history of firefox
    return mozilla_history_file  # return the path of the history file


# TODO: Do not write file directly
def get_mozilla_history():
    with sq.connect(get_mozilla_history_file()) as conn:
        conn.text_factory = str
        c = conn.cursor()
        output_file_path = 'firefox_history.csv'
        with open(output_file_path, 'wb') as output_file:
            csv_writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
            headers = ['URL', 'Title', 'Visit Count', 'Last Accessed DAte-Time (GMT+8)']
            csv_writer.writerow(headers)
            for row in (c.execute(
                    'select moz_places.url, moz_places.title, moz_places.visit_count, '
                    'datetime(moz_places.last_visit_date/1000000,\'unixepoch\', \'localtime\') '
                    'from moz_places '
                    'order by last_visit_date desc')):
                row = list(row)
                csv_writer.writerow(row)
