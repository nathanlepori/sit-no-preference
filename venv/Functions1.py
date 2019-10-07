import csv
import pandas as pd

def functionOpenFile(filename):  # filename is to input government-procurement-via-gebiz.csv
    df = pd.read_csv(filename)
    return df


def functionCaseFile(df,setting): # string for setting is 'upper' or 'lower'
    """ This function is used to set all string in dataframe to upper or lower case. """
    if setting.lower() == 'lower':              # check if the setting match lower (check in lower caps)
        for column in df:                       # for each column in the dataframe
            if df[column].dtype == object:          # if columns is object type
                df[column] = df[column].str.lower() # set all the data in this column to lower case
    elif setting.lower() == 'upper':                # check if the setting match upper (check in lower caps)
        for column in df:                           # for each column in the dataframe
            if df[column].dtype == object:           # if columns is object type
                df[column] = df[column].str.upper()    # set all data in this column to UPPER case
    else:                                       # if setting does not match ignore
        pass
    return df


def functionSortBy(dfData,columnName): # reformat date so the sorting starts from year-month-date
    """ used by functionSortByDateRange

    This function set the columns which have dates to date format, and sort it by date
    This is so that the column can be sort by value of the date instead of the number.
    """

    dfData = dfData.sort_values(by=[columnName])  # sort the reformat date value
    return dfData


def functionSortByDateRange(dfData,columnName,dateStart,dateEnd):   # Please use functionSortByDate first before using this
    """ function used in search function
    function will call functionSortByDate
     filter to keep only dates between dateStart and dateEnd

    """
    dfData = functionSortBy(dfData,columnName)
    dfData = dfData[dfData[columnName].between(dateStart, dateEnd)]  # keep only date between dateStart and dateEnd
    return dfData