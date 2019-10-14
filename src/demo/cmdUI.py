import sys
import src.demo.spacyNLP as spacyNLP
import src.demo.sort as sort
import src.demo.venn as venn
import src.demo.defaults as default
import src.demo.description as des
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")


def headerOutput():
    print("No Preference - Profiler, cmd line user input")


def getConfigInfo():  # whats this for again???
    return True


def cmdUI():
    headerOutput()

    while True:  # part of do while loop
        # fail_condition = False #part of do while loop
        try:
            option = int(input("1:file 2:Spacy 3:description 0:exit >>"))
        except:
            print("invalid option!")
        if option == 1:  # file
            try:
                fileOption = int(input("1:default_file 2:A_file 3:B_file 0:exit >>"))
            except:
                print("invalid option!")
            des.desReadFile()
            if fileOption == 1:
                print("file_A:" + default.defaultFileA() + ", file_B:" + default.defaultFileB())
                filenameA = default.defaultFileA()
                filenameB = default.defaultFileB()
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
                    spacyOption = int(input("1:display 2:token 3:Part_Of_Speech 4:label 5:sort 6:venn"
                                            " 7:clean_[] 0:exit >>"))
                except:
                    print("invalid option!")
                if spacyOption == 1:
                    des.desDisplay()
                    if not df.empty:
                        print(df, end='\n end of fileA \n')
                    if not df2.empty:
                        print(df2, end='\n end of fileB \n')
                if spacyOption == 2:
                    des.desToken()
                    columnName = ""
                    while True:
                        try:
                            tokenOption = int(input("1:both 2:file_A 3:file_B 4:column 0:exit >>"))
                        except:
                            print("invalid option!")
                        if tokenOption == 4:
                            columnOption = int(input("1:default 2:set_column 0:exit >>"))
                            if columnOption == 1:
                                columnName = default.defaultColumn()
                            if columnOption == 2:
                                columnName = input("enter column >>")
                            if columnOption == 0:  # part of do while loop
                                break
                        else:
                            if columnName == "":
                                columnName = default.defaultColumn()
                        if tokenOption == 1:
                            df = spacyNLP.spacyToken(df, columnName)
                            df2 = spacyNLP.spacyToken(df2, columnName)
                            break
                        if tokenOption == 2:
                            df = spacyNLP.spacyToken(df, columnName)
                            break
                        if tokenOption == 3:
                            df2 = spacyNLP.spacyToken(df2, columnName)
                            break
                        if tokenOption == 0:  # part of do while loop
                            break
                if spacyOption == 3:
                    des.desPOS()
                    columnName = ""
                    while True:
                        try:
                            POSOption = int(input("1:both 2:file_A 3:file_B 4:column 0:exit >>"))
                        except:
                            print("invalid option!")
                        if POSOption == 4:
                            columnOption = int(input("1:default 2:set_column 0:exit >>"))
                            if columnOption == 1:
                                columnName = default.defaultColumn()
                            if columnOption == 2:
                                columnName = input("enter column >>")
                            if columnOption == 0:  # part of do while loop
                                break
                        else:
                            if columnName == "":
                                columnName = default.defaultColumn()
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
                    des.desLabel()
                    columnName = ""
                    while True:
                        try:
                            LabelOption = int(input("1:both 2:file_A 3:file_B 4:column 0:exit >>"))
                        except:
                            print("invalid option!")
                        if LabelOption == 4:
                            columnOption = int(input("1:default 2:set_column 0:exit >>"))
                            if columnOption == 1:
                                columnName = default.defaultColumn()
                            if columnOption == 2:
                                columnName = input("enter column: ")
                            if columnOption == 0:  # part of do while loop
                                break
                        else:
                            if columnName == "":
                                columnName = default.defaultColumn()
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
                    des.desSort()
                    columnName = ""
                    while True:
                        try:
                            sortOption = int(
                                input("1:sort_by_date_range 2:sort_by_column 3:reindex 4:upLowCase 0:exit >>"))
                        except:
                            print("invalid option!")
                        if sortOption == 1:
                            while True:
                                try:
                                    dateOption = int(input("1:both 2:file_A 3:file_B 0:exit >>"))
                                except:
                                    print("invalid option!")
                                if dateOption == 1:
                                    columnName = default.defaultDateColumn()
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
                                    columnName = default.defaultDateColumn()
                                    df = sort.sortByDateRange(df, columnName, dateStart, dateEnd)
                                    # print(df, end='\n end of fileA after sort by date range\n')
                                    break
                                if dateOption == 3:
                                    dateStart = input("file_B start date >>")
                                    dateEnd = input("file_B end date >>")
                                    columnName = default.defaultDateColumn()
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
                                        columnName = default.defaultColumn()
                                    if columnOption == 2:
                                        columnName = input("enter column >>")
                                    if columnOption == 0:  # part of do while loop
                                        break
                                else:
                                    if columnName == "":
                                        columnName = default.defaultColumn()

                                if sortColumnOption == 1:
                                    df = sort.sortBy(df, columnName)
                                    df2 = sort.sortBy(df2, columnName)
                                    break
                                if sortColumnOption == 2:
                                    df = sort.sortBy(df, columnName)
                                    break
                                if sortColumnOption == 3:
                                    df2 = sort.sortBy(df2, columnName)
                                    break
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
                                        columnName = default.defaultColumn()
                                    if columnOption == 2:
                                        columnName = input("enter column >>")
                                    if columnOption == 0:  # part of do while loop
                                        break
                                else:
                                    if columnName == "":
                                        columnName = default.defaultColumn()
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
                            upperlower = "lower"
                            while True:
                                try:
                                    caseOption = int(input("1:both 2:file_A 3:file_B 4:ChangeTo:"
                                                           ""+ upperlower +" 0:exit >>"))
                                except:
                                    print("invalid option!")
                                # if caseOption == 4:
                                #     columnOption = int(input("1:default 2:set_column 0:exit >>"))
                                #     if columnOption == 1:
                                #         columnName = default.defaultColumn()
                                #     if columnOption == 2:
                                #         columnName = input("enter column >>")
                                #     if columnOption == 0:  # part of do while loop
                                #         break
                                if(caseOption == 4):
                                    if upperlower == "lower":
                                        upperlower = "upper"
                                    else:
                                        upperlower = "lower"
                                if caseOption == 1:
                                    df = sort.caseFile(df, upperlower)
                                    df2 = sort.caseFile(df2, upperlower)
                                    break
                                if caseOption == 2:
                                    df = sort.caseFile(df, upperlower)
                                    break
                                if caseOption == 3:
                                    df2 = sort.caseFile(df2, upperlower)
                                    break
                                if caseOption == 0:
                                    break
                        if sortOption == 0:  # part of do while loop
                            break
                if spacyOption == 6:
                    des.desVenn()
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
                                columnName = default.defaultColumn()
                                columnNameB = default.defaultColumn()
                            if columnOption == 2:
                                columnName = input("file_A enter column >>")
                                columnNameB = input("file_B enter column >>")
                            if columnOption == 0:  # part of do while loop
                                break
                        else:
                            if columnName == "":
                                columnName = default.defaultColumn()
                            if columnNameB == "":
                                columnNameB = default.defaultColumn()
                        if vennOption == 1:
                            venn.vennUniqueIntersect(df, columnName, df2, columnNameB)
                            break
                        if vennOption == 2:
                            venn.vennIntersect(df, columnName, df2, columnNameB)
                            break
                        if vennOption == 3:
                            venn.vennUniqueSymmetricDif(df, columnName, df, columnNameB)
                            break
                        if vennOption == 4:
                            venn.vennSymmetricDif(df, columnName, df2, columnNameB)
                            break
                        if vennOption == 5:
                            df = venn.vennUnion(df, df2)
                            del df2
                            df2 = pd.DataFrame()
                            break
                        if vennOption == 0:
                            break
                if spacyOption == 7:
                    des.desClean()
                    columnName = columnNameB = ""
                    while True:
                        try:
                            cleanOption = int(
                                input("1:both 2:file_A 3:file_B 4:column 0:exit >>"))
                        except:
                            print("invalid option!")
                        if cleanOption == 4:
                            columnOption = int(input("1:default 2:set_column 0:exit >>"))
                            if columnOption == 1:
                                columnName = default.defaultColumn()
                                columnNameB = default.defaultColumn()
                            if columnOption == 2:
                                columnName = input("file_A enter column >>")
                                columnNameB = input("file_B enter column >>")
                            if columnOption == 0:  # part of do while loop
                                break
                        else:
                            if columnName == "":
                                columnName = default.defaultColumn()
                            if columnNameB == "":
                                columnNameB = default.defaultColumn()
                        if cleanOption == 1:
                            if not df.empty:
                                spacyNLP.spacyCleanCell(df, columnName)
                            if not df2.empty:
                                spacyNLP.spacyCleanCell(df2, columnNameB)
                            break
                        if cleanOption == 2:
                            if not df.empty:
                                spacyNLP.spacyCleanCell(df, columnName)
                            break
                        if cleanOption == 3:
                            if not df2.empty:
                                spacyNLP.spacyCleanCell(df2, columnNameB)
                            break
                        if cleanOption == 0:
                            break
                if spacyOption == 0:  # part of do while loop
                    break
        if option == 3:
            des.desINFO()
            des.getState()
            try:
                desOption = int(input("1:check 2:toggle 0:exit >>"))
            except:
                print("invalid option!")
            if desOption == 1:
                print(des.getState())
            if desOption == 2:
                des.toggleState()
            if desOption == 0:
                break
        if option == 0:  # part of do while loop
            break


cmdUI()
