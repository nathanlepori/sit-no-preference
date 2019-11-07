import pandas as pd
import no_preference.demo.sort as sort


def vennUniqueIntersect(setA, columnName, setB, columnNameB):
    """ Precondition is to have been tokenized
    per venn diagram illustration of intersect of a set A and set B
    This function will display the words found in both set A and set B, hence intersect
    This function does not affect the dataframe that was pass by reference"""

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
    # print(match)
    return match


def vennIntersect(setA, columnName, setB, columnNameB):
    """ Precondition is to have been tokenized
      per venn diagram illustration of intersect of a set A and set B
      This function does WILL affect the dataframe that was pass by reference
    This function will modify the both dataframe to keep words found in both set A and set B, hence intersect"""

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
                setA.iloc[Ai][columnName][Aj] = [w for w in setA.iloc[Ai][columnName][Aj] if
                                                 setA.iloc[Ai][columnName][Aj] in match]
            Aj += 1
        Ai += 1
        # end of setA

    Bi = 0
    for row in setB[columnNameB]:  # start removing non match from setB
        Bj = 0
        for word in setB.iloc[Bi][columnNameB]:
            if setB.iloc[Bi][columnNameB][Bj] not in match:  # if still cannot find
                setB.iloc[Bi][columnNameB][Bj] = [w for w in setB.iloc[Bi][columnNameB][Bj] if
                                                  setB.iloc[Bi][columnNameB][Bj] in match]
            Bj += 1
        Bi += 1

    # print(setA)
    # print(setB)
    # print(match)
    # return setA #no need return as df is pass by reference, hence working here will update the dataframe passed here


def vennIntersectTextTag(setA, columnName, setB, columnNameB, listNo):
    """ Precondition is to have been tokenized
      per venn diagram illustration of intersect of a set A and set B
      This function does WILL affect the dataframe that was pass by reference
    This function will modify the both dataframe to keep words found in both set A and set B, hence intersect"""
    setA = sort.reindex(setA)
    setB = sort.reindex(setB)

    match = []
    for row in setA[columnName]:
        for word in row:
            for rowB in setB[columnNameB]:
                for wordB in rowB:
                    if word[:][listNo] not in match:  # if each element in setA cannot be found in the match list
                        if word[:][listNo] in wordB[:][listNo]:  # then we use it to check if its in each element of
                            # SetB (the whole dataframe)
                            match.append(word[:][listNo])  # if found append into match list
            if word[:][listNo] not in match:  # if the element cant be find in match
                # remove element that are not found in match list
                del word[:]
        # end of setA
    for rowB in setB[columnNameB]:  # start removing non match from setB
        for wordB in rowB:
            if wordB[:][listNo] not in match:  # if the element cant be find in match
                # remove element that are not found in match list
                del wordB[:]
    return setA, setB


def vennSymmetricDifTextTag(setA, columnName, setB, columnNameB, listNo):
    """ Precondition is to have been tokenized
      per venn diagram illustration of intersect of a set A and set B
      This function does WILL affect the dataframe that was pass by reference
    This function will modify the both dataframe to keep words found in both set A and set B, hence intersect"""
    setA = sort.reindex(setA)
    setB = sort.reindex(setB)

    match = []
    for row in setA[columnName]:
        for word in row:
            for rowB in setB[columnNameB]:
                for wordB in rowB:
                    if word[:][listNo] not in match:  # if element cant be found in match list
                        if word[:][listNo] in wordB[:][listNo]:  # if SetA element can be found in SetB dataframe
                            match.append(word[:][listNo])  # if found append into match list
            if word[:][listNo] in match:  # if element of SetA can be found in match list
                # remove element that are found in match list
                del word[:]
        # end of setA

    for row in setB[columnNameB]:  # start removing non match from setB
        for wordB in row:
            if wordB[:][listNo] in match:  # if element of SetB can be found in match list
                # remove element that are found in match list
                del wordB[:]
    return setA, setB


def vennSymmetricDif(setA, columnName, setB, columnNameB):
    """ Precondition is to have been tokenized
         per venn diagram illustration of Symmetric Difference of a set A and set B
         This function does WILL affect the dataframe that was pass by reference
       This function will modify the both dataframe to NOT keep words found in both set A and set B, hence Symmetric Difference"""

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
            setA.iloc[Ai][columnName][Aj] = [w for w in setA.iloc[Ai][columnName][Aj] if
                                             setA.iloc[Ai][columnName][Aj] in noMatchA]
            Aj += 1
        Ai += 1

    noMatchB = []
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
            setB.iloc[Bi][columnNameB][Bj] = [w for w in setB.iloc[Bi][columnNameB][Bj] if
                                              setB.iloc[Bi][columnNameB][Bj] in noMatchB]
            Bj += 1
        Bi += 1
    # print(match, end=' < match b\n')
    # print(noMatchB,end=' < no match b\n')

    # print(noMatch)
    # return noMatch
    return setA, setB


def vennUniqueSymmetricDif(setA, columnName, setB, columnNameB):
    """ Precondition is to have been tokenized
    per venn diagram illustration of Symmetric Difference of a set A and set B
    This function does not affect the dataframe that was pass by reference
  This function will display words found that are NOT found in both set A and set B, hence Symmetric Difference"""

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


def vennUnion(setA, setB):
    """precondition both dataframe setA and setB must have the same columns
    this function will join merge 2 dataframe setA and setB as result dataframe and return
        as a single dataframe
    """
    frames = [setA, setB]
    result = pd.concat(frames)
    result = sort.reindex(result)  # reindex as it will keep the old index from both sets
    return result
