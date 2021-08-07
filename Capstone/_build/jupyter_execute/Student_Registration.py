#!/usr/bin/env python
# coding: utf-8

# In[1]:


from functions import *


# # Student Registration Dataframe
# 
# ---

# ## General

# The student registration dataframe contains information about the dates that students registered and,if applicable, unregistered from the module.

# In[2]:


# looking at the student_registration dataframe
student_registration.head()


# ## Student Registration Contents
# 
# * **code_module**: The code module represents the course which the sutdent registered for.
# * **code_presentation**: The code presentation represents the time of year the course which the student registered for began.
# * **id_student**: The student ID is the unique identifier for each student.
# * **date_registration**: The registration date is the date that the student registered for the module relative to the start of the module. A negative value indicates that many days before the module began.
# * **date_unregistration**: The unregistration date is the date that the student unregistered from the course module in relation to the start date of the course, if applicable.
# 

# **Size**

# In[3]:


# get the row & column sizes for student registration
get_size(student_registration)


# **Data Types**

# In[4]:


# show student registration data types
get_dtypes(student_registration)


# * id_student is currently an int64 datatype, but would be more appropriate as an object data type since it is categorical.

# In[5]:


# changing id_student to the object data type

student_registration['id_student'] = student_registration['id_student'].astype('object')


# **Null Values:**

# In[6]:


# get the null values for each column
null_vals(student_registration)


# In[7]:


# store the sum of null values of date_registration
null_registration = student_registration['date_registration'].isnull().sum()
# store the sum of null values of date_unregistration
null_unregistration = student_registration['date_unregistration'].isnull().sum()


# In[8]:


md(f'''
* We have {null_registration} null values for date_registration, and no mention of this in the dataset documentation, so we will treat this as missing data.
* There are {null_unregistration} null values for date_unregistration which represent the students that did not withdraw from the course.
''')


# **Duplicate Values**

# In[9]:


# get the duplicate values for student registration if any
get_dupes(student_registration)


# **Unique Counts:**

# In[10]:


# get the sum of unique values in columns
count_unique(student_registration)


# **Unique Categorical Values**

# In[11]:


unique_vals(student_registration)


# In[12]:


md(f'''* The Student info dataframe is {len(student_registration)} rows, but there are only {student_registration['id_student'].nunique()} unique student ID's.
* This suggests that there are some students who took multiple modules since we eliminated those who have taken the same course more than once.
        ''')


# In[13]:


student_registration[student_registration['id_student'].duplicated()].head()


# **Duplicate Student ID's**

# In[14]:


# finding student records with duplicate ID's
pd.concat(x for _, x in student_registration.groupby("id_student") if len(x) > 1).head()


# In[15]:


duped_sids = student_registration[student_registration['id_student'].duplicated()]
total_sid_dupes = pd.concat(x for _, x in student_registration.groupby("id_student") if len(x) > 1)


# In[16]:


md(f'''We have {len(duped_sids)} students whose ID is listed more than once and a total of {len(total_sid_dupes)} duplicate records. These students do seem to be in different courses, and so we will leave them''')


# **Statistics:**

# In[17]:


student_registration.describe().astype(int)


# * There are 8,612 values for the count of date_unregistration which represents the number of students who withdrew from the course.
# * The earliest date_unregistration date is 274 days before the course began, which means these students did not make it to the first day. We are only interested in students who took the course so we must eliminate students who did not attend.

# In[18]:


# removing students who withdrew on or before the first day
student_registration = student_registration.drop(student_registration[(student_registration['date_unregistration'] <= 0)].index)
student_registration.reset_index(drop=True).head()


# In[19]:


# finds the longest module length in courses and prints it
longest_course = courses['module_presentation_length'].max()
longest_unreg = student_registration['date_unregistration'].max().astype(int)
md(f'''* The longest course from module_presentation length in the courses dataframe was {longest_course} days, yet we see here the latest unregistration date is {longest_unreg} days, which is longer than any course went on.
    ''')


# **All Students with an unregistration point after 269 days:**

# In[20]:


# finding students whose courses went on for longer than the maximum course length
student_registration.loc[student_registration['date_unregistration'] > 269]


# * It seems to be just this one student is an outlier, but should not affect our overall analysis so we will leave this intact

# In[ ]:




