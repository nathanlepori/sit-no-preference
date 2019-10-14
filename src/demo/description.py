import src.demo.defaults as default

# global state

state = False

def getState():
    return state

def toggleState():
    global state
    if not getState():
        state = True
        return state
    else:
        state = False
        return state

def desDefaultFileA():
    if getState():
        print(default.defaultFileA(), end='')
    return " "

def desDefaultFileB():
    if getState():
        print(default.defaultFileB(), end='')
    return " "

def desDefaultColumn():
    if getState():
        print(default.defaultColumn(), end='')
    return " "

def desDefaultDateColumn():
    if getState():
        print(default.defaultDateColumn(), end='')
    return " "

def desINFO():
    if getState():
        print("Description option here is to display a brief description of the selected option", end='\n')
    return " "

def desReadFile():
    if getState():
        print("This option is to indicate which file to read for 1st file \'file_A\' and 2nd file \'file_B\'", end='\n')
    return " "

def desDisplay():
    if getState():
        print("This option is to display content of 1st file \'file_A\' and 2nd file \'file_B\'", end='\n')
    return " "

def desToken():
    if getState():
        print("This option is to tokenize content of 1st file \'file_A\' and 2nd file \'file_B\' \n"
              "tokenize will change \"example of string\" to [\'example\',\'of\',\'string\'] based on selected column", end='\n')
    return " "

def desPOS():
    if getState():
        print("This option is to tokenize with Part-Of-Speech content of 1st file \'file_A\' and 2nd file \'file_B\' \n"
              "it will change \"sad happy\" to [ [\'sad\',\'ADJ\'] , [\'happy\',\'ADJ\'] ] based on selected column", end='\n')
    return " "

def desLabel():
    if getState():
        print("This option is to tokenize with Label content of 1st file \'file_A\' and 2nd file \'file_B\' \n"
              "it will change \"San Francisco\" to [[San Francisco, GPE]]  based on selected column", end='\n')
    return " "

def desSort():
    if getState():
        print("This option is to sort content of 1st file \'file_A\' and 2nd file \'file_B\' based on select column\n"
              "1:sort_by_date_range deals with filtering of data from a start dates to the end date\n"
              "2:sort_by_column deals with sorting of values in a column\n"
              "3:reindex deals with inaccurate index numbering after extensive usage\n"
              "4:upLowCase (must not be used after tokenize) deals with modifying all values to upper or lower case in a column", end='\n')
    return " "

def desVenn():
    if getState():
        print("venn diagram concepts \n"
              "1:Intersect_Unique show list of content found in both file\n"
              "2:Intersect change the dataframes to keep content found in both file\n"
              "3:SymmetricDif_Unique show list of content unique in each files\n"
              "4:SymmetricDif change the dataframes to NOT keep content found in both file\n"
              "5:Union merge both dataframe together as file_A and empty file_B", end='\n')

    return " "

def desClean():
    if getState():
        print("Remove empty list [] from the dataframe", end='\n')

    return " "