import sys
import no_preference.demo.spacyNLP as spacyNLP
import no_preference.demo.sort as sort
import no_preference.demo.venn as venn
import no_preference.demo.defaults as default
import no_preference.demo.description as des
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

"""Zhengyi's to do list
DONE?
no    A. make clear stopword based on tokenized and non tokenized verison of dataframe into cmdUI
YES    B. write dataframe to csv file
no    C. add to 1:file 2:Spacy 3:description [4:fixed_processing] 0:exit that will have a list of options that will do the following:
            1st example: tokenize A&B > POS/Label > stopword > write
            2nd example: tokenize A&B > POS/Label > stopword > venn intersect > write
            3rd example: tokenize A&B > POS/Label > stopword > request filter or strip > request venn type > write
            4th example ..... continue for all different types we can come up with.
no    D. Currently venn will over write both dataframe:
            make it such that it only over write by file indication????
                reasons:
                        seems no point user can just redo?
                            instead find a way to highlight intersected words in the whole of browser history, to see what VV
                                >> browser history eventually was posted on their social media. Vice versa 
                                    for now by this calculation should have the following types of graphs, minimal
                                        1[pos>inter] 2[pos>symDif] 3[label>inter] 4[label>symdif] 5[pos>union] 6[label>union]
                                        [all 6 of previous graph > sort > filter/strip] = 1 type of graph that depends on input
                                            for a total of 7 for now.
                                        8[pos>inter>keep whole of file_A and highlight intersect words] 9[same as 8 but for label]
                                        point 8 and 9 copy paste for B instead for point 10 and 11.
                                            this will show what browser history was eventually reflected into social media.
                                        Total 11 types of graphs for now.
                                            Convert all these types into fixed_processing as indicated in Point C.
                                        
                                        following not sure should be graph (basically uniq type)
                                            [pos>uniqInter][pos>uniqSymdif][pos>unionUniq][label>uniqInter][label>uniqSymdif][label>unionUniq]
                                            
                                            
                                        as a result might wanna ask which dataframe to overwrite instead of (now just overwrite both df)
                                                add a column say posted? dont make sense as tokenized is done per sentence:row not per word:row
                                                UPPER case vs lower case to indicate posted or not?? seems best for now.   
YES    E. move 8:clean into 7:filtering???
no    F. add a /t to (after selection an option in 1:file 2:Spacy 3:description 0:exit.) in its display of options.
no    G. reformat to python naming convention?
no    H. replace all column option selection to a function (as its all a duplicate). just need return 2 values for columnName and columnNameB
no    I. look for coding errors eg wrong variables used etc.
no    J. do a history to show what have been done to each dataframe eg file_A: token > POS > sort > venn. 
            which changes based on what have been done to the dataframe.
      K. 
no    ?? proper GUI ?? if yes who to do?
    
"""

def headerOutput():
    print("No Preference - Profiler, cmd line user input")


def writeToNewFile(writeContent,newFileName):
    newFile = open(newFileName+'.csv', "w+")
    newFile.write(str(writeContent))
    newFile.close()

def selectColumn(columnName,columnNameB):
    columnOption = int(input("1:default 2:set_column 0:exit >>"))
    if columnOption == 1:
        columnName = default.defaultColumn()
        columnNameB = default.defaultColumn()
    if columnOption == 2:
        columnName = input("file_A enter column >>")
        columnNameB = input("file_B enter column >>")
    return columnName,columnNameB

