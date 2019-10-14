import sys
import src.demo.spacyNLP as spacyNLP
import src.demo.sort as sort
import src.demo.venn as venn
import pandas as pd
import spacy
nlp = spacy.load("en_core_web_sm")


def headerOutput():
    print("No Preference - Profiler, cmd line user input")

def defaultFileA():
    filenameA = '..\..\dataset\words.csv'
    return filenameA

def defaultFileB():
    filenameB = '..\..\dataset\words2.csv'
    return filenameB

def defaultColumn():
    columnName = 'word'
    return columnName

def defaultDateColumn():
    columnName = 'date'
    return columnName

def getConfigInfo():
    return True

def cmdUI():
    headerOutput()

    while True:  # part of do while loop
        # fail_condition = False #part of do while loop
        try:
            option = int(input("1:file 2:Spacy 0:exit >>"))
        except:
            print("invalid option!")
        if option == 1: #file
            try:
                fileOption = int(input("1:default_file 2:A_file 3:B_file 0:exit >>"))
            except:
                print("invalid option!")
            if fileOption == 1:
                filenameA = defaultFileA()
                filenameB = defaultFileB()
                read = spacyNLP.readFile(filenameA)
                df = pd.DataFrame(read, columns=['word', 'date'])  # impt to match columns
                read2 = spacyNLP.readFile(filenameB)
                df2 = pd.DataFrame(read2, columns=['word', 'date'])  # impt to match columns
            if fileOption == 2:
                try:
                    filenameA = input("enter file A location >>")
                    read = spacyNLP.readFile(filenameA)
                    df = pd.DataFrame(read, columns=['word', 'date'])  # impt to match columns
                except:
                    print("invalid file name or location!")
            if fileOption == 3:
                try:
                    filenameB = input("enter file location >>")
                    read = spacyNLP.readFile(filenameB)
                    df2 = pd.DataFrame(read, columns=['word', 'date'])  # impt to match columns
                except:
                    print("invalid file name or location!")
        if option == 2:
            while True:
                try:
                    spacyOption = int(input("1:display 2:token 3:Part_Of_Speech 4:label 5:sort 6:venn 0:exit >>"))
                except:
                    print("invalid option!")
                if spacyOption == 1:
                    if not df.empty:
                        print(df,end='\n end of fileA \n')
                    if not df2.empty:
                        print(df2,end='\n end of fileB \n')
                if spacyOption == 2:
                    columnName = ""
                    while True:
                        try:
                            tokenOption = int(input("1:both 2:file_A 3:file_B 4:column 0:exit >>"))
                        except:
                            print("invalid option!")
                        if tokenOption == 4:
                            columnOption = int(input("1:default 2:set_column 0:exit >>"))
                            if columnOption == 1:
                                columnName = defaultColumn()
                            if columnOption == 2:
                                columnName = input("enter column >>")
                            if columnOption == 0:  # part of do while loop
                                break
                        else:
                            if columnName == "":
                                columnName = defaultColumn()
                        if tokenOption == 1:
                            df = spacyNLP.spacyToken(df,columnName)
                            df2 = spacyNLP.spacyToken(df2,columnName)
                            break
                        if tokenOption == 2:
                            df = spacyNLP.spacyToken(df,columnName)
                            break
                        if tokenOption == 3:
                            df2 = spacyNLP.spacyToken(df2,columnName)
                            break
                        if tokenOption == 0:  # part of do while loop
                            break
                if spacyOption == 3:
                    columnName = ""
                    while True:
                        try:
                            POSOption = int(input("1:both 2:file_A 3:file_B 4:column 0:exit >>"))
                        except:
                            print("invalid option!")
                        if POSOption == 4:
                            columnOption = int(input("1:default 2:set_column 0:exit >>"))
                            if columnOption == 1:
                                columnName = defaultColumn()
                            if columnOption == 2:
                                columnName = input("enter column >>")
                            if columnOption == 0:  # part of do while loop
                                break
                        else:
                            if columnName == "":
                                columnName = defaultColumn()
                        if POSOption == 1:
                            df = spacyNLP.spacyPOSToken(df, columnName)
                            df2 = spacyNLP.spacyPOSToken(df2, columnName)
                            break
                        if POSOption == 2:
                            df = spacyNLP.spacyPOSToken(df, columnName)
                            break
                        if POSOption == 3:
                            df2 = spacyNLP.spacyPOSToken(df2, columnName)
                            break
                        if POSOption == 0:  # part of do while loop
                            break
                if spacyOption == 4:
                    columnName = ""
                    while True:
                        try:
                            LabelOption = int(input("1:both 2:file_A 3:file_B 4:column 0:exit >>"))
                        except:
                            print("invalid option!")
                        if LabelOption == 4:
                            columnOption = int(input("1:default 2:set_column 0:exit >>"))
                            if columnOption == 1:
                                columnName = defaultColumn()
                            if columnOption == 2:
                                columnName = input("enter column: ")
                            if columnOption == 0:  # part of do while loop
                                break
                        else:
                            if columnName == "":
                                columnName = defaultColumn()
                        if LabelOption == 1:
                            df = spacyNLP.spacyLabelToken(df, columnName)
                            df2 = spacyNLP.spacyLabelToken(df2, columnName)
                            break
                        if LabelOption == 2:
                            df = spacyNLP.spacyLabelToken(df, columnName)
                            break
                        if LabelOption == 3:
                            df2 = spacyNLP.spacyLabelToken(df2, columnName)
                            break
                        if LabelOption == 0:  # part of do while loop
                            break
                if spacyOption == 5:
                    columnName = ""
                    while True:
                        try:
                            sortOption = int(input("1:sort_by_date_range 2:sort_by_column 3:reindex 4:upLowCase 0:exit >>"))
                        except:
                            print("invalid option!")
                        if sortOption == 1:
                            while True:
                                try:
                                    dateOption = int(input("1:both 2:file_A 3:file_B 0:exit >>"))
                                except:
                                    print("invalid option!")
                                if dateOption == 1:
                                    columnName = defaultDateColumn()
                                    dateStart = input("file_A start date >>")
                                    dateEnd = input("file_A end date >>")
                                    df = sort.sortByDateRange(df, columnName, dateStart, dateEnd)
                                    # print(df, end='\n end of fileA after sort by date range\n')
                                    dateStart = input("file_B start date >>")
                                    dateEnd = input("file_B end date >>")
                                    df2 = sort.sortByDateRange(df2, columnName, dateStart, dateEnd)
                                    # print(df2, end='\n end of fileB after sort by date range\n')
                                    break
                                if dateOption == 2:
                                    dateStart = input("file_A start date >>")
                                    dateEnd = input("file_A end date >>")
                                    columnName = defaultDateColumn()
                                    df = sort.sortByDateRange(df, columnName, dateStart, dateEnd)
                                    # print(df, end='\n end of fileA after sort by date range\n')
                                    break
                                if dateOption == 3:
                                    dateStart = input("file_B start date >>")
                                    dateEnd = input("file_B end date >>")
                                    columnName = defaultDateColumn()
                                    df2 = sort.sortByDateRange(df2, columnName, dateStart, dateEnd)
                                    # print(df2, end='\n end of fileB after sort by date range\n')
                                    break
                                if dateOption == 0:
                                    break
                        if sortOption == 2:
                            columnName = ""
                            while True:
                                try:
                                    sortColumnOption = int(input("1:both 2:file_A 3:file_B 4:column 0:exit >>"))
                                except:
                                    print("invalid option!")
                                if sortColumnOption == 4:
                                    columnOption = int(input("1:default 2:set_column 0:exit >>"))
                                    if columnOption == 1:
                                        columnName = defaultColumn()
                                    if columnOption == 2:
                                        columnName = input("enter column >>")
                                    if columnOption == 0:  # part of do while loop
                                        break
                                else:
                                    if columnName == "":
                                        columnName = defaultColumn()
                                if sortColumnOption == 1:
                                    df = sort.sortBy(df,columnName)
                                    df2 = sort.sortBy(df2,columnName)
                                if sortColumnOption == 2:
                                    df = sort.sortBy(df,columnName)
                                if sortColumnOption == 3:
                                    df2 = sort.sortBy(df2,columnName)
                                if sortColumnOption == 0:
                                    break
                        if sortOption == 3:
                            columnName = ""
                            while True:
                                try:
                                    reindexOption = int(input("1:both 2:file_A 3:file_B 4:column 0:exit >>"))
                                except:
                                    print("invalid option!")
                                if reindexOption == 4:
                                    columnOption = int(input("1:default 2:set_column 0:exit >>"))
                                    if columnOption == 1:
                                        columnName = defaultColumn()
                                    if columnOption == 2:
                                        columnName = input("enter column >>")
                                    if columnOption == 0:  # part of do while loop
                                        break
                                else:
                                    if columnName == "":
                                        columnName = defaultColumn()
                                if reindexOption == 1:
                                    df = sort.reindex(df, columnName)
                                    df2 = sort.reindex(df2, columnName)
                                    break
                                if reindexOption == 2:
                                    df = sort.reindex(df, columnName)
                                    break
                                if reindexOption == 3:
                                    df2 = sort.reindex(df2, columnName)
                                    break
                                if reindexOption == 0:
                                    break
                        if sortOption == 4:
                            columnName = ""
                            while True:
                                try:
                                    caseOption = int(input("1:both 2:file_A 3:file_B 4:column 0:exit >>"))
                                except:
                                    print("invalid option!")
                                if caseOption == 4:
                                    columnOption = int(input("1:default 2:set_column 0:exit >>"))
                                    if columnOption == 1:
                                        columnName = defaultColumn()
                                    if columnOption == 2:
                                        columnName = input("enter column >>")
                                    if columnOption == 0:  # part of do while loop
                                        break
                                else:
                                    if columnName == "":
                                        columnName = defaultColumn()
                                if caseOption == 1:
                                    df = sort.caseFile(df, columnName)
                                    df2 = sort.caseFile(df2, columnName)
                                    break
                                if caseOption == 2:
                                    df = sort.caseFile(df, columnName)
                                    break
                                if caseOption == 3:
                                    df2 = sort.caseFile(df2, columnName)
                                    break
                                if caseOption == 0:
                                    break
                        if sortOption == 0:  # part of do while loop
                            break
                if spacyOption == 6:
                    columnName = columnNameB = ""
                    while True:
                        try:
                            vennOption = int(
                                input("1:Intersect_Unique 2:Intersect 3:SymmetricDif_Unique 4:SymmetricDif"
                                      " 5:Union 6:column 0:exit >>"))
                        except:
                            print("invalid option!")
                        if vennOption == 6:
                            columnOption = int(input("1:default 2:set_column 0:exit >>"))
                            if columnOption == 1:
                                columnName = defaultColumn()
                                columnNameB = defaultColumn()
                            if columnOption == 2:
                                columnName = input("file_A enter column >>")
                                columnNameB = input("file_B enter column >>")
                            if columnOption == 0:  # part of do while loop
                                break
                        if vennOption == 1:
                            venn.vennUniqueIntersect(df,columnName,df2,columnNameB)
                            break
                        if vennOption == 2:
                            venn.vennIntersect(df,columnName,df2,columnNameB)
                            break
                        if vennOption == 3:
                            venn.vennUniqueSymmetricDif(df,columnName,df,columnNameB)
                            break
                        if vennOption == 4:
                            venn.vennSymmetricDif(df,columnName,df2,columnNameB)
                            break
                        if vennOption == 5:
                            df = venn.vennUnion(df,df2)
                            del df2
                            df2 = pd.DataFrame()
                            break
                if spacyOption == 0:  # part of do while loop
                    break

        if option == 0:  # part of do while loop
            break


cmdUI()
