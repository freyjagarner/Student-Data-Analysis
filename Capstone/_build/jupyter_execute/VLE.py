#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('capture', '', 'from ipynb.fs.full.Student_Info import student_info_reg\nfrom ipynb.fs.full.Assessments import cleaned_assessments\nfrom functions import *\n\n@register_cell_magic\ndef markdown(line, cell):\n    return md(cell.format(**globals()))\n;')


# ---
# 
# # VLE and Student VLE Dataframes

# ---
# 
# ## VLE
# 
# The VLE dataframe contains information about materials available on the Virtual Learning Environment.

# In[2]:


vle.head()


# ---
# 
# ## VLE Contents
# 
# * **id_site**: The site ID is the unique identifier for the online resource.
# * **code_module**: The code module is the module the resource is associated with.
# * **code_presentation**: The code presentation represents the time the module was held at.
# * **activity_type**: The activity type is the type of online material.
# * **week_from**: The week from is the week the material was intended to be used from.
#     - week_from will not be used in our analysis due to it being irrelevant information and will be dropped.
# * **week_to**: The week to is the week the material was intended to be used until.
#     - week_to will not be used in our analysis due to it being irrelevant information and will be dropped.

# In[130]:


# dropping week_to and week_from from VLE dataframe
vle = vle.drop(columns=['week_from', 'week_to'])


# ---
# 
# ## Student VLE
# 
# The Student VLE Dataframe contains information about student interactions with the online resources in the Virtual Learning Environment.

# In[131]:


student_vle.head()


# ---
# 
# ## Student VLE Contents
# 
# * **code_module**: The code module is the module the resource and student are associated with.
# * **code_presentation**: The code presentation represents the time the module was held at.
# * **id_site**: The site ID is the unique identifier for the online resource with which the student engaged.
# * **date**: The date represents the date that the student engaged with the material relevant to the start date of the module.
# * **sum_click**: The sum click represents the number of clicks the student made on that day.

# ```{note}
# Since we are only interested in information that is pertinent to the student, we will be merging the VLE and Student VLE dataframes to have only the relevant information of each.
# ```

# ## Merged VLE and Student VLE Dataframe

# In[132]:


# merging vle & student vle with a full outer join on common columns
merged_vle = student_vle.merge(vle, how='outer', on=['id_site', 'code_module', 'code_presentation'],indicator=True)
merged_vle.head()


# The added merge column tells us if the data maps perfectly to both dataframes, or if it is only found on the right or left side, the right side in this case being the VLE dataframe and the left side being the student_VLE dataframe

# In[133]:


# makes a dataframe containing only entries where _merge value is not both.
vle_only = merged_vle.loc[merged_vle['_merge'] != 'both']
vle_only.head()


# In[134]:


# checking the unique values of the dataframe. Only right_only
vle_only['_merge'].unique()


# In this case the data either maps perfectly to both or is only found on the right hand side, or the VLE dataframe. This represents materials which we have no student activity associated with which can be dropped along with the _merge column which will have no more interesting information.

# In[135]:


# drop rows which have NaN values for id_student
merged_vle = merged_vle.dropna(subset=['id_student'])

# drop _merge column
merged_vle = merged_vle.drop(columns=['_merge'])

# reset index
merged_vle.reset_index(drop=True).head()


# **Aggregating Clicks**

# * For this analysis we will only be using the sum of the students clicks throughout the course, and so we must add each days clicks per student.

# **Number of activity types**

# * We are going to remove activity_type for now. If sum_clicks overall ends up being a good predictor of how a student does, we will add it back.
# * We will remove id_site for now since it does not add any information to the resource it maps to.

# In[138]:


# removing activity_type and id_site columns
merged_vle = merged_vle.drop(columns=['activity_type', 'id_site'])


# **VLE with clicks per student per module aggregated**

# In[143]:


# gets sum click as total for the whol module. Removes date since no longer relevant.
aggregates = {'sum_click':'sum', 'code_module':'first', 'code_presentation':'first'}
merged_vle = merged_vle.groupby(['id_student']).aggregate(aggregates).reset_index()

