import pandas as pd
import no_preference.demo.sort as sort


def venn_intersect_text_tag(setA, columnName, setB, columnNameB, listNo):
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


def vennUnion(setA, setB):
    """precondition both dataframe setA and setB must have the same columns
    this function will join merge 2 dataframe setA and setB as result dataframe and return
        as a single dataframe
    """
    frames = [setA, setB]
    result = pd.concat(frames)
    result = sort.reindex(result)  # reindex as it will keep the old index from both sets
    return result