def cmdUI():
    headerOutput()

    while True:  # part of do while loop
        # fail_condition = False #part of do while loop
        try:
            option = int(input("1:file 2:Spacy 3:description 0:exit >>"))
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
                    df = pd.DataFrame(read, columns=[default.defaultColumn(),default.defaultDateColumn()])  # impt to match columns
                    read2 = spacyNLP.readFile(filenameB)
                    df2 = pd.DataFrame(read2, columns=[default.defaultColumn(),default.defaultDateColumn()])  # impt to match columns
                if fileOption == 2:
                    try:
                        filenameA = input("enter file A location >>")
                        read = spacyNLP.readFile(filenameA)
                        df = pd.DataFrame(read, columns=[default.defaultColumn(),default.defaultDateColumn()])  # impt to match columns
                    except:
                        print("invalid file name or location!")
                if fileOption == 3:
                    try:
                        filenameB = input("enter file location >>")
                        read2 = spacyNLP.readFile(filenameB)
                        df2 = pd.DataFrame(read2, columns=[default.defaultColumn(),default.defaultDateColumn()])  # impt to match columns
                    except:
                        print("invalid file name or location!")
            if option == 2:
                while True:
                    try:
                        spacyOption = int(input("1:display 2:token 3:Part_Of_Speech 4:label 5:sort 6:venn"
                                                " 7:filtering 8:save 0:exit >>"))
                        if spacyOption == 1:
                            des.desDisplay()
                            if not df.empty:
                                print(df, end='\n end of fileA \n')
                            if not df2.empty:
                                print(df2, end='\n end of fileB \n')
                        if spacyOption == 2:
                            des.desToken()
                            columnName = columnNameB = default.defaultColumn()
                            while True:
                                try:
                                    tokenOption = int(input("1:both 2:file_A 3:file_B 4:column"+"[A:"+columnName+",B:"+columnNameB+"] 0:exit >>"))
                                    if tokenOption == 4:
                                        columnName,columnNameB = selectColumn(columnName,columnNameB)
                                    if tokenOption == 1:
                                        df = spacyNLP.spacyToken(df, columnName)
                                        df2 = spacyNLP.spacyToken(df2, columnNameB)
                                        break
                                    if tokenOption == 2:
                                        df = spacyNLP.spacyToken(df, columnName)
                                        break
                                    if tokenOption == 3:
                                        df2 = spacyNLP.spacyToken(df2, columnNameB)
                                        break
                                    if tokenOption == 0:  # part of do while loop
                                        break
                                except:
                                    print("invalid option!")
                        if spacyOption == 3:
                            des.desPOS()
                            columnName = columnNameB = default.defaultColumn()
                            while True:
                                try:
                                    POSOption = int(input("1:both 2:file_A 3:file_B 4:column"+"[A:"+columnName+",B:"+columnNameB+"] 0:exit >>"))
                                    if POSOption == 4:
                                        columnName,columnNameB = selectColumn(columnName,columnNameB)
                                    if POSOption == 1:
                                        df = spacyNLP.spacyPOSToken(df, columnName)
                                        df2 = spacyNLP.spacyPOSToken(df2, columnNameB)
                                        break
                                    if POSOption == 2:
                                        df = spacyNLP.spacyPOSToken(df, columnName)
                                        break
                                    if POSOption == 3:
                                        df2 = spacyNLP.spacyPOSToken(df2, columnNameB)
                                        break
                                    if POSOption == 0:  # part of do while loop
                                        break
                                except:
                                    print("invalid option!")
                        if spacyOption == 4:
                            des.desLabel()
                            columnName = columnNameB = default.defaultColumn()
                            while True:
                                try:
                                    LabelOption = int(input("1:both 2:file_A 3:file_B 4:column"+"[A:"+columnName+",B:"+columnNameB+"] 0:exit >>"))
                                    if LabelOption == 4:
                                        columnName,columnNameB = selectColumn(columnName,columnNameB)
                                    if LabelOption == 1:
                                        df = spacyNLP.spacyLabelToken(df, columnName)
                                        df2 = spacyNLP.spacyLabelToken(df2, columnNameB)
                                        break
                                    if LabelOption == 2:
                                        df = spacyNLP.spacyLabelToken(df, columnName)
                                        break
                                    if LabelOption == 3:
                                        df2 = spacyNLP.spacyLabelToken(df2, columnNameB)
                                        break
                                    if LabelOption == 0:  # part of do while loop
                                        break
                                except:
                                    print("invalid option!")
                        if spacyOption == 5:
                            des.desSort()
                            columnName = columnNameB = default.defaultDateColumn()
                            while True:
                                try:
                                    sortOption = int(
                                        input("1:sort_by_date_range 2:sort_by_column 3:reindex 4:upLowCase 0:exit >>"))
                                    if sortOption == 1:
                                        while True:
                                            try:
                                                dateOption = int(input("1:both 2:file_A 3:file_B 0:exit >>"))
                                                if dateOption == 1:
                                                    dateStart = input("file_A start date >>")
                                                    dateEnd = input("file_A end date >>")
                                                    df = sort.sortByDateRange(df, columnName, dateStart, dateEnd)
                                                    # print(df, end='\n end of fileA after sort by date range\n')
                                                    dateStart = input("file_B start date >>")
                                                    dateEnd = input("file_B end date >>")
                                                    df2 = sort.sortByDateRange(df2, columnNameB, dateStart, dateEnd)
                                                    # print(df2, end='\n end of fileB after sort by date range\n')
                                                    break
                                                if dateOption == 2:
                                                    dateStart = input("file_A start date >>")
                                                    dateEnd = input("file_A end date >>")
                                                    df = sort.sortByDateRange(df, columnName, dateStart, dateEnd)
                                                    # print(df, end='\n end of fileA after sort by date range\n')
                                                    break
                                                if dateOption == 3:
                                                    dateStart = input("file_B start date >>")
                                                    dateEnd = input("file_B end date >>")
                                                    df2 = sort.sortByDateRange(df2, columnNameB, dateStart, dateEnd)
                                                    # print(df2, end='\n end of fileB after sort by date range\n')
                                                    break
                                                if dateOption == 0:
                                                    break
                                            except:
                                                print("invalid option!")
                                    if sortOption == 2:
                                        columnName = columnNameB = default.defaultDateColumn()
                                        while True:
                                            try:
                                                sortColumnOption = int(
                                                    input("1:both 2:file_A 3:file_B 4:column"+"[A:"+columnName+",B:"+columnNameB+"] 0:exit >>"))
                                            except:
                                                print("invalid option!")
                                            if sortColumnOption == 4:
                                                columnName, columnNameB = selectColumn(columnName, columnNameB)
                                            if sortColumnOption == 1:
                                                df = sort.sortBy(df, columnName)
                                                df2 = sort.sortBy(df2, columnNameB)
                                                break
                                            if sortColumnOption == 2:
                                                df = sort.sortBy(df, columnName)
                                                break
                                            if sortColumnOption == 3:
                                                df2 = sort.sortBy(df2, columnNameB)
                                                break
                                            if sortColumnOption == 0:
                                                break
                                    if sortOption == 3:
                                        while True:
                                            try:
                                                reindexOption = int(
                                                    input("1:both 2:file_A 3:file_B 0:exit >>"))
                                            except:
                                                print("invalid option!")
                                            if reindexOption == 1:
                                                df = sort.reindex(df)
                                                df2 = sort.reindex(df2)
                                                break
                                            if reindexOption == 2:
                                                df = sort.reindex(df)
                                                break
                                            if reindexOption == 3:
                                                df2 = sort.reindex(df2)
                                                break
                                            if reindexOption == 0:
                                                break
                                    if sortOption == 4:
                                        upperlower = "lower"
                                        while True:
                                            try:
                                                caseOption = int(input("1:both 2:file_A 3:file_B 4:ChangeTo:"
                                                                       "" + upperlower + " 0:exit >>"))
                                            except:
                                                print("invalid option!")
                                            if (caseOption == 4):
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
                                except:
                                    print("invalid option!")
                        if spacyOption == 6:
                            des.desVenn()
                            columnName = columnNameB = default.defaultColumn()
                            while True:
                                try:
                                    vennOption = int(
                                        input("1:Intersect_Unique 2:Intersect 3:SymmetricDif_Unique 4:SymmetricDif"
                                              " 5:Union 6:column"+"[A:"+columnName+",B:"+columnNameB+"] 0:exit >>"))
                                    if vennOption == 6:
                                        columnName,columnNameB = selectColumn(columnName,columnNameB)
                                    if vennOption == 1:
                                        venn.vennUniqueIntersect(df, columnName, df2, columnNameB)
                                        break
                                    if vennOption == 2:
                                        venn.vennIntersect(df, columnName, df2, columnNameB)
                                        break
                                    if vennOption == 3:
                                        venn.vennUniqueSymmetricDif(df, columnName, df2, columnNameB)
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
                                except:
                                    print("invalid option!")
                        if spacyOption == 7:
                            listNo = 0
                            value = ''
                            des.desFilter()
                            columnName = columnNameB = default.defaultColumn()
                            while True:
                                if listNo == 0:
                                    listType = "text"
                                elif listNo == 1:
                                    listType = "tag"
                                try:
                                    filteringOption = int(
                                        input(
                                            "1:filter 2:strip 3:set_value=[" + value + "] 4:column"+"[A:"+columnName+",B:"+columnNameB+"] 5:ChangeTo=[" + listType +
                                            "] 6:clean_[] 0:exit >>"))
                                    if filteringOption == 4:
                                        columnName,columnNameB = selectColumn(columnName,columnNameB)
                                    if filteringOption == 3:
                                        try:
                                            value = input("pleace enter value to filter >>")
                                        except:
                                            print("invalid value!")
                                    if filteringOption == 5:
                                        if listNo == 0:
                                            listNo = 1
                                        elif listNo == 1:
                                            listNo = 0
                                    if filteringOption == 1:
                                        while True:
                                            try:
                                                filterOption = int(input("1:both 2:file_A 3:file_B 0:exit >>"))
                                                if filterOption == 1:
                                                    spacyNLP.spacyColumnFilterToken(df, columnName, value, listNo)
                                                    spacyNLP.spacyColumnFilterToken(df2, columnNameB, value, listNo)
                                                    break
                                                if filterOption == 2:
                                                    spacyNLP.spacyColumnFilterToken(df, columnName, value, listNo)
                                                    break
                                                if filterOption == 3:
                                                    spacyNLP.spacyColumnFilterToken(df2, columnNameB, value, listNo)
                                                    break
                                                if filterOption == 0:
                                                    break
                                            except:
                                                print("invalid option!")
                                    if filteringOption == 2:
                                        while True:
                                            try:
                                                stripOption = int(input("1:both 2:file_A 3:file_B 0:exit >>"))
                                                if stripOption == 1:
                                                    spacyNLP.spacyColumnStripToken(df, columnName, value, listNo)
                                                    spacyNLP.spacyColumnStripToken(df2, columnNameB, value, listNo)
                                                    break
                                                if stripOption == 2:
                                                    spacyNLP.spacyColumnStripToken(df, columnName, value, listNo)
                                                    break
                                                if stripOption == 3:
                                                    spacyNLP.spacyColumnStripToken(df2, columnNameB, value, listNo)
                                                    break
                                                if stripOption == 0:
                                                    break
                                            except:
                                                print("invalid option!")
                                    if filteringOption == 6:
                                        # des.desClean()
                                        columnName = columnNameB = default.defaultDateColumn()
                                        while True:
                                            try:
                                                cleanOption = int(
                                                    input("1:both 2:file_A 3:file_B 4:column"+"[A:"+columnName+",B:"+columnNameB+"] 0:exit >>"))
                                                if cleanOption == 4:
                                                    columnName,columnNameB = selectColumn(columnName,columnNameB)
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
                                            except:
                                                print("invalid option!")
                                    if filteringOption == 0:
                                        break
                                except:
                                    print("invalid option!")
                        if spacyOption == 8:
                            while True:
                                try:
                                    writeOption = int(input("1:file_A 2:file_B 0:exit >>"))
                                    if writeOption == 1:
                                        newFileName = input("save file_A as >>")
                                        # writeToNewFile(df, newFileName)
                                        df.to_csv(newFileName)
                                        break
                                    if writeOption == 2:
                                        newFileName = input("save file_B as >>")
                                        # writeToNewFile(df2, newFileName)
                                        df2.to_csv(newFileName)
                                        break
                                    if writeOption == 0:
                                        break
                                except:
                                    print("invalid option!")

                        if spacyOption == 0:  # part of do while loop
                            break
                    except:
                        print("invalid option!")
            if option == 3:
                des.desINFO()
                des.getState()
                try:
                    desOption = int(input("1:check 2:toggle 0:exit >>"))
                    if desOption == 1:
                        print(des.getState())
                    if desOption == 2:
                        des.toggleState()
                    if desOption == 0:
                        break
                except:
                    print("invalid option!")

            if option == 0:  # part of do while loop
                break
        except:
            print("invalid option!")


cmdUI()
