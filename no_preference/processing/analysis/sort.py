def reindex(df):
    """This function reset the dataframe format,
    This function drop old index column which contains the initial index value for each rows.
    """
    df = df.reset_index(drop=False)     # prevent move column header from bottom of row to top of row, drop false remove
    if 'index' in df.columns:               # if there exist an additional column call index
        df = df.drop(columns=['index'])     # we drop that column as we already have .index column from reset_index
    # dfData.index = dfData.index + 1 # let the index start from 1, this column of index does not have column header
    return df


def sort_by(df, column_name): # reformat date so the sorting starts from year-month-date
    """ used by sortByDateRange

    This function sort values by the column columnName.
    """

    df = df.sort_values(by=[column_name])  # sort the reformat date value
    return df


def sort_by_date_range(df, column_name, date_start, date_end):   # Please use functionSortByDate first before using this
    """ function used in search function
    function will call sortBy
     filter to keep only dates between dateStart and dateEnd

    """
    # dfData = sort.reindex(dfData)

    df = sort_by(df, column_name)
    df = df[df[column_name].between(date_start, date_end)]  # keep only date between dateStart and dateEnd
    return df
