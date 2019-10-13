def reindex(dfData):
    """This function reset the dataframe format,
    This function drop old index column which contains the initial index value for each rows.
    """
    dfData = dfData.reset_index(drop=False)     # prevent move column header from bottom of row to top of row, drop false remove
    if 'index' in dfData.columns:               # if there exist an additional column call index
        dfData = dfData.drop(columns=['index'])     # we drop that column as we already have .index column from reset_index
    # dfData.index = dfData.index + 1 # let the index start from 1, this column of index does not have column header
    return dfData

def caseFile(df,setting): # string for setting is 'upper' or 'lower'
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

def sortBy(dfData,columnName): # reformat date so the sorting starts from year-month-date
    """ used by sortByDateRange

    This function set the columns which have dates to date format, and sort it by date
    This is so that the column can be sort by value of the date instead of the number.
    """

    dfData = dfData.sort_values(by=[columnName])  # sort the reformat date value
    return dfData


def sortByDateRange(dfData,columnName,dateStart,dateEnd):   # Please use functionSortByDate first before using this
    """ function used in search function
    function will call sortBy
     filter to keep only dates between dateStart and dateEnd

    """
    dfData = sortBy(dfData,columnName)
    dfData = dfData[dfData[columnName].between(dateStart, dateEnd)]  # keep only date between dateStart and dateEnd
    return dfData
