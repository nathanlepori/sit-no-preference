import pandas as pd
import no_preference.processing.analysis.sort as sort


def venn_intersect_text_tag(df_a, column_name, set_b, column_name_b, list_no):
    """ Precondition is to have been tokenized
      per venn diagram illustration of intersect of a set A and set B
      This function does WILL affect the dataframe that was pass by reference
    This function will modify the both dataframe to keep words found in both set A and set B, hence intersect"""
    df_a = sort.reindex(df_a)
    set_b = sort.reindex(set_b)

    match = []
    for row in df_a[column_name]:
        for word in row:
            for rowB in set_b[column_name_b]:
                for wordB in rowB:
                    if word[:][list_no] not in match:  # if each element in setA cannot be found in the match list
                        if word[:][list_no] in wordB[:][list_no]:  # then we use it to check if its in each element of
                            # SetB (the whole dataframe)
                            match.append(word[:][list_no])  # if found append into match list
            if word[:][list_no] not in match:  # if the element cant be find in match
                # remove element that are not found in match list
                del word[:]
        # end of setA
    for rowB in set_b[column_name_b]:  # start removing non match from setB
        for wordB in rowB:
            if wordB[:][list_no] not in match:  # if the element cant be find in match
                # remove element that are not found in match list
                del wordB[:]
    return df_a, set_b


def venn_symmetric_dif_text_tag(df_a, column_name_a, set_b, column_name_b, list_no):
    """ Precondition is to have been tokenized
      per venn diagram illustration of intersect of a set A and set B
      This function does WILL affect the dataframe that was pass by reference
    This function will modify the both dataframe to keep words found in both set A and set B, hence intersect"""
    df_a = sort.reindex(df_a)
    set_b = sort.reindex(set_b)

    match = []
    for row in df_a[column_name_a]:
        for word in row:
            for rowB in set_b[column_name_b]:
                for wordB in rowB:
                    if word[:][list_no] not in match:  # if element cant be found in match list
                        if word[:][list_no] in wordB[:][list_no]:  # if SetA element can be found in SetB dataframe
                            match.append(word[:][list_no])  # if found append into match list
            if word[:][list_no] in match:  # if element of SetA can be found in match list
                # remove element that are found in match list
                del word[:]
        # end of setA

    for row in set_b[column_name_b]:  # start removing non match from setB
        for wordB in row:
            if wordB[:][list_no] in match:  # if element of SetB can be found in match list
                # remove element that are found in match list
                del wordB[:]
    return df_a, set_b


def venn_union(df_a, df_b):
    """precondition both dataframe setA and setB must have the same columns
    this function will join merge 2 dataframe setA and setB as result dataframe and return
        as a single dataframe
    """
    frames = [df_a, df_b]
    result = pd.concat(frames)
    result = sort.reindex(result)  # reindex as it will keep the old index from both sets
    return result
