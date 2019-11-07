import os
import platform
import sqlite3 as sql
import configparser

from sqlite3 import Cursor
from pandas import DataFrame

# Chrome's history file path relative to the home directory on different systems.
_CHROME_PROFILE_PATH = {
    'Windows': '~\\AppData\\Local\\Google\\Chrome\\User Data\\Default',
    'Linux': '~/.config/google-chrome/default',
    # MacOS
    'Darwin': '~/Library/Application Support/Google/Chrome/Default'
}

# Firefox's history file path relative to the home directory on different systems.
_FIREFOX_PROFILE_PATH = {
    'Windows': '~\\AppData\\Roaming\\Mozilla\\Firefox',
    'Linux': '~/.mozilla/firefox',
    # MacOS
    'Darwin': '~/Library/Application Support/Firefox'
}

# content = title of the page
_HISTORY_COLUMNS = ['url', 'content', 'visit_count', 'date']


def _get_chrome_history_file_path() -> str:
    """
    Get the absolute path of Chrome history file.
    :return: System-dependant path of Chrome history file.
    """
    system = platform.system()
    profile_path = os.path.expanduser(_CHROME_PROFILE_PATH[system])
    history_file_path = os.path.join(profile_path, 'History')
    return history_file_path


def get_chrome_history() -> DataFrame:
    with sql.connect(_get_chrome_history_file_path()) as conn:
        conn.text_factory = str
        cursor: Cursor = conn.cursor()
        # Chrome's timestamps are non-standard: they are calculated from January 1. 1601
        # Keep time in UTC timezone to avoid confusion
        cursor.execute('SELECT url, title, visit_count, '
                       'CASE last_visit_time '
                       'WHEN 0 THEN NULL '
                       'ELSE datetime(last_visit_time / 1000000 + strftime("%s", "1601-01-01 00:00:00"), "unixepoch") '
                       'END last_visit_time '
                       'FROM urls ORDER BY last_visit_time DESC;')
        history = DataFrame(cursor.fetchall(), columns=_HISTORY_COLUMNS)
        return history


def _get_firefox_history_file_path():
    """
    Get the path location of Firefox history file.
    :return: System-dependant path of Chrome history file.
    """
    # Get system-specific profile path
    system = platform.system()
    data_path = os.path.expanduser(_FIREFOX_PROFILE_PATH[system])

    # Read default profile from configuration file
    firefox_profiles_ini = os.path.join(data_path, 'profiles.ini')
    profiles = configparser.ConfigParser()
    profiles.read(firefox_profiles_ini)

    # Get default profile path
    profile_path = os.path.join(data_path, profiles.get('Profile0', 'Path'))
    # Places.sqlite is the file that stores the history of Firefox
    history_file_path = os.path.join(profile_path, 'places.sqlite')
    # Return the path of the history file
    return history_file_path


def get_firefox_history() -> DataFrame:
    with sql.connect(_get_firefox_history_file_path()) as conn:
        conn.text_factory = str
        cursor: Cursor = conn.cursor()
        # Keep time in UTC timezone to avoid confusion
        cursor.execute('SELECT url, title, visit_count, datetime(last_visit_date / 1000000, "unixepoch") '
                       'FROM moz_places ORDER BY last_visit_date DESC;')
        history = DataFrame(cursor.fetchall(), columns=_HISTORY_COLUMNS)
        return history


if __name__ == '__main__':
    df = get_chrome_history()
    df.to_csv('../../datasets/chrome_history_nathan.csv', index=False)
