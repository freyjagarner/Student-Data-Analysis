#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('capture', '', 'from functions import *\n\n@register_cell_magic\ndef markdown(line, cell):\n    return md(cell.format(**globals()))')


# # Student Info
# 
# ---

# The student info dataframe contains information about students including the module and presentation they took, demographic information and the final result of their studies.

# In[2]:


# looking at the student_info dataframe
student_info.head()


# ## Contents
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

# ---
# 
# ## Student Info Information

# In[3]:


md(f'''

**Size**
    
* Number of Rows: {len(student_info)}
* Number of Columns: {len(student_info.columns)}

**Data Types**
''')


# In[4]:


# show student info data types
student_info.dtypes


# * id_student is currently an int64 datatype, but would be more appropriate as an object data type since it is categorical.

# In[5]:


# changing id_student to the object data type
student_info['id_student'] = student_info['id_student'].astype(object)


# **Null Values:**

# In[6]:


student_info.isnull().sum()


# In[7]:


imd_null = student_info['imd_band'].isnull().sum()


# In[8]:


get_ipython().run_cell_magic('markdown', '', '\n* The imd_band variable has {imd_null} null values which we may have to work around. ')


# **Unique Counts:**

# In[9]:


student_info.nunique()


# In[10]:


total_students = student_info['id_student'].count()
unique_students = student_info['id_student'].nunique()


# In[11]:


get_ipython().run_cell_magic('markdown', '', '\n* There are {total_students} entries for students but only {unique_students} unique student IDs.\n* This may represent students who have taken the course more than once or who are taking multiple modules')


# **Unique Categorical Values**

# In[12]:


unique_vals(student_info)


# In imd_band the % sign is missing in 10-20. We will add that for consistency and clarity

# In[13]:


# changing all 10-20 values in student_info imd_band to 10-20% for consistency's sake
student_info.loc[student_info['imd_band'] == '10-20', 'imd_band'] = '10-20%'
print(student_info['imd_band'].explode().unique())


# **Duplicate Values**

# In[14]:


analyze_df(student_info, dupes=True)


# **Statistics:**

# In[15]:


student_info.describe().astype(int)


# In[16]:


max_attempts = student_info['num_of_prev_attempts'].max()


# In[17]:


get_ipython().run_cell_magic('markdown', '', '\n* Most students do not have a previous attempt, but there is a high of {max_attempts} attempts.\n* We can only have data for up to two of the students attempts since we only have two years worth of data.')


# In[18]:


ax = sns.countplot(x="code_module", hue="code_presentation", palette="Greens_d", data=student_info)


# In[19]:


students_per_presentation_module = pd.DataFrame(student_info['id_student'].groupby([student_info['code_module'], student_info['code_presentation']]).count()).reset_index()
students_per_presentation_module = students_per_presentation_module.sort_values(by=['code_presentation', 'code_module']).reset_index(drop=True)
students_per_presentation_module['year'] =students_per_presentation_module['code_presentation'].str[:4]
students_per_presentation_module['month'] =students_per_presentation_module['code_presentation'].str[4:]


# In[20]:


students_per_presentation_module


# In[ ]:




