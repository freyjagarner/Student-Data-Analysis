#!/usr/bin/env python
# coding: utf-8

# <h1>Put a badass title here</h1>
# 
# ---

# In this notebook we will be analyzing the Open University Learning Analytics dataset. This dataset contains information about seven courses referred to as module, the students taking these courses, and their interactions with the courses. These courses were taken over the course of two years and offered Febuary and October of 2013 and 2014. The analysis of this dataset is done with the goal of discovering relationships between student features, course features and the overall student outcome. We will begin with exploring the data, which is distributed between seven CSV files, and then apply machine learning algorithms to see what relationships we can tease out. 

# In[1]:


# import statements
import pandas as pd
import numpy as np
import os
from sklearn import linear_model
import seaborn as sns
import itertools
from varname.helpers import Wrapper
import matplotlib.pyplot as plt


# In[99]:


# setting the path to the csv files
path = os.path.join(os.path.abspath(os.getcwd()), 'csvs\\')

student_info = pd.read_csv(path+'studentInfo.csv')
student_registration = pd.read_csv(path+'studentRegistration.csv')
courses = pd.read_csv(path+'courses.csv')
assessments = pd.read_csv(path+'assessments.csv')
student_assessment = pd.read_csv(path+'studentAssessment.csv')
student_vle = pd.read_csv(path+'studentVle.csv')
vle = pd.read_csv(path+'vle.csv')




# In[100]:


# a fuction to print some basic analysis of dataframes
def analyze_df(df):
    print(f"Dataframe Length:\n\n{len(df)}\n\n")
    # print dataframe column data types
    print(f"Data Types:\n\n{df.dtypes}\n\n")
    # print which columns have null values and how many
    print(f"Null Data:\n\n{df.isnull().sum()}\n\n")
    # print the number of unique values per variable in data
    print(f"Unique Values:\n\n{df.nunique()}\n\n")
    # print duplicate values if there are any else prints "No Duplicate Values"
    if not df[df.duplicated()].empty:
        print(f"Duplicate Values:\n\n{df[df.duplicated()]}\n\n")
    else:
        print("No Duplicate Values")
    print(f"Numerical Variable Analysis:\n\n{df.describe()}\n\n")
    

#print the unique values of each column in a dataframe
def unique_vals(df):
    for i in df.columns:
        print(f"{i}: {df[i].explode().unique()}\n")
# a function to change dataframe column values based on a given dictionary
def change_col_val(val_dict, df):
    # val_dict is a dictionary of lists 
    for k, v in val_dict.items():
        for i in v:
            # change the value of the cell to its index number in a list
            df.loc[df[k] == i, k] = v.index(i)
            
# a function to get a percentage
def percentage(part, whole):
  return round(100 * float(part)/float(whole), 2)


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

# <a id='Courses'></a>
# 
# ---
# 
# <h2>Courses Dataframe</h2>
# 
# ---
# 
# <h3>Cleaning</h3>
# 
# ---
# 
# <h4>1. First Look</h4>
# 
# ---

# In[101]:


courses.head()


# <b><u>Contents:</u></b>
# 
# * <b>code_module</b>: The code module represents the code name of the course. Modules are identified with three capital letters which run sequentially between AAA and GGG
# * <b>code_presentation</b>: The code presentations are codified by their year and offering semester. B is for February and J is for October. 2013B for example is February of 2013. 
# * <b>mode_presentation_length</b>: The module presentation length is the length of the course in days.

# In[102]:


analyze_df(courses)


# In[103]:


pd.crosstab(index=courses['code_module'], columns=courses['code_presentation'])


# <a id='StudentInfo'></a>
# 
# <h2>Student Info Dataframe</h2>
# 
# ---
# 
# <h3>Cleaning</h3>
# 
# ---
# 
# <h4>1. First Look</h4>
# 
# ---

# In[104]:


# looking at the student_info dataframe
student_info.head()


