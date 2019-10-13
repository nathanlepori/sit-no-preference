def vennUniqueIntersect(setA, columnName, setB, columnNameB):
    # unique does not affect dataframe
    #must use spacyToken

    match = []
    Ai = 0
    for row in setA[columnName]:
        Aj = 0
        for word in setA.iloc[Ai][columnName]:
            Bi = 0
            for rowB in setB[columnNameB]:
                if setA.iloc[Ai][columnName][Aj] not in match:
                    # if already found skip, avoid many of the same word in future
                    if setA.iloc[Ai][columnName][Aj] in setB.iloc[Bi][columnNameB]:
                        match.append(setA.iloc[Ai][columnName][Aj])
                Bi += 1
            Aj += 1
        Ai += 1
    print(match)
    # return match


def vennIntersect(setA, columnName, setB, columnNameB):
    #must use spacyToken, spacyPOS, spacyLabel
    match = []
    Ai = 0
    for row in setA[columnName]:
        Aj = 0
        for word in setA.iloc[Ai][columnName]:
            Bi = 0
            for rowB in setB[columnNameB]:
                if setA.iloc[Ai][columnName][Aj] not in match:
                    # if already found skip, avoid many of the same word in future
                    if setA.iloc[Ai][columnName][Aj] in setB.iloc[Bi][columnNameB]:
                        match.append(setA.iloc[Ai][columnName][Aj])  # if found keep in match list
                Bi += 1
            if setA.iloc[Ai][columnName][Aj] not in match:  # if still cannot find
                # remove non match from setA
                setA.iloc[Ai][columnName][Aj] = [w for w in setA.iloc[Ai][columnName][Aj] if setA.iloc[Ai][columnName][Aj] in match]
            Aj += 1
        Ai += 1
        # end of setA

    Bi = 0
    for row in setB[columnNameB]:  # start removing non match from setB
        Bj = 0
        for word in setB.iloc[Bi][columnNameB]:
            if setB.iloc[Bi][columnNameB][Bj] not in match:  # if still cannot find
                setB.iloc[Bi][columnNameB][Bj] = [w for w in setB.iloc[Bi][columnNameB][Bj] if setB.iloc[Bi][columnNameB][Bj] in match]
            Bj += 1
        Bi += 1
    # print(setA)
    print(match)
    # return setA #no need return as df is pass by reference, hence working here will update the dataframe passed here

def vennSymmetricDif(setA, columnName, setB, columnNameB):
    #must use spacyToken

    match = []
    noMatchA = []
    Ai = 0
    for row in setA[columnName]:
        Aj = 0
        for word in setA.iloc[Ai][columnName]:
            Bi = 0
            for rowB in setB[columnNameB]:
                if setA.iloc[Ai][columnName][Aj] not in match:
                    if setA.iloc[Ai][columnName][Aj] in setB.iloc[Bi][columnNameB]:
                        match.append(setA.iloc[Ai][columnName][Aj])
                Bi += 1
            if setA.iloc[Ai][columnName][Aj] not in match:  # if still cannot find
                if setA.iloc[Ai][columnName][Aj] not in noMatchA:
                    noMatchA.append(setA.iloc[Ai][columnName][Aj])
            setA.iloc[Ai][columnName][Aj] = [w for w in setA.iloc[Ai][columnName] if w in noMatchA]
            Aj += 1
        Ai += 1
    # print(match,end=' < match a\n')
    # print(noMatchA,end=' < no match a\n')

    noMatchB =[]
    Bi = 0
    for row in setB[columnNameB]:
        Bj = 0
        for word in setB.iloc[Bi][columnNameB]:
            Ai = 0
            for rowA in setA[columnName]:
                if setB.iloc[Bi][columnNameB][Bj] not in match:
                    if setB.iloc[Bi][columnNameB][Bj] in setA.iloc[Ai][columnName]:
                        match.append(setB.iloc[Bi][columnName][Bj])
                Ai += 1
            if setB.iloc[Bi][columnNameB][Bj] not in match:  # if still cannot find
                if setB.iloc[Bi][columnNameB][Bj] not in noMatchB:
                    noMatchB.append(setB.iloc[Bi][columnName][Bj])
            setB.iloc[Bi][columnNameB][Bj] = [w for w in setB.iloc[Bi][columnNameB] if w in noMatchB]
            Bj += 1
        Bi += 1
    # print(match, end=' < match b\n')
    # print(noMatchB,end=' < no match b\n')

    # print(noMatch)
    # return noMatch

def vennUniqueSymmetricDif(setA, columnName, setB, columnNameB):
    # unique does not affect dataframe
    #must use spacyToken

    match = []
    noMatch = []
    Ai = 0
    for row in setA[columnName]:
        Aj = 0
        for word in setA.iloc[Ai][columnName]:
            Bi = 0
            for rowB in setB[columnNameB]:
                if setA.iloc[Ai][columnName][Aj] not in match:
                    if setA.iloc[Ai][columnName][Aj] in setB.iloc[Bi][columnNameB]:
                        match.append(setA.iloc[Ai][columnName][Aj])
                Bi += 1
            if setA.iloc[Ai][columnName][Aj] not in match:  # if still cannot find
                noMatch.append(setA.iloc[Ai][columnName][Aj])
            Aj += 1
        Ai += 1
    print(noMatch)
    return noMatch


def vennUniqueUnion(setA, columnName, setB, columnNameB):
    return setA  # placeholder


# def vennRelativeComplmentOfSetA(setA, columnName, setB, columnNameB):
#     return setA  # placeholder
