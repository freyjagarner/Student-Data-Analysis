#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('capture', '', 'from functions import *\n\n@register_cell_magic\ndef markdown(line, cell):\n    return md(cell.format(**globals()))')


# <a id='StudentInfo'></a>
# 
# # Student Info and Student Registration
# 
# ---

# ```{note}
# * The student registration dataframe matches 1:1 with the student_info dataframe only adding the date the student registered and the date, if applicable, they unregistered, and so we will merge these two dataframes
# * Though the number of previous attempts may be interesting to analyze on its own to see the relationship between students who had to take the course multiple times, and the differences in their bahavior on the second or higher attempt, here we are only interested in students on their first attempt. The reason is that familiarity with course content is a confounding variable. Due to this we will remove students on their second or higher attempt. We will then remove num_prev_attempts since it will not contain any interesting data.
# * studied_credits will not be a part of our analysis, and so may be removed.
# * The dataframe columns can then be reordered to keep relevent data together. 
# ```

# In[2]:


# left join and merge student info with student registration
student_info_reg = student_info.merge(student_registration, how='left', on=['code_module', 'code_presentation', 'id_student'])

# changing the student info dataframe to include only records where num_prev_attempts is 
student_info_reg = student_info_reg[student_info_reg['num_of_prev_attempts'] == 0]

# reordering the student_info dataframe to keep country, module and student data together
student_info_reg = student_info_reg[['code_module', 'code_presentation', 'id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result', 'date_registration', 'date_unregistration']]


# ---
# 
# ### Student Info Information

# **Updated Dataframe**

# In[3]:


# looking at our now merged dataframe
student_info_reg.head()


# In[4]:


md(f'''

**Size**
    
* Number of Rows: {len(student_info_reg)}
* Number of Columns: {len(student_info_reg.columns)}

**Data Types**
''')


# In[5]:


# show student info data types
student_info_reg.dtypes


# * id_student is currently an int64 datatype, but would be more appropriate as an object data type since it is categorical.

# In[6]:


# changing id_student to the object data type
student_info_reg['id_student'] = student_info_reg['id_student'].astype(object)


# **Null Values:**

# In[7]:


student_info_reg.isnull().sum()


# * The imd_band variable has 990 null values which we may have to work around. 
# * There are 19,809 null values for date_unregistration which represent the students that did not withdraw from the course.
# * We have 38 null values for date_registration, and no mention of this in the dataset documentation, so we will treat this as missing data.

# **Unique Counts:**

# In[8]:


student_info_reg.nunique()


# **Unique Categorical Values**

# In[9]:


unique_vals(student_info_reg)


# In imd_band the % sign is missing in 10-20. We will add that for consistency and clarity

# In[10]:


# changing all 10-20 values in student_info imd_band to 10-20% for consistency's sake
student_info.loc[student_info['imd_band'] == '10-20', 'imd_band'] = '10-20%'
print(student_info['imd_band'].explode().unique())


# **Duplicate Values**

# In[11]:


analyze_df(student_info_reg, dupes=True)


# In[12]:


md(f'''* The Student info dataframe is {len(student_info_reg)} rows, but there are only {student_info_reg['id_student'].nunique()} unique student ID's.
* This suggests that there are some students who took multiple modules since we eliminated those who have taken the same course more than once.
        ''')


# In[13]:


student_info_reg[student_info_reg['id_student'].duplicated()].head()


# **Duplicate Student ID's**

# In[14]:


# finding student records with duplicate ID's
pd.concat(x for _, x in student_info_reg.groupby("id_student") if len(x) > 1).head()


# In[15]:


duped_sids = student_info_reg[student_info_reg['id_student'].duplicated()]
total_sid_dupes = pd.concat(x for _, x in student_info_reg.groupby("id_student") if len(x) > 1)


# In[16]:


md(f'''We have {len(duped_sids)} students whose ID is listed more than once and a total of {len(total_sid_dupes)} duplicate records. These students do seem to be in different courses, and so we will leave them''')


# **Statistics:**

# In[17]:


student_info_reg.describe().astype(int)


# * There are 8,612 values for the count of date_unregistration which represents the number of students who withdrew from the course.
# * The earliest date_unregistration date is 274 days before the course began, which means these students did not make it to the first day. We are only interested in students who took the course so we must eliminate students who did not attend.

# In[18]:


# removing students who withdrew on or before the first day
student_info_reg = student_info_reg.drop(student_info_reg[(student_info_reg['date_unregistration'] <= 0)].index)
student_info_reg.reset_index(drop=True).head()


# In[22]:


# finds the longest module length in courses and prints it
longest_course = courses['module_presentation_length'].max()
longest_unreg = int(student_info_reg['date_unregistration'].max())
md(f'''* The longest course from module_presentation length in the courses dataframe was {longest_course} days, yet we see here the latest unregistration date is {longest_unreg} days, which is longer than any course went on.
    ''')


# **All Students with an unregistration point after 269 days:**

# In[23]:


# finding students whose courses went on for longer than the maximum course length
student_info_reg.loc[student_info_reg['date_unregistration'] > 269]


# * It seems to be just this one student is an outlier, but should not affect our overall analysis so we will leave this intact

# In[ ]:




