import csv
import os
import sqlite3 as sq

import configparser

def getChromeHistoryFolder(): # getting the path location of chrome history file
    data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    files = os.listdir(data_path)
    history_db = os.path.join(data_path, 'history')
    return history_db

# need to take a look at this link:
# https://stackoverflow.com/questions/43435216/sql-after-the-join-remove-duplicate-rows

with sq.connect(getChromeHistoryFolder()) as conn:
    conn.text_factory = str
    c = conn.cursor()
    output_file_path = 'chrome_history.csv'
    with open(output_file_path, 'wb') as output_file:
        csv_writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        headers = ['URL', 'Title', 'Visit Count', 'Last Accessed Date-Time (GMT)',
                   'Duration of Last Accessed (in seconds)']
        csv_writer.writerow(headers)
        # epoch = datetime(1601, 1, 1)
        for row in (c.execute(
                'select u.url, u.title, u.visit_count, '
                'datetime((u.last_visit_time/1000000)-11644473600,\'unixepoch\', \'localtime\'), '
                '(v.visit_duration/1000000) '
                'from urls as u '
                'inner join visits as v on u.id = v.id '
                # 'group by u.url, u.title, u.visit_count, u.last_visit_time, v.visit_duration '
                'order by u.last_visit_time desc;')):
            row = list(row)
            # url_time = epoch + timedelta(microseconds=row[3])
            # row[3] = url_time
            csv_writer.writerow(row)
        # for row in (c.execute(
        #         'SELECT urls.url, urls.title, urls.visit_count, '
        #         'datetime((urls.last_visit_time/1000000)-11644473600,\'unixepoch\', \'localtime\') '
        #         'FROM urls '
        #         'order by urls.last_visit_time desc;')):
        #     row = list(row)
        #     # url_time = epoch + timedelta(microseconds=row[3])
        #     # row[3] = url_time
        #     csv_writer.writerow(row)
os.startfile(output_file_path)

def getMozillaHistoryFile(): # getting the path location of firefox history file
    # the following 5 lines of code will retrieve the profile of firefox
    mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
    mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
    profile = configparser.ConfigParser()
    profile.read(mozilla_profile_ini)
    data_path = os.path.normpath(os.path.join(mozilla_profile, profile.get('Profile0', 'Path')))
    mozilla_history_file = data_path + '\\places.sqlite' # places.sqlite is the file that store the history of firefox
    return mozilla_history_file # return the path of the history file

with sq.connect(getMozillaHistoryFile()) as conn:
    conn.text_factory = str
    c = conn.cursor()
    output_file_path = 'firefox_history.csv'
    with open(output_file_path, 'wb') as output_file:
        csv_writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        headers = ['URL', 'Title', 'Visit Count', 'Last Accessed (GMT)']
        csv_writer.writerow(headers)
        for row in (c.execute(
                'select moz_places.url, moz_places.title, moz_places.visit_count, '
                'datetime(moz_places.last_visit_date/1000000,\'unixepoch\', \'localtime\') '
                'from moz_places order by last_visit_date desc')):
            row = list(row)
            csv_writer.writerow(row)
os.startfile(output_file_path)