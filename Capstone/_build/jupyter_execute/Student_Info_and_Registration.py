#!/usr/bin/env python
# coding: utf-8

# In[1]:


from functions import *

@register_cell_magic
def markdown(line, cell):
    return md(cell.format(**globals()))


# <a id='StudentInfo'></a>
# 
# <h2>Student Info and Student Registration Cleaning</h2>
# 
# ---

# ```{note}
# * The student registration dataframe matches 1:1 with the student_info dataframe only adding the date the student registered and the date, if applicable, they unregistered, and so we will merge these two dataframes
# * Though the number of previous attempts may be interesting to analyze on its own to see the relationship between students who had to take the course multiple times, and the differences in their bahavior on the second or higher attempt, here we are only interested in students on their first attempt. The reason is that familiarity with course content is a confounding variable. Due to this we will remove students on their second or higher attempt. We will then remove num_prev_attempts since it will not contain any interesting data.
# * studied_credits will not be a part of our analysis, and so may be removed.
# * The dataframe columns can then be reordered to keep relevent data together. 
# ```

# In[6]:


# left join and merge student info with student registration
student_info_reg = student_info.merge(student_registration, how='left', on=['code_module', 'code_presentation', 'id_student'])

# changing the student info dataframe to include only records where num_prev_attempts is 
student_info_reg = student_info_reg[student_info_reg['num_of_prev_attempts'] == 0]

# reordering the student_info dataframe to keep country, module and student data together
student_info_reg = student_info_reg[['code_module', 'code_presentation', 'id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result', 'date_registration', 'date_unregistration']]


# ---
# 
# <h4>Student Info Information</h4>

# <b>Updated Dataframe</b>

# In[7]:


# looking at our now merged dataframe
student_info_reg.head()


# In[8]:


md(f'''

<b>Size</b>
    
* Number of Rows: {len(student_info_reg)}
* Number of Columns: {len(student_info_reg.columns)}

<b>Data Types</b>
''')


# In[9]:


# show student info data types
student_info_reg.dtypes


# * id_student is currently an int64 datatype, but would be more appropriate as an object data type since it is categorical.

# In[10]:


# changing id_student to the object data type
student_info_reg['id_student'] = student_info_reg['id_student'].astype(object)


# <b>Null Values:</b>

# In[11]:


student_info_reg.isnull().sum()


# * The imd_band variable has 990 null values which we may have to work around. 
# * There are 19,809 null values for date_unregistration which represent the students that did not withdraw from the course.
# * We have 38 null values for date_registration, and no mention of this in the dataset documentation, so we will treat this as missing data.

# <b>Unique Counts:</b>

# In[12]:


student_info_reg.nunique()


# <b>Unique Categorical Values</b>

# In[13]:


unique_vals(student_info_reg)


# In imd_band the % sign is missing in 10-20. We will add that for consistency and clarity

# In[14]:


# changing all 10-20 values in student_info imd_band to 10-20% for consistency's sake
student_info.loc[student_info['imd_band'] == '10-20', 'imd_band'] = '10-20%'
print(student_info['imd_band'].explode().unique())


# <b>Duplicate Values</b>

# In[15]:


analyze_df(student_info_reg, dupes=True)


# In[16]:


md(f'''* The Student info dataframe is {len(student_info_reg)} rows, but there are only {student_info_reg['id_student'].nunique()} unique student ID's.
* This suggests that there are some students who took multiple modules since we eliminated those who have taken the same course more than once.
        ''')


# In[17]:


student_info_reg[student_info_reg['id_student'].duplicated()].head()


# <b>Duplicate Student ID's</b>

# In[18]:


# finding student records with duplicate ID's
pd.concat(x for _, x in student_info_reg.groupby("id_student") if len(x) > 1).head()


# In[19]:


duped_sids = student_info_reg[student_info_reg['id_student'].duplicated()]
total_sid_dupes = pd.concat(x for _, x in student_info_reg.groupby("id_student") if len(x) > 1)


# In[20]:


md(f'''We have {len(duped_sids)} students whose ID is listed more than once and a total of {len(total_sid_dupes)} duplicate records. These students do seem to be in different courses, and so we will leave them''')


# <b>Statistics:</b>

# In[21]:


student_info_reg.describe().astype(int)


# * There are 8,612 values for the count of date_unregistration which represents the number of students who withdrew from the course.
# * The earliest date_unregistration date is 274 days before the course began, which means these students did not make it to the first day. We are only interested in students who took the course so we must eliminate students who did not attend.

# In[22]:


# removing students who withdrew on or before the first day
student_info_reg = student_info_reg.drop(student_info_reg[(student_info_reg['date_unregistration'] <= 0)].index)
student_info_reg.reset_index(drop=True).head()


# In[23]:


# finds the longest module length in courses and prints it
longest_course = courses['module_presentation_length'].max()
longest_unreg = student_info_reg['date_unregistration'].max().astype(int)
md(f'''* The longest course from module_presentation length in the courses dataframe was {longest_course} days, yet we see here the latest unregistration date is {longest_unreg} days, which is longer than any course went on.
    ''')


# <b>All Students with an unregistration point after 269 days:</b>

# In[24]:


# finding students whose courses went on for longer than the maximum course length
student_info_reg.loc[student_info_reg['date_unregistration'] > 269]


# * It seems to be just this one student is an outlier, but should not affect our overall analysis so we will leave this intact

# In[ ]:




