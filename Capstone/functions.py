# import statements
import pandas as pd
import numpy as np
import os
from sklearn import linear_model
import seaborn as sns
import itertools
import matplotlib.pyplot as plt
from IPython.display import Markdown as md
from IPython.core.magic import register_cell_magic
from IPython.display import HTML
import random

# setting the path to the csv files
path = os.path.join(os.path.abspath(os.getcwd()), 'csvs\\')
dataframe = pd.DataFrame

student_info = pd.read_csv(path+'studentInfo.csv')
student_registration = pd.read_csv(path+'studentRegistration.csv')
courses = pd.read_csv(path+'courses.csv')
assessments = pd.read_csv(path+'assessments.csv')
student_assessment = pd.read_csv(path+'studentAssessment.csv')
student_vle = pd.read_csv(path+'studentVle.csv')
vle = pd.read_csv(path+'vle.csv')



# a function to print some basic analysis of dataframes
'''def analyze_df(df, rowlen=False, collen=False, types=False, nulls=False, uniques=False, dupes=False, nums=False):
    if types:
        # print dataframe column data types
        return df.dtypes
    elif nulls:
        # print which columns have null values and how many
        df.isnull().sum()
    elif uniques:
        # print the number of unique values per variable in data
        return df.nunique()
    # print duplicate values if there are any else prints "No Duplicate Values"
    elif dupes:
        if not df[df.duplicated()].empty:
            return df[df.duplicated()]
        else:
            return "No Duplicate Values"
    elif nums:
        return df.describe()'''

@register_cell_magic
def markdown(line, cell):
    return md(cell.format(**globals()))   

# function to style dataframes as first column being bold and hiding the index
# to bring attention to the important data
def boldify(df):
    df = df.style.set_table_styles([{'selector': 'td.col0', 'props': 'font-weight:bold'}]).hide_index()
    return df
    
def null_vals(df):
    # if the dataframe of nulls is not empty return the null values as a dataframe
    if not df[df.isnull()].empty:
        df_nulls = dataframe(df.isnull().sum(), columns=['Null Values'])
        df_nulls.index.name = "Variable"
        df_nulls = df_nulls.reset_index()
        return boldify(df_nulls)
    else:
        return md("No Null Values")

# function to make a dataframe of a dataframes columns datatypes
def get_dtypes(df):
    # make a dataframe out of datatypes
    df_dtypes = dataframe(df.dtypes, columns=['Type'])
    # index is automatically the column variables
    # set index name to variable
    df_dtypes.index.name = "Variable"
    # make index into a range index so Variable can be a column
    df_dtypes = df_dtypes.reset_index()
    # return data types dataframe
    return boldify(df_dtypes)
    
# function to get the row and column counts of a dataframe
def get_size(df):
    # get the count of dataframe columns
    col_size = len(df.columns)
    # get the count of the dataframe rows
    row_size = len(df)
    # create dataframe of columns and rows with their count
    df_sizes = dataframe(columns=['Count'], index=['Columns', 'Rows'], data=[col_size, row_size])
    # return the dataframe
    return df_sizes

#function to get duplicate rows in a dataframe
def get_dupes(df):
    # if the dataframe of duplicated values is not empty return the dataframe of duplicate values
    if not df[df.duplicated()].empty:
        df_dupes = df[df.duplicated()]
        return md(f"Duplicate Values:\n\n{boldify(df_dupes)}\n\n")
    # else return No Duplicate Values
    else:
        return md("No Duplicate Values")

def numerical_analysis(df):
    print(f"Size: {df.value_counts} rows")
    print(f"Numerical Variable Analysis:\n\n")
    df.describe()


# function to makea  dataframe of the counts of unique values in columns
def count_unique(df):
    # create dataframe of unique value counts per column
    unique_counts = dataframe(df.nunique(), columns=['Count'])
    # make a range index to make the variable names a column
    unique_counts = unique_counts.reset_index()
    # return dataframe of unique column counts
    return boldify(unique_counts)

# function to print the unique values of each categorical column in a dataframe
def unique_vals(df):
    # iterate through the dataframe columns
    for i in df.columns:
        # find columns which are 'object' data type
        if df[i].dtypes == object:
            # get all of the unique values in a column
            unique_values = df[i].explode().unique()
            # Student ID is categorical but we don't want to return all of those
            # so limiting to the variables where unique_vals is less than 25
            if len(unique_values) < 25:
                # retrieve unique values in a list from each variable
                unique_val_list = [[df[i].explode().unique() for i in df.columns]]
                # create a df using a dict mapping the values of the unique value list to a column vs a row
                unique_vals_df = dataframe(dict(zip(["Values"], unique_val_list)), index = courses.columns)
                # add a range index to put the variables into a row instead of the index
                unique_vals_df = unique_vals_df.reset_index()
                # return the dataframe 
                return boldify(unique_vals_df)
            


# a function to change dataframe column values based on a given dictionary
def change_col_val(val_dict, df):
    # val_dict is a dictionary of lists
    for k, v in val_dict.items():
        for i in v:
            # change the value of the cell to its index number in a list
            df.loc[df[k] == i, k] = v.index(i)


# a function to get a percentage
def percentage(part, whole):
    return round(100 * float(part) / float(whole), 2)
