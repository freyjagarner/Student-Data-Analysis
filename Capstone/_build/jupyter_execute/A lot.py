#!/usr/bin/env python
# coding: utf-8

# # Student Success Analysis and Prediction
# 
# ---

# In this notebook we will be analyzing the Open University Learning Analytics dataset. This dataset contains information about seven online courses, referred to as modules, the students taking these courses, and their interactions with the courses. There were four seperate presentations of these courses offered in February and October of 2013 and 2014. The analysis of this dataset is done with the goal of discovering relationships between student features, course features, student grades and the overall student outcome. We will begin with exploring the data, which is distributed between seven CSV files, and then apply machine learning algorithms to see what relationships we can tease out. 

# In[1]:


from functions import *

@register_cell_magic
def markdown(line, cell):
    return md(cell.format(**globals()))


# 
# Navigation:
# 
# * Cleaning:
#     * [Student Info](#StudentInfo) 
#     * [Student Registration](#StudentRegistration) 
#     * [Courses](#Courses) 
#     * [Assessments](#Assessments)
#     * [Student Assessment](#StudentAssessment)
#     * [Student VLE](#StudentVLE)
#     * [VLE](#VLE) 
# 

# <h1>Cleaning and Analysis</h1>
# 
# ---
# 
# Let's get to know our data!
# 
# Step by step we will clean and explore the student data here.
# For each dataframe we will first Get a general look at our data frame looking at datatypes, null values, duplicate values, and unique values and perform cleaning based on what we find, then we will explore the information visually

# ---
# 
# <h2>Observations and Cleaning</h2>

# <h3>General</h3>

# In[71]:


# pd.concat(x for _, x in vle.groupby(['id_student',"date"]) if len(x) > 1)[0:50]


# In[246]:





# In[247]:


merged_vle_ass.loc[merged_vle_ass['_merge'] == 'right_only']


# In[248]:


# merged_vle_ass.loc[merged_vle_ass['_merge'] == 'right_only']


# In[249]:


# merged_vle_ass.loc[merged_vle_ass['_merge'] == 'left_only']


# In[250]:


# merged_vle_ass2 = vle.merge(assessments, how='left', on=['code_module', 'code_presentation'],indicator=True).head()


# In[251]:


# merged_vle_ass2 


# In[252]:


# merged_vle_ass2.loc[merged_vle_ass2['_merge'] == 'right_only']


# In[253]:


# merged_vle_ass2.loc[merged_vle_ass2['_merge'] == 'left_only']


# In[254]:


# merged_vle_ass3 = assessments.merge(vle, how='right', on=['code_module', 'code_presentation'],indicator=True).head()


# In[255]:


# merged_vle_ass3 


# In[256]:


# merged_vle_ass3.loc[merged_vle_ass3['_merge'] == 'right_only']


# In[257]:


# merged_vle_ass3.loc[merged_vle_ass3['_merge'] == 'left_only']


# In[258]:


# merged_vle_ass4 = assessments.merge(vle, how='left', on=['code_module', 'code_presentation'],indicator=True).head()


# In[259]:


# merged_vle_ass4


# In[260]:


# merged_vle_ass4.loc[merged_vle_ass4['_merge'] == 'right_only']


# In[261]:


# merged_vle_ass4.loc[merged_vle_ass4['_merge'] == 'left_only']


# In[262]:


# merged_vle_si


# In[263]:


# merged_vle_si.loc[merged_vle_si['_merge'] == 'left_only']


# In[264]:


merged_vle_si = merged_vle_si.dropna(subset=['final_result'])


# In[265]:


vle = merged_vle_si


# In[266]:


vle


# * The data types are acceptable.
# * There are 11 null values in date. The documentation for this dataset states that if the final exam date is missing it is at the end of the last presentation week.

# We will again look at the possible values for our categorical variables:

# ---
# 
# <h4>Assessment Type</h4>
# 

# In[299]:


unique_assessments = assessments['id_assessment'].count()
tma = assessments['assessment_type'].value_counts()['TMA']
cma = assessments['assessment_type'].value_counts()['CMA']
exams = assessments['assessment_type'].value_counts()['Exam']
print(f"There are {unique_assessments} unique assessments\n{tma} are Tutor Marked Assessments (TMA)\n{cma} are Computer Marked Assessments (CMA)\n{exams} are Final Exams (Exam)")


# In[300]:


print(assessments.loc[assessments['assessment_type'] == 'TMA', 'code_presentation'].value_counts())
print()
print(assessments.loc[assessments['assessment_type'] == 'CMA', 'code_presentation'].value_counts())
print()
print(assessments.loc[assessments['assessment_type'] == 'Exam', 'code_presentation'].value_counts())


