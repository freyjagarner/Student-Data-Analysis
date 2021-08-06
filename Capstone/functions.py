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

student_info = pd.read_csv(path+'studentInfo.csv')
student_registration = pd.read_csv(path+'studentRegistration.csv')
courses = pd.read_csv(path+'courses.csv')
assessments = pd.read_csv(path+'assessments.csv')
student_assessment = pd.read_csv(path+'studentAssessment.csv')
student_vle = pd.read_csv(path+'studentVle.csv')
vle = pd.read_csv(path+'vle.csv')



# a function to print some basic analysis of dataframes
def analyze_df(df, rowlen=False, collen=False, types=False, nulls=False, uniques=False, dupes=False, nums=False):
    if rowlen:
        # get the length of the dataframe
        return len(df)
    elif collen:
        return len(df.columns)
    elif types:
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
        return df.describe()
    
   
    


def numerical_analysis(df):
    print(f"Size: {df.value_counts} rows")
    print(f"Numerical Variable Analysis:\n\n")
    df.describe()


def duplicate_vals(df):
    if not df[df.duplicated()].empty:
        print(f"Duplicate Values:\n\n{df[df.duplicated()]}\n\n")
    else:
        print("No Duplicate Values")


# print the unique values of each column in a dataframe
def unique_vals(df):
    for i in df.columns:
        if df[i].dtypes == object:
            print(f"{i}: {df[i].explode().unique()}\n")


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
