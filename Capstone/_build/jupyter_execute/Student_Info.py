#!/usr/bin/env python
# coding: utf-8

# In[1]:


from functions import *


# # Student Info
# 
# ---

# ## General

# The student info dataframe contains information about students including the module and presentation they took, demographic information and the final result of their studies.

# In[2]:


# looking at the student_info dataframe
student_info.head()


# ## Student Info Contents
# 
# * **code_module**: The code module represents the course the student is taking.
# * **code_presentation**: The code presentations are the year and semester the student is taking the course.
# * **id_student**: The student ID is a unique identifier for each student
# * **gender**: The gender represents the binary gender of a student 'M' for students who identify as male and 'F' for students who identify as female.
# * **region**: Region represents the location of the student when they took the module. All regions are in the UK, Scotland, Ireland or Wales.
# * **highest_education**: Highest education is representative of a students highest level of formal academic achievement.
#     - Education levels in order from least to most formal education: 
#         - No formal quals (qualifications)
#         - Lower than A Level which is nearly but not quite analagous to under high school level
#         - A Level or equivalent which is again nearly analagous to high school level, but more like college ready
#         - HE Qualification which stands for higher education qualification
#         - Post Graduate Qualification
# * **imd_band**: The imd_band represents the Indices of multiple deprivation (IMD) score which is a commonly used method in the UK to measure poverty or deprivation in an area. The lower the score, the more 'deprived' the area is.
# * **age_band**: There are only three bins for age; 0-35, 35-55 and over 55
# * **num_of_prev_attempts**: The number of times the student has attempted the course previously.
# * **studied_credits**: The number of credits for the module the student is taking.
# * **disability**: Disability status is represented by a binary 'Y', yes a student does identify as having a disability and 'N', no a student does not identify as having a disability.
# * **final_results**: * The final result is the students overall result in the class.
#     - Possible Results include:
#          - Pass: The student passed the course
#          - Fail: The student did not pass the course
#          - Withdraw: The student withdrew before the course term ended
#          - Distinction: The student passed the class with distinction

# * studied_credits will not be a part of our analysis and will be removed
# * num_of_prev_attempts will be changed to prev_attempts to save space

# In[3]:


# student_info = student_info.drop(columns='studied_credits')
student_info.rename(columns={'num_of_prev_attempts':'prev_attempts'})


# ---
# 
# ## Student Info Information

# In[4]:


# get size counts of student_info
get_size(student_info)


# In[5]:


# show student info data types
get_dtypes(student_info)


# `id_student` is currently an int64 datatype, but would be more appropriate as an object data type since it is categorical.

# In[6]:


# changing id_student to the object data type
student_info['id_student'] = student_info['id_student'].astype(object)


# **Null Values:**

# In[7]:


null_vals(student_info)


# In[8]:


# store sum of imd null values
imd_null = student_info['imd_band'].isnull().sum()
md(f'''The imd_band variable has {imd_null} null values which we may have to work around.''')


# **Duplicate Values**

# In[9]:


# show duplicate values in student info if any
get_dupes(student_info)


# **Unique Counts:**

# In[10]:


# Get number of unique values per variable in student info
count_unique(student_info)


# In[11]:


# store count of total student ids
total_students = student_info['id_student'].count()
# store count of unique student ids
unique_students = student_info['id_student'].nunique()


# In[12]:


md(f'''
* There are {total_students} entries for students but only {unique_students} unique student IDs.
* This may represent students who have taken the course more than once or who are taking multiple modules
''')


# **Unique Categorical Values**

# In[13]:


unique_vals(student_info)


# In imd_band the % sign is missing in 10-20. We will add that for consistency and clarity

# In[14]:


# changing all 10-20 values in student_info imd_band to 10-20% for consistency's sake
student_info.loc[student_info['imd_band'] == '10-20', 'imd_band'] = '10-20%'
# making sure it updated
student_info['imd_band'].explode().unique()


# **Statistics:**

# In[15]:


# show statistical breakdown of numerical values in student info
student_info.describe().astype(int)


# In[16]:


# store the highest number of module previous attempts by students
max_attempts = student_info['num_of_prev_attempts'].max()


# In[17]:


md(f'''
* Most students do not have a previous attempt, but there is a high of {max_attempts} attempts.
* We can only have data for up to two of the students attempts since we only have two years worth of data.
''')


# In[ ]:




