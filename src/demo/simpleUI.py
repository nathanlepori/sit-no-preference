import src.demo.spacyNLP as spacyNLP
import src.demo.sort as sort
import src.demo.venn as venn
import src.demo.defaults as default
import src.demo.description as des
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")


def selectFile():
    fileOption = int(input("1:default_file 2:A_file 3:B_file 0:exit >>"))
    des.desReadFile()
    if fileOption == 1:
        print("file_A:" + default.defaultFileA() + ", file_B:" + default.defaultFileB())
        filenameA = default.defaultFileA()
        filenameB = default.defaultFileB()
        read = spacyNLP.readFile(filenameA)
        df = pd.DataFrame(read, columns=[default.defaultColumn(), default.defaultDateColumn()])  # impt to match columns
        read2 = spacyNLP.readFile(filenameB)
        df2 = pd.DataFrame(read2,
                           columns=[default.defaultColumn(), default.defaultDateColumn()])  # impt to match columns
    if fileOption == 2:
        try:
            filenameA = input("enter file A location >>")
            read = spacyNLP.readFile(filenameA)
            df = pd.DataFrame(read,
                              columns=[default.defaultColumn(), default.defaultDateColumn()])  # impt to match columns
        except:
            print("invalid file name or location!")
    if fileOption == 3:
        try:
            filenameB = input("enter file location >>")
            read2 = spacyNLP.readFile(filenameB)
            df2 = pd.DataFrame(read2,
                               columns=[default.defaultColumn(), default.defaultDateColumn()])  # impt to match columns
        except:
            print("invalid file name or location!")
    return df, df2

def displayDataframe(df,df2):
    if not df.empty:
        print(df, end='\n end of fileA \n')
    if not df2.empty:
        print(df2, end='\n end of fileB \n')

def simpleSortByDateRange(df,df2,columnName,columnNameB):
    # dateStart = input("file_A start date >>")
    # dateEnd = input("file_A end date >>")
    dateStart = '10/6/2019' #testing
    dateEnd = '11/6/2019' #testing
    print(dateStart,dateEnd)
    df = sort.sortByDateRange(df, columnName, dateStart, dateEnd)
    # dateStart = input("file_B start date >>")
    # dateEnd = input("file_B end date >>")
    dateStart = '10/6/2019' #testing
    dateEnd = '11/6/2019' #testing
    print(dateStart, dateEnd)

    df2 = sort.sortByDateRange(df2, columnNameB, dateStart, dateEnd)
    return df,df2


def simpleUI():
    while True:  # part of do while loop
        # fail_condition = False #part of do while loop
        try:
            select = int(input("POS 1:Intersect 2:SymDif 3:Union \n"
                               "Label 4:Intersect 5:SymDif 6:Union \n"
                               "Browser 7:POS Intersect 8:label Intersect \n"
                               "Social 9:POS Intersect 10:label Intersect \n"
                               "11:save 0:exit >>"))
            columnName = columnNameB = default.defaultColumn()
            if select == 1:
                df, df2 = selectFile()
                dateColumnA = dateColumnB = default.defaultDateColumn()
                simpleSortByDateRange(df,df2,dateColumnA,dateColumnB)
                spacyNLP.spacyToken(df, columnName)
                spacyNLP.spacyToken(df2, columnNameB)
                spacyNLP.spacyStopword(df,columnName)
                spacyNLP.spacyStopword(df2,columnNameB)
                spacyNLP.spacyPOSToken(df, columnName)
                spacyNLP.spacyPOSToken(df2, columnNameB)
                venn.vennIntersect(df, columnName, df2, columnNameB)
                spacyNLP.spacyCleanCell(df,columnName)
                spacyNLP.spacyCleanCell(df2,columnNameB)
            if select == 2:
                df, df2 = selectFile()
                dateColumnA = dateColumnB = default.defaultDateColumn()
                simpleSortByDateRange(df, df2, dateColumnA, dateColumnB)
                spacyNLP.spacyToken(df, columnName)
                spacyNLP.spacyToken(df2, columnNameB)
                spacyNLP.spacyStopword(df, columnName)
                spacyNLP.spacyStopword(df2, columnNameB)
                spacyNLP.spacyPOSToken(df, columnName)
                spacyNLP.spacyPOSToken(df2, columnNameB)
                venn.vennSymmetricDif(df, columnName, df2, columnNameB)
                spacyNLP.spacyCleanCell(df, columnName)
                spacyNLP.spacyCleanCell(df2, columnNameB)
            if select == 3:
                df, df2 = selectFile()
                dateColumnA = dateColumnB = default.defaultDateColumn()
                simpleSortByDateRange(df, df2, dateColumnA, dateColumnB)
                spacyNLP.spacyToken(df, columnName)
                spacyNLP.spacyToken(df2, columnNameB)
                spacyNLP.spacyStopword(df, columnName)
                spacyNLP.spacyStopword(df2, columnNameB)
                spacyNLP.spacyPOSToken(df, columnName)
                spacyNLP.spacyPOSToken(df2, columnNameB)
                df = venn.vennUnion(df, df2)
                del df2
                df2 = pd.DataFrame
                # spacyNLP.spacyCleanCell(df, columnName)
                # spacyNLP.spacyCleanCell(df2, columnNameB)
            if select == 4:
                df, df2 = selectFile()
                dateColumnA = dateColumnB = default.defaultDateColumn()
                simpleSortByDateRange(df,df2,dateColumnA,dateColumnB)
                spacyNLP.spacyToken(df, columnName)
                spacyNLP.spacyToken(df2, columnNameB)
                spacyNLP.spacyStopword(df,columnName)
                spacyNLP.spacyStopword(df2,columnNameB)
                spacyNLP.spacyLabelToken(df, columnName)
                spacyNLP.spacyLabelToken(df2, columnNameB)
                venn.vennIntersect(df, columnName, df2, columnNameB)
                spacyNLP.spacyCleanCell(df,columnName)
                spacyNLP.spacyCleanCell(df2,columnNameB)
            if select == 5:
                df, df2 = selectFile()
                dateColumnA = dateColumnB = default.defaultDateColumn()
                simpleSortByDateRange(df, df2, dateColumnA, dateColumnB)
                spacyNLP.spacyToken(df, columnName)
                spacyNLP.spacyToken(df2, columnNameB)
                spacyNLP.spacyStopword(df, columnName)
                spacyNLP.spacyStopword(df2, columnNameB)
                spacyNLP.spacyLabelToken(df, columnName)
                spacyNLP.spacyLabelToken(df2, columnNameB)
                venn.vennSymmetricDif(df, columnName, df2, columnNameB)
                spacyNLP.spacyCleanCell(df, columnName)
                spacyNLP.spacyCleanCell(df2, columnNameB)
            if select == 6:
                df, df2 = selectFile()
                dateColumnA = dateColumnB = default.defaultDateColumn()
                simpleSortByDateRange(df, df2, dateColumnA, dateColumnB)
                spacyNLP.spacyToken(df, columnName)
                spacyNLP.spacyToken(df2, columnNameB)
                spacyNLP.spacyStopword(df, columnName)
                spacyNLP.spacyStopword(df2, columnNameB)
                spacyNLP.spacyLabelToken(df, columnName)
                spacyNLP.spacyLabelToken(df2, columnNameB)
                df = venn.vennUnion(df, df2)
                del df2
                df2 = pd.DataFrame
                # spacyNLP.spacyCleanCell(df, columnName)
                # spacyNLP.spacyCleanCell(df2, columnNameB)
            if select == 11:
                writeOption = int(input("1:file_A 2:file_B 0:exit >>"))
                if writeOption == 1:
                    newFileName = input("save file_A as >>")
                    # writeToNewFile(df, newFileName)
                    df.to_csv(newFileName)
                if writeOption == 2:
                    newFileName = input("save file_B as >>")
                    # writeToNewFile(df2, newFileName)
                    df2.to_csv(newFileName)
            if select == 0:
                break
            displayDataframe(df,df2)
        except:
            print("invalid option!")

simpleUI()