# <a id='VLE'></a>
# 
# ---
# 
# <h2>VLE Dataframe</h2>
# 
# ---
# 
# <h3>Cleaning</h3>
# 
# ---
# 
# <h4>1. Look at the dataframe</h4>
# 
# ---

# ---
# 
# <h4>2. Remove unnecessary variables</h4>
# 
# ---

# In[118]:


vle = vle[['id_site', 'code_module', 'code_presentation', 'activity_type']]


# In[119]:


vle.head()


# ---
# 
# <h4>3. Explore the dataframe</h4>
# 
# ---
# 
# <h4>Basic Information</h4>

# In[309]:


analyze_df(vle)


# In[314]:


print(vle['activity_type'].explode().unique())


# ---
# 
# <h4>Activity Type</h4>

# In[68]:


print(vle['activity_type'].explode().unique())


# <a id='StudentAssessment'></a>
# 
# ---
# 
# <h2>Student Assessment Dataframe</h2>
# 
# ---
# 
# <h3>Cleaning</h3>
# 
# ---
# 
# <h4>1. Look at the dataframe</h4>
# 
# 

# In[ ]:





# In[141]:


student_info_cm = student_info[['code_module', 'code_presentation', 'id_student']]


# In[142]:


student_info_cm


# In[132]:


merged = student_assessment.merge(student_info, how='right', on=['id_student', ],indicator=True)


# In[133]:


merged.loc[merged['_merge'] == 'right_only']


# In[136]:


merged2 = student_assessment.merge(student_info, how='left', indicator=True)


# In[140]:


merged2.loc[merged2['_merge'] == 'left_only']


# ---
# 
# <h4>2. Remove unnecessary variables</h4>
# 
# ---

# ---
# 
# <h4>3. Explore the dataframe</h4>
# 
# ---
# 
# <h4>Basic Information</h4>

# In[117]:


analyze_df(student_assessment)


# ---
# 
# <h4>Assessment ID</h4>

# ---
# 
# <h4>Student ID</h4>

# In[320]:


student_assessment['id_student'].value_counts()


# ---
# 
# <h4>Date Submitted</h4>

# ---
# 
# <h4>Score</h4>

# In[ ]:


for index, row in student_assessment[student_assessment['score'].isna()].iterrows():
    assessments.at[index, 'date'] = courses.loc[(courses['code_module'] == row['code_module']) & (courses['code_presentation'] == row['code_presentation']), 'module_presentation_length']


# In[319]:


assessment_score_nas = pd.DataFrame()
for i, row in student_assessment[student_assessment['score'].isna()].iterrows():
    print(student_info.loc[(student_info['id_student'] == row['id_student']), 'final_result'])


# In[317]:


assessment_score_nas


# In[123]:


student_assessment[student_assessment['score'].isna()]


# In[125]:


student_info.loc[student_info['id_student'] == 721259]


# In[126]:


student_info.loc[student_info['id_student'] == 260355]


# <a id='MachineLearning'></a>
# 
# <h1>Machine Learning</h1>

# In[267]:


change_col_val(col_dict, student_info)


# In[270]:


student_info = student_info.drop(columns=['date_registration', 'date_unregistration'])


# In[276]:


vle


# In[271]:


student_info


# In[273]:


from sklearn.linear_model import LinearRegression

# create linear regression object
mlr = LinearRegression()

# fit linear regression
mlr.fit(student_info[['gender', 'region']], student_info['final_result'])

# get the slope and intercept of the line best fit.
print(mlr.intercept_)
# -244.92350252069903

print(mlr.coef_)
# [ 5.97694123 19.37771052]


# In[274]:


assessments.head()


# In[275]:


assessments[assessments['region']=='Scotland']


# In[26]:


# list of final_result possibilities
final_results = ['Fail', 'Pass', 'Withdrawn', 'Distinction']

# list of disability possibilities
disability = ['N', 'Y']

# list of region possibilities
regions = ['East Anglian Region', 'North Western Region',
 'South East Region', 'West Midlands Region', 'North Region',
 'South Region', 'South West Region', 'East Midlands Region',
 'Yorkshire Region', 'London Region', 'Wales', 'Scotland', 'Ireland']

# list of highest_education possibilities
highest_ed = ['No Formal quals', 'Lower Than A Level', 'A Level or Equivalent', 'HE Qualification', 'Post Graduate Qualification' ]

# list of imd_band possibilites
imd_bands = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']

# list of age_band possibilities
age_bands = ['0-35', '35-55', '55<=']

# list of code_module possibilities
code_mods = ['2013B', '2013J', '2014B', '2014J']

# list of gender possibilities
genders = ['M', 'F']

# dictionary mapping column string names to the above lists to pass to the change_col_val function
col_dict = {'imd_band':imd_bands, 'region':regions, 'disability':disability, 'age_band':age_bands, 'highest_education':highest_ed, 'gender':genders, 'final_result':final_results}