# change id_student to int and then object to remove the .0
merged_vle = merged_vle.astype({'id_student': int})
merged_vle = merged_vle.astype({'id_student': object})


# In[144]:


merged_vle = merged_vle[['code_module', 'code_presentation', 'id_student', 'sum_click']]


# **Merge with Student Info Dataframe**

# Finally, we will merge the merged VLE dataframe with the Student info dataframe to ensure wwe are only working with students who were not previously eliminated due to dropping out before the first day or for being on higher than their first attempt

# **Merged VLE and Student Info Dataframes**

# In[145]:


# outer merge of stud_info and vle dataframes on common columns
merged_vle_si = stud_info.merge(merged_vle, how='outer', on=['id_student', 'code_presentation', 'code_module'],indicator=True)

# show head of resulting dataframe
merged_vle_si


# For the _merge column for this dataframe, left_only tells us that the data is only found in student info, and right only tells us the data is only found in VLE.

# In[146]:


only_vle = merged_vle_si.loc[merged_vle_si['_merge'] == 'right_only']
only_vle.head()


# In[147]:


only_stud_info= merged_vle_si.loc[merged_vle_si['_merge'] == 'left_only']
only_stud_info.head()


# In[148]:


md(f'''
    We have {len(only_vle)} values in only the merged vle, which map to students who had made previous attempts, and {len(only_stud_info)} values in only student_info, which means we have students for whom we have no click data.
    We can drop both of these which are missing values for the purpose of this dataframe since having no clicks gives us nothing to analyze.
    ''')


# In[149]:


# merging vle with the original student data dataframe to make sure that the missing students are the ones we removed.
merged_test = merged_vle.merge(student_info, how='outer', on=['id_student', 'code_module', 'code_presentation'], indicator=True)

# removing entries where num_prev_attempts == 0
merged_test = merged_test[merged_test['num_of_prev_attempts'] == 0]

# checking if any in only the student info dataframe remain (left_only). No output means all of the tests without students map to a student where num_prev_attempts == 0
merged_test.loc[merged_test['_merge']=='left_only']


# In[165]:


# removing any entries where the region or sum click are NaN
merged_vle_si = merged_vle_si.dropna(subset=['region', 'sum_click'])

# reordering the data for clarity
cleaned_vle = merged_vle_si[['code_module', 'code_presentation',  'id_student', 'region', 'imd_band', 'age_band','gender','highest_education', 'disability', 'sum_click', 'final_result']]


# In[166]:


cleaned_vle


# **Merge with Assessments Dataframe**

# Finally we will be creating a merged dataframe of the the merged vle and student info and assessments dataframes. This is so that we can attempt to predict scores based on number of clicks.

# In[162]:


merged_vle_assm = assessments_final.merge(merged_vle_si, how='outer', on=['code_module', 'code_presentation', 'id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result'],indicator=True)
merged_vle_assm


# This dataframe is a full outer merge on our cleaned assessments dataframe and our cleaned VLE dataframe

# In[160]:


merged_vle_assm.loc[merged_vle_assm['_merge'] == 'left_only']


# In[161]:


merged_vle_assm.loc[merged_vle_assm['_merge'] == 'right_only']


# In[159]:


merged_vle_assm = merged_vle_assm.dropna(subset=['sum_click', 'id_assessment'])
merged_vle_assm = merged_vle_assm.drop(columns=['_merge'])


# In[167]:


cleaned_assessments = merged_vle_assm[['code_module', 'code_presentation','id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'sum_click', ]]


# In[196]:


aggregates = {'score':'sum', 'code_module':'first', 'code_presentation':'first', 'weight': 'sum'}
score_test = cleaned_assessments.groupby(['id_student']).aggregate(aggregates).reset_index()
score_test.loc[score_test['weight']>=200]


# **Data Types:**

# In[197]:


student_info.loc[student_info['id_student'] ==8462.0]


# In[179]:


student_assessment.loc[student_assessment['id_student'] ==8462.0]


# In[182]:


assessments.loc[assessments['id_assessment'] == 25365]


# In[120]:


vle.dtypes


# In[198]:


assessments


# In[ ]:




