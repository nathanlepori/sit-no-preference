import no_preference.demo.spacyNLP as spacyNLP
import no_preference.demo.sort as sort
import no_preference.demo.venn as venn
import no_preference.demo.defaults as default
import no_preference.demo.description as des
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


def writeFile(content, filename):
    f = open(filename, "w+")
    f.write(str(content))
    f.close()


def writeHTML(df, columnName, df2, columnNameB, intersect, filename):
    filename = filename + '.html'
    f = open(filename, "w+")
    f.write("<!DOCTYPE html><html><body><h2>Highlight Text in Profiler</h2>"
            "<style>div{colour: lightblue;}</style>"
            "<table style=\"width:100%\"><tr><th>Index</th><th>Date</th><th>Word</th></tr>")
    f.write('<p>' + str(intersect) + '</p>')
    f.write("<h3>file_A</h3>")
    Ai = index = 0
    for row in df[columnName]:
        Aj = 0
        f.write("<tr><td>" + str(index) + "</td>")
        f.write("<td>" + str(df.iloc[Ai][default.defaultDateColumn()]) + "</td>")
        index += 1
        for word in df.iloc[Ai][columnName]:
            if df.iloc[Ai][columnName][Aj] in intersect:
                f.write("<td><div>" + str(word) + "</div></td>")
            else:
                f.write("<td>" + str(word) + "</td>")
        f.write("</tr>")
        Ai += 1
    f.write("</table>"
            "<table style=\"width:100%\"><tr><th>Index</th><th>Date</th><th>Word</th></tr>"
            "<h3>file_B</h3>")
    Bi = index = 0
    for row in df2[columnNameB]:
        Bj = 0
        f.write("<tr><td>" + str(index) + "</td>")
        f.write("<td>" + str(df2.iloc[Bi][default.defaultDateColumn()]) + "</td>")
        index += 1
        for word in df2.iloc[Bi][columnNameB]:
            if df2.iloc[Bi][columnNameB][Bj] in intersect:
                f.write("<td><div>" + str(word) + "</div></td>")
            else:
                f.write("<td>" + str(word) + "</td>")
        f.write("</tr>")
        Bi += 1
    f.close()


def displayColorText(df, columnName, df2, columnNameB, intersect):
    print("\033[22;33m" + str(intersect) + "\033[m", end='\n')
    Ai = index = 0
    for row in df[columnName]:
        Aj = 0
        print()
        print(index, end=' ')
        index += 1
        print(df.iloc[Ai][default.defaultDateColumn()], end=' ')
        for word in df.iloc[Ai][columnName]:
            if df.iloc[Ai][columnName][Aj] in intersect:
                # pass
                # df.iloc[Ai][columnName][Aj] = ("\033[44;33m" + str(word) + "\033[m")
                print("\033[22;33m" + str(word) + "\033[m", end='')
            # Aj += 1
            else:
                print(word, end=' ')
        Ai += 1
    print()
    Bi = index = 0
    for row in df2[columnNameB]:
        Bj = 0
        print()
        print(index, end=' ')
        index += 1
        print(df2.iloc[Bi][default.defaultDateColumn()], end=' ')
        for word in df2.iloc[Bi][columnNameB]:
            if df2.iloc[Bi][columnNameB][Bj] in intersect:
                # pass
                # df.iloc[Ai][columnName][Aj] = ("\033[44;33m" + str(word) + "\033[m")
                print("\033[22;33m" + str(word) + "\033[m", end='')
            # Aj += 1
            else:
                print(word, end=' ')
        Bi += 1


def displayDataframe(df, df2):
    if not df.empty:
        print(df, end='\n end of fileA \n')
    if not df2.empty:
        print(df2, end='\n end of fileB \n')


def simpleSortByDateRange(df, df2, columnName, columnNameB):
    # dateStart = input("file_A start date >>")
    # dateEnd = input("file_A end date >>")
    dateStart = '10/6/2019'  # testing
    dateEnd = '11/6/2019'  # testing
    print(dateStart, dateEnd)
    df = sort.sortByDateRange(df, columnName, dateStart, dateEnd)
    # dateStart = input("file_B start date >>")
    # dateEnd = input("file_B end date >>")
    dateStart = '10/6/2019'  # testing
    dateEnd = '11/6/2019'  # testing
    print(dateStart, dateEnd)

    df2 = sort.sortByDateRange(df2, columnNameB, dateStart, dateEnd)
    return df, df2


def fraction(countA):
    totalValue = 0
    for key, value in countA.items():
        totalValue += value
    for mykey, value in countA.items():
        countA[mykey] = (value / totalValue)
    return countA


def writeCountAsFile(count, writeOption):
    if writeOption == 1:
        newFileName = input("save file_A's counter as >>")
    if writeOption == 2:
        newFileName = input("save file_B's counter as >>")
    writeFile(count, newFileName)


def assocTerm(df, columnName, termStruct, ached):
    i = 0
    if ached == 1:  # in detached form
        for row in df[columnName]:
            tempStruct = termStruct.copy()
            for word in df.iloc[i][columnName]:
                t = 0
                for element in tempStruct:
                    if tempStruct[t][1] == 'text':
                        listNo = 0
                    else:
                        listNo = 1
                    if word[listNo] == tempStruct[t][0]:  # if value match remove from list of struct to track
                        del tempStruct[t]
                    t += 1
            if len(tempStruct) > 0:
                df.iloc[i][columnName] = []
            i += 1
    # if ached == 2:  # in attached form



        # for row in df[columnName]:
        #     # match = False
        #     tempStruct = termStruct.copy()
        #     t = 0
        #     wordtracker = 0
        #     while wordtracker < len(df.iloc[i][columnName]):
        #         if tempStruct[t][1] == 'text':
        #             listNo = 0
        #         else:
        #             listNo = 1
        #         if df.iloc[i][columnName][wordtracker][listNo] == tempStruct[t][0]:
        #             match = True #not using the correct match?
        #             run = True
        #             wordmatch = 0
        #             try:
        #                 while match == True and run == True:
        #                     if len(tempStruct) - t > 0 and len(df.iloc[i][columnName]) - wordtracker > 0:
        #                         # print(str(df.iloc[i][columnName][wordtracker][listNo]) +":" + str(wordtracker) + ":compare:" + str(tempStruct[t][0])+":"+str(t))
        #                         if df.iloc[i][columnName][wordtracker][listNo] == tempStruct[t][0]:
        #                             # print("match")
        #                             match = True
        #                             wordmatch += 1
        #                             if len(df.iloc[i][columnName]) - wordtracker > 1:
        #                                 # print("increase word tracker")
        #                                 wordtracker += 1
        #                             else:
        #                                 # print("dont increase wordtracker")
        #                                 run= False
        #                             if len(tempStruct) - t > 1: #2 - 0 > 1
        #                                 # print("increase t")
        #                                 t += 1
        #                             else:
        #                                 # print("dont increase")
        #                                 run = False
        #                         else:
        #                             # print("dont match")
        #                             match = False
        #                     else:
        #                         print("n and k")
        #                         run = False
        #
        #             except Exception as e:
        #                 print(" my error here at option 14 "+str(e))
        #         print(str(wordmatch) + " compar " + str(len(tempStruct)))
        #         if wordmatch != len(tempStruct):
        #             print(str(wordmatch) + " havent match all " + str(len(tempStruct)))
        #             match = False
        #         else:
        #             match = True
        #         if match == True:
        #             pass
        #         else:
        #             print("clean to []")
        #             df.iloc[i][columnName] = []
        #         if len(df.iloc[i][columnName]) - wordtracker > 1:
        #             # print("increase word tracker")
        #             wordtracker += 1
        #         if len(tempStruct) - t > 1:  # 2 - 0 > 1
        #             # print("increase t")
        #             t += 1
        #     # if(wordtracker == len(df.iloc[i][columnName])):
        #     i += 1
        #     wordtracker = 0
        #     t = 0

        # for row in df[columnName]:
        #     tempStruct = termStruct.copy()
        #     tempCount = len(tempStruct)
        #     j = 0
        #     t = 0
        #     for word in df.iloc[i][columnName]:
        #         for element in tempStruct:
        #             if tempStruct[t][1] == 'text':
        #                 listNo = 0
        #             else:
        #                 listNo = 1
        #             if word[listNo] == tempStruct[t][0]:  # if value match remove from list of struct to track
        #                 tempJ = j
        #                 tempT = t
        #                 totalInRow = len(df.iloc[i][columnName])
        #                 try:
        #                     while (totalInRow - tempCount) >= 0 and (totalInRow - tempJ) >= 0 and (tempCount - tempT) >=0 and len(tempStruct) > 0:
        #                         print( str(totalInRow - tempCount)+ " " + str(totalInRow - tempJ) + " " + str(tempCount - tempT))
        #                         print(str(df.iloc[i][columnName][tempJ][listNo]) + " compare " + (tempStruct[tempT][0]))
        #                         print(str(tempJ)+"<>"+str(tempT))
        #                         if df.iloc[i][columnName][tempJ][listNo] == tempStruct[tempT][0]:
        #                             print(tempStruct)
        #                             del tempStruct[tempT]
        #                             tempT-=1
        #                             print(tempStruct)
        #                         tempJ += 1
        #                         tempT += 1
        #                         print(str(tempJ)+"<A>"+str(tempT))
        #                         if len(tempStruct) == 0: #no more values
        #                             break
        #                     if len(tempStruct) > 0:  # failed match
        #                         print("failed")
        #                         tempStruct = termStruct.copy()
        #                 except Exception as e:
        #                     print("LINE 210 " + str(e))
        #             t += 1
        #         j += 1
        #     if len(tempStruct) > 0:
        #         df.iloc[i][columnName] = []
        #     i += 1
    return df


def simpleUI():
    while True:  # part of do while loop
        try:
            select = int(input("POS 1:Intersect 2:SymDif 3:Union \n"
                               "Label 4:Intersect 5:SymDif 6:Union \n"
                               "Highlight 7:POS Intersect 8:label Intersect \n"
                               # "Social 9:POS Intersect 10:label Intersect \n"
                               "11:Save 12:Math 13:Modify 14:term_association 0:exit >>"))
            columnName = columnNameB = default.defaultColumn()
            if select == 1:
                df, df2 = selectFile()
                dateColumnA = dateColumnB = default.defaultDateColumn()
                simpleSortByDateRange(df, df2, dateColumnA, dateColumnB)
                spacyNLP.spacyToken(df, columnName)
                spacyNLP.spacyToken(df2, columnNameB)
                spacyNLP.spacyStopword(df, columnName)
                spacyNLP.spacyStopword(df2, columnNameB)
                spacyNLP.spacyPOSToken(df, columnName)
                spacyNLP.spacyPOSToken(df2, columnNameB)
                venn.vennIntersect(df, columnName, df2, columnNameB)
                spacyNLP.spacyCleanCell(df, columnName)
                spacyNLP.spacyCleanCell(df2, columnNameB)
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
                simpleSortByDateRange(df, df2, dateColumnA, dateColumnB)
                spacyNLP.spacyToken(df, columnName)
                spacyNLP.spacyToken(df2, columnNameB)
                spacyNLP.spacyStopword(df, columnName)
                spacyNLP.spacyStopword(df2, columnNameB)
                spacyNLP.spacyLabelToken(df, columnName)
                spacyNLP.spacyLabelToken(df2, columnNameB)
                print(df,df2)
                venn.vennIntersect(df, columnName, df2, columnNameB)
                # spacyNLP.spacyCleanCell(df, columnName)
                # spacyNLP.spacyCleanCell(df2, columnNameB)
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
            if select == 7:
                df, df2 = selectFile()
                dateColumnA = dateColumnB = default.defaultDateColumn()
                simpleSortByDateRange(df, df2, dateColumnA, dateColumnB)
                spacyNLP.spacyToken(df, columnName)
                spacyNLP.spacyToken(df2, columnNameB)
                spacyNLP.spacyStopword(df, columnName)
                spacyNLP.spacyStopword(df2, columnNameB)
                spacyNLP.spacyPOSToken(df, columnName)
                spacyNLP.spacyPOSToken(df2, columnNameB)
                intersect = venn.vennUniqueIntersect(df, columnName, df2, columnNameB)
                try:
                    highlightOption = int(input("1:display 2:save_html >>"))
                    if highlightOption == 1:
                        displayColorText(df, columnName, df2, columnNameB, intersect)
                    if highlightOption == 2:
                        filename = input("Please enter [filename].html >>")
                        writeHTML(df, columnName, df2, columnNameB, intersect, filename)
                except:
                    print("highlight error")
            if select == 8:
                df, df2 = selectFile()
                dateColumnA = dateColumnB = default.defaultDateColumn()
                simpleSortByDateRange(df, df2, dateColumnA, dateColumnB)
                spacyNLP.spacyToken(df, columnName)
                spacyNLP.spacyToken(df2, columnNameB)
                spacyNLP.spacyStopword(df, columnName)
                spacyNLP.spacyStopword(df2, columnNameB)
                spacyNLP.spacyLabelToken(df, columnName)
                spacyNLP.spacyLabelToken(df2, columnNameB)
                intersect = venn.vennUniqueIntersect(df, columnName, df2, columnNameB)
                try:
                    highlightOption = int(input("1:display 2:save_html >>"))
                    if highlightOption == 1:
                        displayColorText(df, columnName, df2, columnNameB, intersect)
                    if highlightOption == 2:
                        filename = input("Please enter [filename].html >>")
                        writeHTML(df, columnName, df2, columnNameB, intersect, filename)
                except:
                    print("highlight error")
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
            if select == 12:
                while True:
                    try:
                        mathOption = int(input("1:counter 2:term_frequency 3:frequency_By_Date 0:exit >>"))
                        writeOption = int(input("1:file_A 2:file_B 0:exit >>"))

                        if mathOption == 0:
                            break
                        if mathOption == 3:
                            value = input("The value to track its frequency by its date >>")
                            if writeOption == 1:
                                countA = spacyNLP.spacyFrequencyByDate(df, columnName, 0, value)
                                writeCountAsFile(countA, writeOption)
                            if  writeOption == 2:
                                countB = spacyNLP.spacyFrequencyByDate(df2, columnNameB, 0, value)
                                writeCountAsFile(countB, writeOption)
                        if mathOption == 2:
                            if writeOption == 1:
                                countA = spacyNLP.spacyTokenTagCounter(df, columnName, 0)
                                countA = fraction(countA)
                                writeCountAsFile(countA, writeOption)
                            if writeOption == 2:
                                countB = spacyNLP.spacyTokenTagCounter(df2, columnNameB, 0)
                                countB = fraction(countB)
                                writeCountAsFile(countB, writeOption)
                        if mathOption == 1:
                            if writeOption == 1:
                                countA = spacyNLP.spacyTokenTagCounter(df, columnName, 0)
                                writeCountAsFile(countA, writeOption)
                            if writeOption == 2:
                                countB = spacyNLP.spacyTokenTagCounter(df2, columnNameB, 0)
                                writeCountAsFile(countB, writeOption)
                    except:
                        print("math option error")
            if select == 13:
                while True:
                    try:
                        fileOption = int(input("1:file_A 2:file_B 0:exit >>"))
                        if fileOption == 0:
                            break
                        modifyOption = int(input("1:filter 2:strip 0:exit >>"))
                        if modifyOption == 0:
                            break
                        textTagOption = int(input("1:text 2:tag >>"))
                        if textTagOption == 1:
                            textTagOption = 0
                        elif textTagOption == 2:
                            textTagOption = 1
                        value = input("Enter value to filter or strip >>")
                        if modifyOption == 1:
                            if fileOption == 1:
                                spacyNLP.spacyColumnFilterToken(df, columnName, value, textTagOption)
                            if fileOption == 2:
                                spacyNLP.spacyColumnFilterToken(df2, columnNameB, value, textTagOption)
                        if modifyOption == 2:
                            if fileOption == 1:
                                spacyNLP.spacyColumnStripToken(df, columnName, value, textTagOption)
                            if fileOption == 2:
                                spacyNLP.spacyColumnStripToken(df2, columnNameB, value, textTagOption)
                    except:
                        print("modify option error")
            if select == 14:
                fileAorB = int(input("1:file_A 2:file_B 0:exit >>"))
                if fileAorB == 0:
                    break
                ached = int(input("Term association are to be 1:detached or 2:attached 0:exit >>"))
                if ached == 0:
                    break
                termStruct = [['VERB', 'tag'], ['NOUN', 'tag']]
                while True:
                    try:
                        insetRun = int(input("1:insert_term 2:run 0:exit >>"))
                        if insetRun == 0:
                            break
                        if insetRun == 1:
                            termInput = input("Insert term :" + str(termStruct) + " >>")
                            termTextTag = int(input("The term: " + termInput + " is 1:text or 2:tag >>"))
                            if termTextTag == 1:
                                listIdentity = "text"
                            else:
                                listIdentity = "tag"
                            termStruct.append([str(termInput), str(listIdentity)])
                            print(termStruct)
                        if insetRun == 2:
                            if fileAorB == 1:
                                assocTerm(df, columnName, termStruct, ached)
                            if fileAorB == 2:
                                assocTerm(df2, columnNameB, termStruct, ached)
                            break
                    except Exception as e:
                        print(e)
                        break

            if select == 0:
                break

            displayDataframe(df, df2)
        except:
            print("invalid option!")


simpleUI()
