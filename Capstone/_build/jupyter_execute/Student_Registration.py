#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('capture', '', 'from functions import *\n\n@register_cell_magic\ndef markdown(line, cell):\n    return md(cell.format(**globals()))')


# # Student Registration Dataframe

# ---
# The student registration dataframe contains information about the dates that students registered and,if applicable, unregistered from the module.
# 
# ### Contents
# 
# * **code_module**: The code module represents the course which the sutdent registered for.
# * **code_presentation**: The code presentation represents the time of year the course which the student registered for began.
# * **id_student**: The student ID is the unique identifier for each student.
# * **date_registration**: The registration date is the date that the student registered for the module relative to the start of the module. A negative value indicates that many days before the module began.
# * **date_unregistration**: The unregistration date is the date that the student unregistered from the course module in relation to the start date of the course, if applicable.
# 

# In[2]:


# looking at the student_registration dataframe
student_registration.head()


# In[4]:


md(f'''

**Size**
    
* Number of Rows: {len(student_registration)}
* Number of Columns: {len(student_registration.columns)}

**Data Types**
''')


# In[6]:


# show student info data types
student_registration.dtypes


# * id_student is currently an int64 datatype, but would be more appropriate as an object data type since it is categorical.

# In[7]:


# changing id_student to the object data type
student_registration['id_student'] = student_registration['id_student'].astype(object)


# **Null Values:**

# In[8]:


student_registration.isnull().sum()


# In[15]:


null_registration = student_registration['date_registration'].isnull().sum()
null_unregistration = student_registration['date_unregistration'].isnull().sum()


# In[16]:


get_ipython().run_cell_magic('markdown', '', '\n* We have {null_registration} null values for date_registration, and no mention of this in the dataset documentation, so we will treat this as missing data.\n* There are {null_unregistration} null values for date_unregistration which represent the students that did not withdraw from the course.')


# **Unique Counts:**

# In[17]:


student_registration.nunique()


# **Unique Categorical Values**

# In[18]:


unique_vals(student_registration)


# In imd_band the % sign is missing in 10-20. We will add that for consistency and clarity

# In[71]:


# changing all 10-20 values in student_info imd_band to 10-20% for consistency's sake
student_info.loc[student_info['imd_band'] == '10-20', 'imd_band'] = '10-20%'
print(student_info['imd_band'].explode().unique())


# **Duplicate Values**

# In[56]:


analyze_df(student_registration, dupes=True)


# In[57]:


md(f'''* The Student info dataframe is {len(student_registration)} rows, but there are only {student_registration['id_student'].nunique()} unique student ID's.
* This suggests that there are some students who took multiple modules since we eliminated those who have taken the same course more than once.
        ''')


# In[67]:


student_registration[student_registration['id_student'].duplicated()].head()


# **Duplicate Student ID's**

# In[61]:


# finding student records with duplicate ID's
pd.concat(x for _, x in student_registration.groupby("id_student") if len(x) > 1).head()


# In[68]:


duped_sids = student_registration[student_registration['id_student'].duplicated()]
total_sid_dupes = pd.concat(x for _, x in student_registration.groupby("id_student") if len(x) > 1)


# In[70]:


md(f'''We have {len(duped_sids)} students whose ID is listed more than once and a total of {len(total_sid_dupes)} duplicate records. These students do seem to be in different courses, and so we will leave them''')


# **Statistics:**

# In[40]:


student_registration.describe().astype(int)


# * There are 8,612 values for the count of date_unregistration which represents the number of students who withdrew from the course.
# * The earliest date_unregistration date is 274 days before the course began, which means these students did not make it to the first day. We are only interested in students who took the course so we must eliminate students who did not attend.

# In[45]:


# removing students who withdrew on or before the first day
student_registration = student_registration.drop(student_registration[(student_registration['date_unregistration'] <= 0)].index)
student_registration.reset_index(drop=True).head()


# In[46]:


# finds the longest module length in courses and prints it
longest_course = courses['module_presentation_length'].max()
longest_unreg = student_registration['date_unregistration'].max().astype(int)
md(f'''* The longest course from module_presentation length in the courses dataframe was {longest_course} days, yet we see here the latest unregistration date is {longest_unreg} days, which is longer than any course went on.
    ''')


# **All Students with an unregistration point after 269 days:**

# In[47]:


# finding students whose courses went on for longer than the maximum course length
student_registration.loc[student_registration['date_unregistration'] > 269]


# * It seems to be just this one student is an outlier, but should not affect our overall analysis so we will leave this intact

# In[ ]:




