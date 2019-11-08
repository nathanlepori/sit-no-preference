def reindex(dfData):
    """This function reset the dataframe format,
    This function drop old index column which contains the initial index value for each rows.
    """
    dfData = dfData.reset_index(drop=False)     # prevent move column header from bottom of row to top of row, drop false remove
    if 'index' in dfData.columns:               # if there exist an additional column call index
        dfData = dfData.drop(columns=['index'])     # we drop that column as we already have .index column from reset_index
    # dfData.index = dfData.index + 1 # let the index start from 1, this column of index does not have column header
    return dfData


def sort_by(dfData, columnName): # reformat date so the sorting starts from year-month-date
    """ used by sortByDateRange

    This function sort values by the column columnName.
    """

    dfData = dfData.sort_values(by=[columnName])  # sort the reformat date value
    return dfData


def sort_by_date_range(dfData, columnName, dateStart, dateEnd):   # Please use functionSortByDate first before using this
    """ function used in search function
    function will call sortBy
     filter to keep only dates between dateStart and dateEnd

    """
    # dfData = sort.reindex(dfData)

    dfData = sort_by(dfData, columnName)
    dfData = dfData[dfData[columnName].between(dateStart, dateEnd)]  # keep only date between dateStart and dateEnd
    return dfData