# <b><u>Contents:</u></b>
# 
# * <b>code_module</b>: The code module represents the course the student is taking.
# * <b>code_presentation</b>: The code presentations are the year and semester the student is taking the course.
# * <b>id_student</b>: The student ID is a unique identifier for each student
# * <b>gender</b>: The gender represents the binary gender of a student 'M' for students who identify as male and 'F' for students who identify as female.
# * <b>region</b>: Region represents the location of the student when they took the module. All regions are in the UK, Scotland, Ireland or Wales.
# * <b>highest_education</b>: Highest education is representative of a students highest level of formal academic achievement.
#     - Education levels in order from least to most formal education: 
#         - No formal quals (qualifications)
#         - Lower than A Level which is nearly but not quite analagous to under high school level
#         - A Level or equivalent which is again nearly analagous to high school level, but more like college ready
#         - HE Qualification which stands for higher education qualification
#         - Post Graduate Qualification
# * <b>imd_band</b>: The imd_band represents the Indices of multiple deprivation (IMD) score which is a commonly used method in the UK to measure poverty or deprivation in an area. The lower the score, the more 'deprived' the area is.
# * <b>age_band</b>: There are only three bins for age; 0-35, 35-55 and over 55
# * <b>num_of_prev_attempts</b>: The number of times the student has attempted the course previously.
# * <b>studied_credits</b>: The number of credits for the module the student is taking.
# * <b>disability</b>: Disability status is represented by a binary 'Y', yes a student does identify as having a disability and 'N', no a student does not identify as having a disability.
# * <b>final_results</b>: * The final result is the students overall result in the class.
#     - Possible Results include:
#          - Pass: The student passed the course
#          - Fail: The student did not pass the course
#          - Withdraw: The student withdrew before the course term ended
#          - Distinction: The student passed the class with distinction

# studied_credits will not be a part of our analysis, and so may be removed.
# 
# Though the number of previous attempts may be interesting to analyze on its own to see the relationship between students who had to take the course multiple times, and the differences in their bahavior on the second or higher attempt, here we are only interested in students on their first attempt. The reason is that familiarity with course content is a confounding variable. Due to this we will remove students on their second or higher attempt. We will then remove num_prev_attempts since it will not contain any interesting data.
# 
# The dataframe columns can also be reordered to keep relevent data together. 

# ---
# 
# A Quick Aside to the Student Registration Dataframe!
# 
# ---

# In[105]:


student_registration.head()


# <b><u>New Contents:</u></b>
# * <b>date_registration</b> is the date that the student registered for the module relative to the start of the module. A negative value indicates that many days before the module began.
#  
# * <b>date_unregistration</b> is the date that the student unregistered from the course module in relation to the start date of the course. 
# 
# The student registration dataframe matches 1:1 with the student_info dataframe only adding the date the student registered and the date, if applicable, they unregistered, and so we will merge these two dataframes

# In[106]:


student_info = student_info[student_info['num_of_prev_attempts'] == 0]


# In[107]:


student_info = student_info[['code_module', 'code_presentation', 'id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result']]


# In[108]:


student_info = student_info.merge(student_registration, how='left', on=['code_module', 'code_presentation', 'id_student'])


# In[109]:


student_info.head()


# In[110]:


# printing basic analysis of dataframe
print("Student Info\n")
analyze_df(student_info)


# Notes:
# 
# * The imd_band variable has 990 null values which we may have to work around. 
# * There are 19,809 null values for date_unregistration which represent the students that did not withdraw from the course. 
# * There are 8,612 values for the count of unregistration which represents the number of students who withdrew from the course.
# * We have 38 null values for date_registration, and no mention of this in the dataset documentation, so we will treat this as missing data.

# id_student is currently an int64 datatype, but would be more appropriate as an object data type since it is categorical.

# In[111]:


# changing id_student to the object data type
student_info['id_student'] = student_info['id_student'].astype(object)


# The earliest unregistration date is 274 days before the course began, and so we must eliminate students who did not attend the course.

# In[112]:


# removing students who withdrew on or before the first day
student_info = student_info.drop(student_info[(student_info['date_unregistration'] <= 0)].index)
student_info.reset_index()


# The latest unregistration date is far beyond the date any of the courses went on for.

# In[113]:


longest_course = courses['module_presentation_length'].max()
print(f"Longest Course: {longest_course} days")

# finding students whose courses went on for longer than the maximum course length
student_info.loc[student_info['date_unregistration'] > 269]


# This seems to be an outlier, but should not affect our overall analysis so we will leave this intact

# The dataframe length is 28,421 but there are only 26,096 unique student ID's. There are no duplicate records, so these students are likely enrolled in other courses at the same or different times.

# In[114]:


student_info[student_info['id_student'].duplicated()]


# In[115]:


# finding student records with duplicate ID's
pd.concat(x for _, x in student_info.groupby("id_student") if len(x) > 1)


# We have 1956 students whose ID is listed more than once and a total of 3906 duplicate records. These do seem to be in different courses, and so we will leave them

# In[116]:


analyze_df(student_info)


# In[117]:


# changing all 10-20 values in student_info imd_band to 10-20% for consistency's sake
student_info.loc[student_info['imd_band'] == '10-20', 'imd_band'] = '10-20%'
print(student_info['imd_band'].explode().unique())


# After this cleaning we are down to 25,760 relevent records

# ---
# 
# Let's take a look at the possible values for our categorical variables:

# In[118]:


unique_vals(student_info)


# The 10-20 range for imd_band is missing its % sign. We will add that in for consistenct and clarity

# In[119]:


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


# ---
# 
# <h5>Code Modules</h5>
# 
# * Here we will figure out how many students are in each course. The frequency of each course is equivalent to the amount of students in the courses since the student ID's are unique.

# In[120]:


student_info[['code_module']].value_counts(sort=False)


# In[121]:


ax = sns.countplot(x="code_module", data=student_info)


# ---
# 
# <h5>Code Presentations</h5>
# 
# * The code presentation is the year and time of year the courses were offered. These are codified by the year they were offered (2013 or 2014) and the semester they were offered (February represented as B and October represented as J)
# * For the code presentations, the data owner recommends that B and J presentations be analyzed seperately as the presentations may have been different. In some cases though, the author states it is necessary to supplement B with J material in vice versa in CCC EEE and GGG modules. We shall see how this affects our analysis later on.
# * Here we will see how many students are in each presentation. The frequency of each presentation is also equivalent to the amount of students in the courses since the student ID's are unique.

# In[157]:


student_info[['code_presentation']].value_counts(sort=False)


# In[387]:


ax = sns.countplot(x="code_presentation", data=student_info, order=code_mods)


# In[388]:


student_info.head()


# ---
# 
# <h5>Region</h5>
# 
# 
# * Here we will see how many students we have from each region

# In[389]:


student_info[['region']].value_counts()


# In[390]:


fig_dims = (28, 10)
fig, ax = plt.subplots(figsize=fig_dims)
sorted_regions = student_info['region'].value_counts().sort_values(ascending=False).index.values
ax = sns.countplot(x="region", data=student_info, order=sorted_regions)


# ---
# 
# <h5>IMD Band</h5>
# 
# 
# * As mentioned above, the imd_band variable has 1,111 null values and those values will not be counted in this analysis.

# In[391]:


# getting the count of students we have the information for and figuring out what percent of total students that is
total_imd = student_info['imd_band'].count()
percentage_imd = percentage(total_imd, total_students)
print(f"We have IMD information for {total_imd} students, which is {percentage_imd}% of our students.")


# In[392]:


# looking at the counts of students in each range
student_info[['imd_band']].value_counts()


# In[393]:


# figuring out how many students fall under the 50% range
# only counting up to 40-50% mark for our data
total_imd_under_50 = 0
for i in imd_bands[0:5]:
    total_imd_under_50 += student_info[['imd_band']].value_counts()[i]

# getting our imd number as a percentage
perc_imd_under_50 = percentage(total_imd_under_50, total_imd)

print(f"{perc_imd_under_50}% of students come from areas under the 50% IMD figure")


# In[394]:


# plotting imd data
fig_dims = (15, 8)
fig, ax = plt.subplots(figsize=fig_dims)
ax = sns.countplot(x="imd_band", data=student_info, order=imd_bands)


# This graph shows that the bulk of our students are from areas under the 50% mark for the meausurement, so we have more students from more impoverished areas than not.
# 
# This information can be important in assuming certain priviliged knowledge or skills among students, which could give some students an unfair advantage.

# ---
# 
# <h5>Age Bands</h5>
# 

# In[395]:


student_info[['age_band']].value_counts()


# In[396]:


# plotting imd data
ax = sns.countplot(x="age_band", data=student_info, order=age_bands)


# ---
# 
# <h5>Gender</h5>
# 
# * Here we will see our gender ratio and counts:

# In[397]:


# getting the number of males and females in our dataframe
males = student_info[['gender']].value_counts()['M']
females = student_info[['gender']].value_counts()['F']

# figuring out the percentage of males and females to the whole
percentage_males = percentage(males, total_students)
percentage_females = percentage(females, total_students)


# In[398]:


print(f"{males} or {percentage_males}% of the students are male.")
print(f"{females} or {percentage_females}% of the students are female.")


# In[399]:


# plotting the gender distribution
ax = sns.countplot(x="gender", data=student_info)


# 
# * We have more males than females in this dataset, but a fairly every distribution
# 

# ---

# <h5>Highest Education</h5>

# In[400]:


student_info[['highest_education']].value_counts()


# In[401]:


fig_dims = (15, 8)
fig, ax = plt.subplots(figsize=fig_dims)
ax = sns.countplot(x="highest_education", data=student_info, order=highest_ed)


# In[402]:


student_info[['highest_education']].value_counts().plot.pie(autopct="%.1f%%", subplots=True);


# ---
# 
# <h5> Disability Status</h5>
# 
# * Knowing how many differently abled students make up you class is important in order to better understand and accommadate different needs.

# In[403]:


# getting the number and percentage of students who identified as having a disability
number_disability = student_info[['disability']].value_counts()['Y']
percentage_disability = percentage(number_disability, total_students)

print(f"{number_disability} students or {percentage_disability}% of students identify as disabled.")


# In[404]:


ax = sns.countplot(x="disability", data=student_info)


# ---
# 
# <h5>Final Result</h5>
# 
# 

# In[405]:


student_info[['final_result']].value_counts()


# In[406]:


ax = sns.countplot(x="final_result", data=student_info)


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

# In[122]:


assessments.head()


# In[123]:


student_assessment.head()


# In[124]:


student_assessment = student_assessment.drop(columns='is_banked')


# ---
# 
# <h4>2. Remove unnecessary variables</h4>
# 
# ---
# 

# We will merge the student_assessment and assessments dataframes, matching the records by the assessment ID to have one dataframe with the assessment information.

# In[125]:


# merges dataframes student_assessment with assessments with a right join on their common ID id_assessment
# creates a colum _merge which tells you if the id_assessment was found in one or both dataframes
merged_assessments = student_assessment.merge(assessments, how='right', on=['id_assessment'],indicator=True)
merged_assessments.head()


# In[126]:


merged_assessments.loc[merged_assessments['_merge'] == 'right_only']


# This subset consists of exams which exist in assessments, but none of the students in student_assessment have taken. Since there is no student data mapped to these exams we will drop them.

# In[127]:


# remove tests that students did not take
assessments = merged_assessments.dropna(subset=['id_student'])
# reset the index to be consecutive again
assessments = assessments.reset_index(drop=True)


# In[128]:


assessments.head()


# Now we have a dataframe of students which we have the exam data for mapped to the exam type, date and weight

# In[129]:


assessments[assessments['date'].isna()]


# In[130]:


analyze_df(assessments)


# We have 2,873 null data points for assessment date. The documentation of this dataset states that if the exam date is missing then it is as the end of the last presentation week. We can find this information in the courses dataframe.

# In[131]:


# adding the dates for the null test dates
for index, row in assessments[assessments['date'].isna()].iterrows():
    assessments.at[index, 'date'] = courses.loc[(courses['code_module'] == row['code_module']) & (courses['code_presentation'] == row['code_presentation']), 'module_presentation_length']


# In[132]:


assessments = assessments[['code_module', 'code_presentation', 'id_student', 'id_assessment', 'assessment_type', 'weight', 'date', 'date_submitted', 'score']]


# There are 173 records with missing scores. These are not of much interest to us, since score is what we are trying to find the relationship for.

# In[133]:


assessments = assessments.dropna(subset=['score'])


# In[134]:


# converting the data types back
assessments = assessments.astype({'id_assessment': object, 'id_student': object})


# In[135]:


assessments.head()


# In[136]:


analyze_df(assessments)


# In order to remove the students that we removed for the number of previous attempts, we must merge assessments and student info and find the difference

# In[137]:


merged_sia = assessments.merge(student_info, how='left', on=['id_student', 'code_module', 'code_presentation'], indicator=True)
merged_sia


# In[138]:


merged_sia.loc[merged_sia['_merge'] == 'left_only']


# In[139]:


assessments = merged_sia.dropna(subset=['final_result'])


# In[140]:


assessments.reset_index(drop=True)


# In[141]:


assessments = assessments.drop(columns='_merge')


# In[142]:


analyze_df(assessments)


# In[ ]:





# * Put this up with student info

# In[143]:


# student_info = student_info.drop(columns=['date_registration', 'date_unregistration'])


# In[144]:


student_info


# In[145]:


assessments


# In[146]:


no_test_scores = assessments.merge(student_info, how='right', on=['id_student', 'code_module', 'code_presentation', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result', 'date_registration', 'date_unregistration'], indicator=True)
no_test_scores = no_test_scores.loc[no_test_scores['_merge'] == 'right_only']


# In[147]:


no_test_scores


# In[148]:


no_test_scores[no_test_scores['final_result']=='Pass']


# In[149]:


student_info


# In[152]:


vle = vle.drop(columns=['week_from', 'week_to'])


# In[153]:


# merging vle & student vle
merged_vle = student_vle.merge(vle, how='right', on=['id_site', 'code_module', 'code_presentation'],indicator=True)


# In[154]:


merged_vle.loc[merged_vle['_merge'] == 'right_only']


# This represents materials which we have no student activity associated withh

# In[155]:


merged_vle = merged_vle.dropna(subset=['id_student'])


# In[156]:


merged_vle = merged_vle.drop(columns=['_merge'])


# In[157]:


vle = merged_vle


# In[158]:


vle.head()


# In[159]:


analyze_df(vle)


# In[160]:


vle = vle.reset_index(drop=True)


# In[161]:


# pd.concat(x for _, x in vle.groupby(['id_student',"date"]) if len(x) > 1)[0:50]


# In[162]:


aggregates = {'sum_click':'sum', 'code_module':'first', 'code_presentation':'first'}


# In[163]:


vle = vle.groupby(['id_student']).aggregate(aggregates).reset_index()


# In[164]:


vle.head()


# In[165]:


merged_vle_si = student_info.merge(vle, how='right', on=['id_student', 'code_module', 'code_presentation'],indicator=True)


# In[166]:


merged_vle_si


# In[167]:


assessments


# In[168]:


merged_vle_si.loc[merged_vle_si['_merge'] == 'right_only']


# In[169]:


merged_vle_si = merged_vle_si.dropna(subset=['region'])


# In[170]:


merged_vle_si


# In[188]:


student_info


# In[195]:


vle = merged_vle_si[['code_module', 'code_presentation', 'region', 'imd_band', 'id_student', 'age_band','gender','highest_education', 'disability', 'sum_click', 'final_result']]


# In[196]:


vle


# In[203]:


vle['sum_click'] = vle['sum_click'].astype(int)


# In[209]:


vle['id_student'] = vle['id_student'].astype(int)
vle['id_student'] = vle['id_student'].astype(object)


# In[210]:


analyze_df(vle)


# In[236]:


vle


# In[239]:


merged_vle_ass = assessments.merge(vle, how='left', on=['code_module', 'code_presentation', 'id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result'],indicator=True)


# In[240]:


merged_vle_ass


# In[ ]:





# In[230]:


merged_vle_ass.loc[merged_vle_ass['_merge'] == 'left_only']


# No missing VLE data for students in assessments

# In[231]:


merged_vle_ass = assessments.merge(vle, how='right', on=['code_module', 'code_presentation', 'id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result'],indicator=True).head()


# In[241]:


analyze_df(merged_vle_ass)


# In[223]:


merged_vle_ass


# In[224]:


merged_vle_ass.loc[merged_vle_ass['_merge'] == 'left_only']


# In[225]:


merged_vle_ass.loc[merged_vle_ass['_merge'] == 'right_only']


# In[176]:


# merged_vle_ass.loc[merged_vle_ass['_merge'] == 'right_only']


# In[177]:


# merged_vle_ass.loc[merged_vle_ass['_merge'] == 'left_only']


# In[178]:


# merged_vle_ass2 = vle.merge(assessments, how='left', on=['code_module', 'code_presentation'],indicator=True).head()


# In[179]:


# merged_vle_ass2 


# In[180]:


# merged_vle_ass2.loc[merged_vle_ass2['_merge'] == 'right_only']


# In[181]:


# merged_vle_ass2.loc[merged_vle_ass2['_merge'] == 'left_only']


# In[182]:


# merged_vle_ass3 = assessments.merge(vle, how='right', on=['code_module', 'code_presentation'],indicator=True).head()


# In[183]:


# merged_vle_ass3 


# In[184]:


# merged_vle_ass3.loc[merged_vle_ass3['_merge'] == 'right_only']


# In[185]:


# merged_vle_ass3.loc[merged_vle_ass3['_merge'] == 'left_only']


# In[186]:


# merged_vle_ass4 = assessments.merge(vle, how='left', on=['code_module', 'code_presentation'],indicator=True).head()


# In[187]:


# merged_vle_ass4


# In[ ]:


# merged_vle_ass4.loc[merged_vle_ass4['_merge'] == 'right_only']


# In[ ]:


# merged_vle_ass4.loc[merged_vle_ass4['_merge'] == 'left_only']


# In[ ]:


# merged_vle_si


# In[535]:


# merged_vle_si.loc[merged_vle_si['_merge'] == 'left_only']


# In[538]:


merged_vle_si = merged_vle_si.dropna(subset=['final_result'])


# In[539]:


vle = merged_vle_si


# In[540]:


vle


# ---
# 
# <h4>3. Explore the dataframe</h4>
# 
# ---
# 
# <h5>Basic Information</h5>

# In[297]:


print('Assessments Dataframe\n')
analyze_df(assessments)


# * The data types are acceptable.
# * There are 11 null values in date. The documentation for this dataset states that if the final exam date is missing it is at the end of the last presentation week.

# We will again look at the possible values for our categorical variables:

# ---
# 
# <h5>Code Module</h5>
# 

# ---
# 
# <h5>Code Presentation</h5>
# 

# ---
# 
# <h5>Assessment ID</h5>
# 

# ---
# 
# <h5>Assessment Type</h5>
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

# In[65]:


vle.head()


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
# <h5>Basic Information</h5>

# In[309]:


analyze_df(vle)


# In[314]:


print(vle['activity_type'].explode().unique())


# ---
# 
# <h5>Code Module</h5>

# In[ ]:





# ---
# 
# <h5>Code Presentation</h5>

# In[ ]:





# ---
# 
# <h5>Student ID</h5>

# In[ ]:





# ---
# 
# <h5>Site ID</h5>

# In[ ]:





# ---
# 
# <h5>Date</h5>

# In[ ]:





# ---
# 
# <h5>Sum Click</h5>

# In[ ]:





# ---
# 
# <h5>Site ID</h5>

# ---
# 
# <h5>Code Module</h5>

# ---
# 
# <h5>Code Presentation</h5>

# ---
# 
# <h5>Activity Type</h5>

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
# <h5>Basic Information</h5>

# In[117]:


analyze_df(student_assessment)


# ---
# 
# <h5>Assessment ID</h5>

# ---
# 
# <h5>Student ID</h5>

# ---
# 
# <h5>Date Submitted</h5>

# ---
# 
# <h5>Score</h5>

# In[ ]:


for index, row in student_assessment[student_assessment['score'].isna()].iterrows():
    assessments.at[index, 'date'] = courses.loc[(courses['code_module'] == row['code_module']) & (courses['code_presentation'] == row['code_presentation']), 'module_presentation_length']


# In[319]:


assessment_score_nas = pd.DataFrame()
for i, row in student_assessment[student_assessment['score'].isna()].iterrows():
    print(student_info.loc[(student_info['id_student'] == row['id_student']), 'final_result'])


# <a id='MachineLearning'></a>
# 
# <h1>Machine Learning</h1>

# In[ ]:


change_col_val(col_dict, student_info)


# In[77]:


from sklearn.linear_model import LinearRegression

# create linear regression object
mlr = LinearRegression()

# fit linear regression
mlr.fit(student_info[['gender', 'imd_band']], student_info['final_result'])

# get the slope and intercept of the line best fit.
print(mlr.intercept_)
# -244.92350252069903

print(mlr.coef_)
# [ 5.97694123 19.37771052]


# In[ ]:





# In[ ]:





# In[ ]:




