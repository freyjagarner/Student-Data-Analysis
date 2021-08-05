#!/usr/bin/env python
# coding: utf-8

# <h1>Put a badass title here</h1>
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

# * Though the number of previous attempts may be interesting to analyze on its own to see the relationship between students who had to take the course multiple times, and the differences in their bahavior on the second or higher attempt, here we are only interested in students on their first attempt. The reason is that familiarity with course content is a confounding variable. Due to this we will remove students on their second or higher attempt. We will then remove num_prev_attempts since it will not contain any interesting data.
# * studied_credits will not be a part of our analysis, and so may be removed.
# * The dataframe columns can be reordered to keep relevent data together. 

# In[2]:


# changing the student info dataframe to include only records where num_prev_attempts is 
student_info = student_info[student_info['num_of_prev_attempts'] == 0]


# In[3]:


# reordering the student_info dataframe to keep country, module and student data together
student_info = student_info[['code_module', 'code_presentation', 'id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result']]


# * The student registration dataframe matches 1:1 with the student_info dataframe only adding the date the student registered and the date, if applicable, they unregistered, and so we will merge these two dataframes

# In[4]:


# left join and merge student info with student registration
student_info = student_info.merge(student_registration, how='left', on=['code_module', 'code_presentation', 'id_student'])


# <h3>Datatypes</h3>

# In[5]:


# show student info data types
student_info.dtypes


# * id_student is currently an int64 datatype, but would be more appropriate as an object data type since it is categorical.

# In[6]:


# changing id_student to the object data type
student_info['id_student'] = student_info['id_student'].astype(object)


# <h3>Null Values</h3>

# In[7]:


# print the sum of null values in each column
student_info.isnull().sum()


# * The imd_band variable has 990 null values which we may have to work around. 
# * There are 19,809 null values for date_unregistration which represent the students that did not withdraw from the course.
# * We have 38 null values for date_registration, and no mention of this in the dataset documentation, so we will treat this as missing data.

# <h3>Numerical Analysis</h3>

# In[8]:


len(student_info.index)


# In[9]:


student_info.describe().astype(int)


# * There are 8,612 values for the count of date_unregistration which represents the number of students who withdrew from the course.
# * The earliest date_unregistration date is 274 days before the course began, which means these students did not make it to the first day. We are only interested in students who took the course so we must eliminate students who did not attend.

# In[10]:


# removing students who withdrew on or before the first day
student_info = student_info.drop(student_info[(student_info['date_unregistration'] <= 0)].index)
student_info.reset_index(drop=True).head()


# * Also notable is that the latest unregistration date is far beyond the date any of the courses went on for.

# In[11]:


# finds the longest module length in courses and prints it
longest_course = courses['module_presentation_length'].max()
md(f"Longest Course: {longest_course} days")


# In[12]:


# finding students whose courses went on for longer than the maximum course length
student_info.loc[student_info['date_unregistration'] > 269]


# This seems to be an outlier, but should not affect our overall analysis so we will leave this intact

# In[13]:


student_info.nunique()


# The dataframe length is 341,052 but there are only 26,096 unique student ID's. There are no duplicate records, so these students are likely enrolled in other courses at the same or different times.

# In[14]:


student_info[student_info['id_student'].duplicated()]


# In[15]:


# finding student records with duplicate ID's
pd.concat(x for _, x in student_info.groupby("id_student") if len(x) > 1)


# We have 1956 students whose ID is listed more than once and a total of 3906 duplicate records. These do seem to be in different courses, and so we will leave them

# In imd_bands the % sign is missing in 10-20. We will add that for consistency and clarity

# In[16]:


# changing all 10-20 values in student_info imd_band to 10-20% for consistency's sake
student_info.loc[student_info['imd_band'] == '10-20', 'imd_band'] = '10-20%'
print(student_info['imd_band'].explode().unique())


# After this cleaning we are down to 25,760 relevent records

# ---
# 
# Let's take a look at the possible values for our categorical variables:

# In[17]:


unique_vals(student_info)


# In[18]:


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


# <a id='Assessments'></a>
# 
# ---
# 
# <h2>Assessments Dataframe</h2>
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

# In[19]:


assessments.head()


# In[20]:


student_assessment.head()


# In[21]:


student_assessment = student_assessment.drop(columns='is_banked')


# ---
# 
# <h4>2. Remove unnecessary variables</h4>
# 
# ---
# 

# We will merge the student_assessment and assessments dataframes, matching the records by the assessment ID to have one dataframe with the assessment information.

# In[22]:


# merges dataframes student_assessment with assessments with a right join on their common ID id_assessment
# creates a colum _merge which tells you if the id_assessment was found in one or both dataframes
merged_assessments = student_assessment.merge(assessments, how='outer', on=['id_assessment'],indicator=True)
merged_assessments.head()


# In[23]:


merged_assessments.loc[merged_assessments['_merge'] == 'right_only']


# This subset consists of exams which exist in assessments, but none of the students in student_assessment have taken. Since there is no student data mapped to these exams we will drop them.

# In[24]:


# remove tests that students did not take
assessments = merged_assessments.dropna(subset=['id_student'])
# reset the index to be consecutive again
assessments = assessments.reset_index(drop=True)


# In[25]:


assessments.head()


# Now we have a dataframe of students which we have the exam data for mapped to the exam type, date and weight

# In[26]:


assessments[assessments['date'].isna()].head()


# We have 2,873 null data points for assessment date. The documentation of this dataset states that if the exam date is missing then it is as the end of the last presentation week. We can find this information in the courses dataframe.

# In[27]:


# adding the dates for the null test dates
for index, row in assessments[assessments['date'].isna()].iterrows():
    assessments.at[index, 'date'] = courses.loc[(courses['code_module'] == row['code_module']) & (courses['code_presentation'] == row['code_presentation']), 'module_presentation_length']


# In[28]:


assessments = assessments[['code_module', 'code_presentation', 'id_student', 'id_assessment', 'assessment_type', 'weight', 'date', 'date_submitted', 'score']]


# There are 173 records with missing scores. These are not of much interest to us, since score is what we are trying to find the relationship for.

# In[29]:


assessments = assessments.dropna(subset=['score'])


# In[30]:


# converting the data types back
assessments = assessments.astype({'id_assessment': object, 'id_student': object})


# In[31]:


assessments.head()


# In[32]:


analyze_df(assessments)


# In order to remove the students that we removed for the number of previous attempts, we must merge assessments and student info and find the difference

# In[33]:


merged_sia = assessments.merge(student_info, how='outer', on=['id_student', 'code_module', 'code_presentation'], indicator=True)
merged_sia.head()


# In[34]:


merged_sia.loc[merged_sia['_merge'] == 'right_only']


# In[35]:


assessments = merged_sia.dropna(subset=['final_result', 'id_assessment'])


# In[36]:


assessments.reset_index(drop=True)


# In[37]:


assessments.loc[assessments['_merge'] == 'left_only']


# In[38]:


assessments = assessments.drop(columns='_merge')


# In[39]:


analyze_df(assessments)


# In[40]:


vle = vle.drop(columns=['week_from', 'week_to'])


# In[41]:


# merging vle & student vle
merged_vle = student_vle.merge(vle, how='outer', on=['id_site', 'code_module', 'code_presentation'],indicator=True)


# In[42]:


merged_vle.loc[merged_vle['_merge'] == 'right_only']


# This represents materials which we have no student activity associated withh

# In[43]:


merged_vle = merged_vle.dropna(subset=['id_student'])


# In[44]:


merged_vle = merged_vle.drop(columns=['_merge'])


# In[45]:


vle = merged_vle


# In[46]:


vle.head()


# In[47]:


analyze_df(vle)


# In[48]:


vle = vle.reset_index(drop=True)


# In[49]:


# pd.concat(x for _, x in vle.groupby(['id_student',"date"]) if len(x) > 1)[0:50]


# In[50]:


aggregates = {'sum_click':'sum', 'code_module':'first', 'code_presentation':'first'}


# In[51]:


vle = vle.groupby(['id_student']).aggregate(aggregates).reset_index()


# In[52]:


vle.head()


# In[53]:


merged_vle_si = student_info.merge(vle, how='outer', on=['id_student', 'code_module', 'code_presentation'],indicator=True)


# In[54]:


merged_vle_si


# In[55]:


merged_vle_si.loc[merged_vle_si['_merge'] == 'left_only']


# In[56]:


merged_vle_si = merged_vle_si.dropna(subset=['region'])
merged_vle_si = merged_vle_si.dropna(subset=['sum_click'])


# In[57]:


merged_vle_si


# In[58]:


vle = merged_vle_si[['code_module', 'code_presentation', 'region', 'imd_band', 'id_student', 'age_band','gender','highest_education', 'disability', 'sum_click', 'final_result']]


# In[59]:


vle


# In[60]:


vle['sum_click'] = vle['sum_click'].astype(int)
vle['id_student'] = vle['id_student'].astype(int)
vle['id_student'] = vle['id_student'].astype(object)


# In[61]:


analyze_df(vle)


# In[62]:


vle


# In[63]:


merged_vle_ass = assessments.merge(vle, how='outer', on=['code_module', 'code_presentation', 'id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result'],indicator=True)


# In[64]:


merged_vle_ass


# In[65]:


merged_vle_ass.loc[merged_vle_ass['_merge'] == 'left_only']


# In[66]:


merged_vle_ass = assessments.merge(vle, how='outer', on=['code_module', 'code_presentation', 'id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result'],indicator=True).head()


# In[67]:


analyze_df(merged_vle_ass)


# In[68]:


merged_vle_ass


# In[69]:


merged_vle_ass.loc[merged_vle_ass['_merge'] == 'left_only']


# In[70]:


merged_vle_ass.loc[merged_vle_ass['_merge'] == 'right_only']


# In[71]:


# merged_vle_ass.loc[merged_vle_ass['_merge'] == 'right_only']


# In[72]:


# merged_vle_ass.loc[merged_vle_ass['_merge'] == 'left_only']


# In[73]:


# merged_vle_ass2 = vle.merge(assessments, how='left', on=['code_module', 'code_presentation'],indicator=True).head()


# In[74]:


# merged_vle_ass2 


# In[75]:


# merged_vle_ass2.loc[merged_vle_ass2['_merge'] == 'right_only']


# In[76]:


# merged_vle_ass2.loc[merged_vle_ass2['_merge'] == 'left_only']


# In[77]:


# merged_vle_ass3 = assessments.merge(vle, how='right', on=['code_module', 'code_presentation'],indicator=True).head()


# In[78]:


# merged_vle_ass3 


# In[79]:


# merged_vle_ass3.loc[merged_vle_ass3['_merge'] == 'right_only']


# In[80]:


# merged_vle_ass3.loc[merged_vle_ass3['_merge'] == 'left_only']


# In[81]:


# merged_vle_ass4 = assessments.merge(vle, how='left', on=['code_module', 'code_presentation'],indicator=True).head()


# In[82]:


# merged_vle_ass4


# In[83]:


# merged_vle_ass4.loc[merged_vle_ass4['_merge'] == 'right_only']


# In[84]:


# merged_vle_ass4.loc[merged_vle_ass4['_merge'] == 'left_only']


# In[85]:


# merged_vle_si


# In[86]:


# merged_vle_si.loc[merged_vle_si['_merge'] == 'left_only']


# In[87]:


merged_vle_si = merged_vle_si.dropna(subset=['final_result'])


# In[88]:


vle = merged_vle_si


# In[89]:


vle


# * The data types are acceptable.
# * There are 11 null values in date. The documentation for this dataset states that if the final exam date is missing it is at the end of the last presentation week.

# We will again look at the possible values for our categorical variables:

# ---
# 
# <h4>Code Module</h4>
# 

# ---
# 
# <h4>Code Presentation</h4>
# 

# ---
# 
# <h4>Assessment ID</h4>
# 

# ---
# 
# <h4>Assessment Type</h4>
# 

# In[90]:


unique_assessments = assessments['id_assessment'].count()
tma = assessments['assessment_type'].value_counts()['TMA']
cma = assessments['assessment_type'].value_counts()['CMA']
exams = assessments['assessment_type'].value_counts()['Exam']
print(f"There are {unique_assessments} unique assessments\n{tma} are Tutor Marked Assessments (TMA)\n{cma} are Computer Marked Assessments (CMA)\n{exams} are Final Exams (Exam)")


# In[91]:


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

# In[92]:


vle.head()


# ---
# 
# <h4>2. Remove unnecessary variables</h4>
# 
# ---

# In[93]:


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
# <h4>Code Module</h4>

# In[ ]:





# ---
# 
# <h4>Code Presentation</h4>

# In[ ]:





# ---
# 
# <h4>Student ID</h4>

# In[ ]:





# ---
# 
# <h4>Site ID</h4>

# In[ ]:





# ---
# 
# <h4>Date</h4>

# In[ ]:





# ---
# 
# <h4>Sum Click</h4>

# In[ ]:





# ---
# 
# <h4>Site ID</h4>

# ---
# 
# <h4>Code Module</h4>

# ---
# 
# <h4>Code Presentation</h4>

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


# In[ ]:





# In[ ]:





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


# In[ ]:




