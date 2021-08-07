#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('capture', '', 'from functions import *\n\n@register_cell_magic\ndef markdown(line, cell):\n    return md(cell.format(**globals()))')


# ---
# 
# # Student Assessment

# The Student Assessments dataframe contains information about each student and the assessments they took during the module

# In[2]:


student_assessment.head()


# ---
# 
# ## Student Assessment Contents
# 
# * **id_assessment**: The assessment ID is the unique identifier for the assessment the student took.
# * **id_student**: The student ID is the unique identifier for the student who took the assessment.
# * **date_submitted**: The date submitted is the date the student submitted the exam relevant to the start date of the module.
# * **is_banked**: Whether the score for the assessment is banked indicates wheter the assessment result was transferred from a previous presentation.
#     - is_banked does indicate that the student took the course previously, but since it is their first score that is retained it is not a confounder and entries with a 1 for is_banked will be kept.
#     - is_banked has no other relevant information though and so can be removed.

# ---
# 
# ## Student Assessments Information

# **Size**

# In[3]:


md(f'''* Number of Rows: {len(student_assessment)}
* Number of Columns: {len(student_assessment.columns)}''')


# **Data Types**

# In[4]:


student_assessment.dtypes


# * id_student and id_assessments are both categorical values and so should be converted to objects

# In[5]:


# converting the data types
student_assessment = student_assessment.astype({'id_assessment': int, 'id_student': int})
student_assessment = student_assessment.astype({'id_assessment': object, 'id_student': object})


# **Null Values**

# In[6]:


# prints the sum of a columns null value
student_assessment.isnull().sum()


# In[7]:


null_score = student_assessment['score'].isnull().sum()


# In[8]:


get_ipython().run_cell_magic('markdown', '', '\n* We have {null_score} null values for score, which we are trying to predict.')


# In[9]:


NaN_scores = student_assessment.loc[student_assessment['score'].isnull() == True]


# In[10]:


NaN_scores


# In[11]:


students_w_NaN_scores = pd.DataFrame()


# In[12]:


for index, row in NaN_scores.iterrows():
    students_w_NaN_scores = students_w_NaN_scores.append(student_info.loc[student_info['id_student'] == row['id_student']])


# In[13]:


students_w_NaN_scores


# In[14]:


students_w_NaN_scores['final_result'].value_counts()


# In[15]:


student_assessment.loc[student_assessment['id_student'] == 631786]


# In[ ]:





# In[16]:


NaN_students_all_exams = pd.DataFrame()


# In[17]:


for index, row in student_assessment.iterrows():
    NaN_students_all_exams = NaN_students_all_exams.append(student_assessment.loc[student_info['id_student'] == row['id_student']])


# **Merged Assessment/Student_info dataframes**

# In order to remove the students that we removed for the number of previous attempts, we must merge assessments and student info and find the difference

# In[ ]:


# merged 'student info/assessments' with a full outer join on their common columns
merged_si_assm = student_assessment.merge(student_info, how='outer', on=['id_student', 'code_module', 'code_presentation'], indicator=True)
merged_si_assm.head()


# For this merge column the right side would be the student info dataframe and the left side would be assessments. If an entry receives the label of right_only there is a student who has no assessments, if the label is left_only, there is an assessment that doesn't match up with a student.

# In[ ]:


# variable for where merge is left_only, and only found on the 
only_assessments = merged_si_assm.loc[merged_si_assm['_merge']=='left_only']
only_student_info = merged_si_assm.loc[merged_si_assm['_merge']=='right_only']


# **Assessments that do not map to students**:

# In[ ]:


only_assessments.head()


# **Students without any test scores**:

# In[ ]:


only_student_info.head()


# In[ ]:


md(f'''
    We have {len(only_assessments)} values in only assessments, which map to students who had made previous attempts which we eliminated, and {len(only_student_info)} values in only student_info, which means we have students for whom we have no test scores.
    We can drop both of these which are missing values for the purpose of this dataframe since we are just analyzing test scores
    ''')


# In[ ]:


# merging assessments with the original student data dataframe to make sure that the missing students are the ones we removed.
merged_test = student_assessment.merge(student_info, how='outer', on=['id_student', 'code_module', 'code_presentation'], indicator=True)

# removing entries where num_prev_attempts == 0
merged_test = merged_test[merged_test['num_of_prev_attempts'] == 0]

# checking if any in only the student info dataframe remain (left_only). No output means all of the tests without students map to a student where num_prev_attempts == 0
merged_test.loc[merged_test['_merge']=='left_only']


# In[ ]:


# removing any student with NaN values in id_assessment or region
merged_si_assm = merged_si_assm.dropna(subset=['id_assessment', 'region'])


# In[ ]:


# reordering dataframe columns to group like data
merged_si_assm = merged_si_assm[['code_module', 'code_presentation', 'id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result', 'id_assessment', 'assessment_type', 'date_submitted', 'date', 'weight', 'score']]


# In[ ]:


# converting the data types back
merged_si_assm = merged_si_assm.astype({'id_assessment': int, 'id_student': int})
merged_si_assm = merged_si_assm.astype({'id_assessment': object, 'id_student': object})


# In[ ]:


# reset the index
merged_si_assm.reset_index(drop=True).head()


# In[ ]:


student_assessment = merged_si_assm


# **Unique Counts**

# In[ ]:


student_assessment.nunique()


# **Unique Categorical Values**

# In[ ]:


unique_vals(student_assessment)


# **Duplicate Values:**

# In[ ]:


duplicate_vals(student_assessment)


# **Statistics**

# In[ ]:


student_assessment.describe()

