#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('capture', '', 'from ipynb.fs.full.Student_Info_and_Registration import student_info_reg\nfrom functions import *\n\n@register_cell_magic\ndef markdown(line, cell):\n    return md(cell.format(**globals()))\n\nimport timeit\nfrom collections import OrderedDict')


# ---
# 
# # Assessments and Student Assessments

# ---
# 
# ## Assessments and Student Assessments Merged Dataframe:

# In[2]:


# merges dataframes student_assessment with assessments with a full outer join on their common ID id_assessment
# creates a column _merge which tells you if the id_assessment was found in one or both dataframes
merged_assessments = student_assessment.merge(assessments, how='outer', on=['id_assessment'] ,indicator=True)
merged_assessments.head()


# * Our new merge column tells us if the data maps perfectly, or if it is only found on the right or left side, the right side being the assessments dataframe and the left side being the student_assessments dataframe

# **Rows that do not map:**

# In[3]:


missing_exams = merged_assessments.loc[merged_assessments['_merge'] != 'both'].reset_index(drop=True)


# In[4]:


missing_exams


# In[5]:


missing_exams_list =list(missing_exams['id_assessment'])


# These rows all have entries in the assessments dataframe but have no match in the student_assessment dataframe. This indicates that no students in our data took these exams, and so we will drop them, and then the merge column since it will have no more useful information.

# In[6]:


# remove tests that students did not take
# reset the index to be consecutive again
merged_assessments = merged_assessments.dropna(subset=['id_student']).reset_index(drop=True)

# drop the merge column since it is no longer of use
merged_assessments = merged_assessments.drop(columns=['_merge']).reset_index(drop=True)


# In[7]:


merged_assessments = merged_assessments[['code_module', 'code_presentation', 'id_student', 'id_assessment', 'assessment_type', 'date_submitted', 'date', 'weight', 'score']]


# **Removing Eliminated Students**

# **Merged Assessment/Student_info dataframes**

# In order to remove the students that we removed for the number of previous attempts, we must merge assessments and student info and find the difference

# In[8]:


# merged 'student info/assessments' with a full outer join on their common columns
merged_si_assm = merged_assessments.merge(student_info_reg, how='outer', on=['id_student', 'code_module', 'code_presentation'], indicator=True)
merged_si_assm.head()


# For this merge column the right side would be the student info dataframe and the left side would be assessments. If an entry receives the label of right_only there is a student who has no assessments, if the label is left_only, there is an assessment that doesn't match up with a student.

# In[9]:


# variable for where merge is left_only, and only found on the 
only_assessments = merged_si_assm.loc[merged_si_assm['_merge']=='left_only']
only_student_info = merged_si_assm.loc[merged_si_assm['_merge']=='right_only']


# **Assessments that do not map to students**:

# In[10]:


only_assessments.head()


# **Students without any test scores**:

# In[11]:


only_student_info.head()


# In[12]:


md(f'''
    We have {len(only_assessments)} values in only assessments, which map to students who had made previous attempts which we eliminated, and {len(only_student_info)} values in only student_info, which means we have students for whom we have no test scores.
    We can drop both of these which are missing values for the purpose of this dataframe since we are just analyzing test scores
    ''')


# In[13]:


# merging assessments with the original student data dataframe to make sure that the missing students are the ones we removed.
merged_test = merged_assessments.merge(student_info, how='outer', on=['id_student', 'code_module', 'code_presentation'], indicator=True)

# removing entries where num_prev_attempts == 0
merged_test = merged_test[merged_test['num_of_prev_attempts'] == 0]

# checking if any in only the student info dataframe remain (left_only). No output means all of the tests without students map to a student where num_prev_attempts == 0
merged_test.loc[merged_test['_merge']=='left_only']


# In[14]:


# removing any student with NaN values in id_assessment or final_result
merged_si_assm = merged_si_assm.dropna(subset=['id_assessment', 'final_result'])


# In[15]:


# reordering dataframe columns to group like data
merged_si_assm = merged_si_assm[['code_module', 'code_presentation', 'id_student', 'region', 'imd_band', 'age_band', 'gender', 'highest_education', 'disability', 'final_result', 'id_assessment', 'assessment_type', 'date_submitted', 'date', 'weight', 'score']]


# In[16]:


# converting the data types back
merged_si_assm = merged_si_assm.astype({'id_assessment': int, 'id_student': int})
merged_si_assm = merged_si_assm.astype({'id_assessment': object, 'id_student': object})


# In[17]:


# reset the index
merged_si_assm.reset_index(drop=True).head()


# In[18]:


cleaned_assessments = merged_si_assm


# In[ ]:





# ---
# 
# ## Testing Area

# In[19]:


pd.DataFrame(student_info.loc[student_info['id_student'] == 65002, ['final_result']])


# In[20]:


pd.DataFrame(merged_assessments.loc[merged_assessments['id_student'] == 65002, ['id_assessment','score']])


# In[21]:


new_df = pd.DataFrame(columns=merged_assessments.columns)


# In[22]:


for i, r in assessments['module_presentation'].iteritems():
    print(r)


# In[ ]:


cleaned_assessments.iloc[0]


# In[ ]:


cleaned_assessments.head()


# In[ ]:


assessments.head()


# In[ ]:


pd.DataFrame(cleaned_assessments.loc[0:3])


# In[42]:


cleaned_assessments['code_module'].values[0]


# In[47]:


missing_exams_list = list(missing_exams['id_assessment'])
count = 0
my_list = []
value_list =[]
cleaned_assessments['module_presentation'] = cleaned_assessments['code_module'] + cleaned_assessments['code_presentation']
assessments['module_presentation'] = assessments['code_module'] + assessments['code_presentation']


for i in cleaned_assessments['module_presentation'].values:
    for j in assessments['module_presentation'].values:
        if row == r:
            tests_student_has = list(cleaned_assessments.loc[cleaned_assessments['id_student'] == cleaned_assessments['id_student'][index], 'id_assessment'])
            bad_lists = tests_student_has+missing_exams_list
            if assessments['id_assessment'].values[i] not in bad_lists:
                value_list = [cleaned_assessments['code_module'].values[index], cleaned_assessments['code_presentation'].values[index], cleaned_assessments['id_student'].values[index], assessments['id_assessment'].values[i], cleaned_assessments['score'].values[index], cleaned_assessments['date_submitted'].values[index], assessments['assessment_type'].values[i], assessments['date'].values[i], assessments['weight'].values[i]]
                my_list.append(value_list)
                print(f"{len(my_list)}/infinite rows appended", end="\r")


# In[33]:


missing_exams_list = list(missing_exams['id_assessment'])
count = 0
my_list = []
value_list =[]
cleaned_assessments['module_presentation'] = cleaned_assessments['code_module'] + cleaned_assessments['code_presentation']
assessments['module_presentation'] = assessments['code_module'] + assessments['code_presentation']


for index, row in cleaned_assessments['module_presentation'].iteritems():
    for i, r in assessments['module_presentation'].iteritems():
        if row == r:
            tests_student_has = list(cleaned_assessments.loc[cleaned_assessments['id_student'] == cleaned_assessments['id_student'][index], 'id_assessment'])
            bad_lists = tests_student_has+missing_exams_list
            if assessments['id_assessment'][i] not in bad_lists:
                value_list = [cleaned_assessments['code_module'][index], cleaned_assessments['code_presentation'][index], cleaned_assessments['id_student'][index], assessments['id_assessment'][i], cleaned_assessments['score'][index], cleaned_assessments['date_submitted'][index], assessments['assessment_type'][i], assessments['date'][i], assessments['weight'][i]]
                my_list.append(value_list)
    print(f"{len(my_list)}/infinite rows appended", end="\r")
    


# In[32]:


pd.DataFrame(my_list)


# In[168]:


missing_exams_list = list(missing_exams['id_assessment'])
couant = 0
my_list = []

cleaned_assessments['module_presentation'] = cleaned_assessments['code_module'] + cleaned_assessments['code_presentation']
assessments['module_presentation'] = assessments['code_module'] + assessments['code_presentation']

print(start)

for index, row in cleaned_assessments['module_presentation'].iteritems():
    for i, r in assessments['module_presentation'].iteritems():
        if row == r:
            tests_student_has = list(cleaned_assessments.loc[cleaned_assessments['id_student'] == cleaned_assessments['id_student'][index], 'id_assessment'])
            bad_lists = tests_student_has+missing_exams_list
            if assessments['id_assessment'][i] not in bad_lists:
                value_dict = {'code_module':cleaned_assessments['code_module'][index], 'code_presentation':cleaned_assessments['code_presentation'][index], 'id_student':cleaned_assessments['id_student'][index], 'id_assessment':assessments['id_assessment'][i], 'score':cleaned_assessments['score'][index], 'date_submitted':cleaned_assessments['date_submitted'][index],'assessment_type':assessments['assessment_type'][i], 'date':assessments['date'][i], 'weight':assessments['weight'][i]}
    my_list.append(value_dict)
    print(f"{len(my_list)}/infinite rows appended", end="\r")
print(time.process_time() - start)


# In[79]:


#good

cleaned_assessments['module_presentation'] = cleaned_assessments['code_module'] + cleaned_assessments['code_presentation']
assessments['module_presentation'] = assessments['code_module'] + assessments['code_presentation']
start = time.process_time()
missing_exams_list = list(missing_exams['id_assessment'])
count = 0

for index, row in cleaned_assessments.iterrows():
    for i, r in assessments.iterrows():
        if assessments['module_presentation'][i] == cleaned_assessments['module_presentation'][index]:
            tests_student_has = list(cleaned_assessments.loc[cleaned_assessments['id_student'] == cleaned_assessments['id_student'][index], 'id_assessment'])
            bad_lists = tests_student_has+missing_exams_list
            if assessments['id_assessment'][i] not in bad_lists:
                value_series = pd.Series([cleaned_assessments['code_module'][index], cleaned_assessments['code_presentation'][index], cleaned_assessments['id_student'][index], assessments['id_assessment'][i], cleaned_assessments['score'][index], cleaned_assessments['date_submitted'][index], assessments['assessment_type'][i], assessments['date'][i], assessments['weight'][i]])
                new_df = new_df.append(value_series, ignore_index=True)
                print(f"{len(new_df)}/ rows appended", end="\r")
                continue


# In[88]:


pd.DataFrame(my_list)[0:50]


# 

# In[ ]:





# In[10]:


start = time.process_time()
missing_exams_list = list(missing_exams['id_assessment'])
count = 0
my_list = []
d = {}
print(start)
for index, row in merged_assessments.iterrows():
    for i, r in assessments.iterrows():
        if assessments['code_module'][i] == merged_assessments['code_module'][index] and assessments['code_presentation'][i] == merged_assessments['code_presentation'][index]:
            value_dict = {'code_module':merged_assessments['code_module'][index], 'code_presentation':merged_assessments['code_presentation'][index], 'id_student':merged_assessments['id_student'][index], 'id_assessment':assessments['id_assessment'][i], 'score':merged_assessments['score'][index], 'date_submitted':merged_assessments['date_submitted'][index],'assessment_type':assessments['assessment_type'][i], 'date':assessments['date'][i], 'weight':assessments['weight'][i]}
            tests_student_has = list(merged_assessments.loc[merged_assessments['id_student'] == merged_assessments['id_student'][index], 'id_assessment'])
            if assessments['id_assessment'][i] not in (tests_student_has):
                    if assessments['id_assessment'][i] not in (missing_exams_list):
                            d[count] = value_dict
                            count+=1
                            print(f"{len(d)}/ rows appended", end="\r")
                            continue
print(time.process_time() - start)


# In[141]:


missing_exams_list


# In[ ]:


start = time.process_time()
missing_exams_list = list(missing_exams['id_assessment'])
count = 0
my_list = []
d = {}
print(start)
for index, row in merged_assessments.iterrows():
    for i, r in assessments.iterrows():
        if assessments['code_module'][i] == merged_assessments['code_module'][index] and assessments['code_presentation'][i] == merged_assessments['code_presentation'][index]:
            value_dict = {'code_module':merged_assessments['code_module'][index], 'code_presentation':merged_assessments['code_presentation'][index], 'id_student':merged_assessments['id_student'][index], 'id_assessment':assessments['id_assessment'][i], 'score':merged_assessments['score'][index], 'date_submitted':merged_assessments['date_submitted'][index],'assessment_type':assessments['assessment_type'][i], 'date':assessments['date'][i], 'weight':assessments['weight'][i]}
            tests_student_has = list(merged_assessments.loc[merged_assessments['id_student'] == merged_assessments['id_student'][index], 'id_assessment'])
            if assessments['id_assessment'][i] not in (tests_student_has):
                    if assessments['id_assessment'][i] not in (missing_exams_list):
                            d[count] = value_dict
                            count+=1
                            print(f"{len(d)}/ rows appended", end="\r")
                            continue
print(time.process_time() - start)


# In[ ]:


d = {}
count = 0

start = time.process_time()
missing_exams_list = list(missing_exams['id_assessment'])
my_list = []
d = {}
print(start)
for index, row in merged_assessments.iterrows():
    for i, r in assessments.iterrows():
        if assessments['code_module'][i] == merged_assessments['code_module'][index] and assessments['code_presentation'][i] == merged_assessments['code_presentation'][index]:
            value_dict = {'code_module':merged_assessments['code_module'][index], 'code_presentation':merged_assessments['code_presentation'][index], 'id_student':merged_assessments['id_student'][index], 'id_assessment':assessments['id_assessment'][i], 'score':merged_assessments['score'][index], 'date_submitted':merged_assessments['date_submitted'][index],'assessment_type':assessments['assessment_type'][i], 'date':assessments['date'][i], 'weight':assessments['weight'][i]}
            tests_student_has = list(merged_assessments.loc[merged_assessments['id_student'] == merged_assessments['id_student'][index], 'id_assessment'])
            if assessments['id_assessment'][i] not in (tests_student_has):
                    if assessments['id_assessment'][i] not in (missing_exams_list):
                            d[count] = value_dict
                            count+=1
                            print(f"{len(d)}/ rows appended", end="\r")
                            continue
print(time.process_time() - start)



# In[ ]:


# the dictionary to pass to pandas dataframe
d = {}

# a counter to use to add entries to "dict"
i = 0 

# Example data to loop and append to a dataframe
data = [{"foo": "foo_val_1", "bar": "bar_val_1"}, 
       {"foo": "foo_val_2", "bar": "bar_val_2"}]

# the loop
for entry in data:

    # add a dictionary entry to the final dictionary
    d[i] = {"col_1_title": entry['foo'], "col_2_title": entry['bar']}
    
    # increment the counter
    i = i + 1

# create the dataframe using 'from_dict'
# important to set the 'orient' parameter to "index" to make the keys as rows
df = DataFrame.from_dict(d, "index")


# In[86]:


missing_exams_list = list(missing_exams['id_assessment'])
count = 0
while count < 1:
    for index, row in merged_assessments.iterrows():
        for i, r in assessments.iterrows():
            if assessments['code_module'][i] == merged_assessments['code_module'][index]:
                 if assessments['code_presentation'][i] == merged_assessments['code_presentation'][index]:
                        value_dict = {'code_module':merged_assessments['code_module'][index], 'code_presentation':merged_assessments['code_presentation'][index], 'id_student':merged_assessments['id_student'][index], 'id_assessment':assessments['id_assessment'][i], 'score':merged_assessments['score'][index], 'date_submitted':merged_assessments['date_submitted'][index],'assessment_type':assessments['assessment_type'][i], 'date':assessments['date'][i], 'weight':assessments['weight'][i]}
                        tests_student_has = list(merged_assessments.loc[merged_assessments['id_student'] == merged_assessments['id_student'][index], 'id_assessment'])
                        if assessments['id_assessment'][i] not in (tests_student_has):
                            if assessments['id_assessment'][i] not in (missing_exams_list):
                                print(assessments['id_assessment'][i], merged_assessments['id_student'][index])
                                continue


# In[53]:


count = 0
while count < 1:
    for index, row in merged_assessments.iterrows():
        for i, r in assessments.iterrows():
            if assessments['code_module'][i] == merged_assessments['code_module'][index]:
                 if assessments['code_presentation'][i] == merged_assessments['code_presentation'][index]:
                        value_dict = {'code_module':merged_assessments['code_module'][index], 'code_presentation':merged_assessments['code_presentation'][index], 'id_student':merged_assessments['id_student'][index], 'id_assessment':assessments['id_assessment'][i], 'score':merged_assessments['score'][index], 'date_submitted':merged_assessments['date_submitted'][index],'assessment_type':assessments['assessment_type'][i], 'date':assessments['date'][i], 'weight':assessments['weight'][i]}
                        if assessments['id_assessment'][i] not in list(merged_assessments.loc[merged_assessments['id_student'] == merged_assessments['id_student'][index], 'id_assessment']):
                            new_df = new_df.append(value_dict, ignore_index=True)
                            print(f"{len(new_df)}/ rows appended", end="\r")
                            count += 1
                            continue


# In[32]:


for index, row in student_info.iterrows():
     for i, r in assessments.iterrows():
            if assessments['code_module'][i] == student_info['code_module'][index]:
                 if assessments['code_presentation'][i] == student_info['code_presentation'][index]:
                        if int(assessments['id_assessment'][i]) not in list(merged_assessments.loc[merged_assessments['id_student'] == merged_assessments['id_student'][index], 'id_assessment']):
                            values = [student_info['code_module'][index], student_info['code_presentation'][index], student_info['id_student'][index], assessments['id_assessment'][i], assessments['assessment_type'][i], assessments['weight'][i]]
                            for m in list(merged_assessments.columns):
                                for n in values:
                                    new_df[]


# In[55]:


'''count = 0
while count < 1:
    for index, row in student_info.iterrows():
        for i, r in assessments.iterrows():
            if assessments['code_module'][i] == student_info['code_module'][index]:
                 if assessments['code_presentation'][i] == student_info['code_presentation'][index]:
                        if assessments['id_assessment'][i] not in list(merged_assessments.loc[merged_assessments['id_student'] == merged_assessments['id_student'][index], 'id_assessment']):
                            new_df = new_df.append([[student_info['code_module'][index], student_info['code_presentation'][index], student_info['id_student'][index], assessments['id_assessment'][i], assessments['assessment_type'][i], assessments['weight'][i]]], ignore_index=True)
                            print(f"{len(new_df)}/ rows appended", end="\r")
                            count += 1
                            continue'''


# In[15]:


pd.DataFrame(merged_assessments.loc[merged_assessments['id_student'] == 11391, 'id_assessment'])


# **Updated Dataframe**

# **Size**

# In[ ]:


md(f'''* Number of Rows: {len(merged_assessments)}
* Number of Columns: {len(merged_assessments.columns)}''')


# **Data Types**

# In[ ]:


merged_assessments.dtypes


# * id_student and id_assessments are both categorical values and so should be converted to objects

# In[ ]:


# converting the data types
merged_assessments = merged_assessments.astype({'id_assessment': int, 'id_student': int})
merged_assessments = merged_assessments.astype({'id_assessment': object, 'id_student': object})


# **Null Values**

# In[ ]:


# prints the sum of a columns null value
merged_assessments.isnull().sum()


# * We have 2,873 null data points for assessment date. The documentation of this dataset states that if the exam date is missing then it is as the end of the last presentation week. We can find this information in the courses dataframe.

# In[ ]:


# adding the dates for the null test dates
for index, row in merged_assessments[merged_assessments['date'].isna()].iterrows():
    merged_assessments.at[index, 'date'] = courses.loc[(courses['code_module'] == row['code_module']) & (courses['code_presentation'] == row['code_presentation']), 'module_presentation_length']

# reprinting to ensure it worked
merged_assessments.isnull().sum()


# * There are 173 null values for score. These records are, unfortunately not of much interest to us, since score is what we are trying to find the relationship for, and so we will discard them. This leaves us with no null data in assessments.

# In[ ]:


# removes any entry where the score is NaN
merged_assessments = merged_assessments.dropna(subset=['score'])

# reprinting to ensure it worked
merged_assessments.isnull().sum()


# **Unique Counts**

# In[ ]:


cleaned_assessments.nunique()


# **Unique Categorical Values**

# In[ ]:


unique_vals(cleaned_assessments)


# **Duplicate Values:**

# In[ ]:


duplicate_vals(cleaned_assessments)


# **Statistics**

# In[ ]:


cleaned_assessments.describe()


# In[ ]:


cleaned_assessments


# In[ ]:


assessments


# In[ ]:


cleaned_assessments.loc[cleaned_assessments['id_student'] == 11391, 'id_assessment']


# if a test id is in assessments in the same code module and presentation as a student is in:
#     if the test is already in the dataframe under that student id:
#         do nothing
#     else:
#         add the test with all the same student information, the assessment id, type, and weight to the dataframe

# In[ ]:


count = 0

# iterate through cleaned_assessments dataframe
for i, r in assessments.iterrows():
    for index, row in cleaned_assessments.iterrows():
    # iterate through assessments dataframe
    
        # if the code module in cleaned_assessments is the same as the code_module in assessments
        # convert to strings to compare
        if str(cleaned_assessments['code_module'][index]) == str(assessments['code_module'][i]):
            # if the code presentations are also the same
            if str(cleaned_assessments['code_presentation'][index]) == str(assessments['code_presentation'][i]):
                # if the assessment id is not found under that student append another row with that students information and the test they are missing
                if assessments['id_assessment'][i] not in cleaned_assessments.loc[cleaned_assessments['id_student'] == cleaned_assessments['id_student'][index], 'id_assessment']:
                    cleaned_assessments = cleaned_assessments.append([cleaned_assessments['code_module'][index], cleaned_assessments['code_presentation'][index], cleaned_assessments['id_student'][index], cleaned_assessments['region'][index], cleaned_assessments['imd_band'][index], cleaned_assessments['age_band'][index], cleaned_assessments['gender'][index], cleaned_assessments['highest_education'][index], cleaned_assessments['disability'][index], assessments['id_assessment'][i], assessments['assessment_type'][i], assessments['weight'][i]])
                    count += 1
                    print(f"{count} rows appended", end="\r")


# In[ ]:


aggregates = { 'assessment_type':'first','weight':'sum'}
assessments.groupby(['code_module','code_presentation']).aggregate(aggregates).reset_index()


# In[ ]:



for index, row in cleaned_assessments.iterrows():
    for i, r in assessments.iterrows():
        if cleaned_assessments['code_module'][index] == assessments['code_module'][i]:
            if cleaned_assessments['code_presentation'][index] == assessments['code_presentation'][i]:
                cleaned_assessments.append([cleaned_assessments['code_module'][index], cleaned_assessments['code_presentation'][index], cleaned_assessments['id_student'][index], cleaned_assessments['region'][index], cleaned_assessments['imd_band'][index], cleaned_assessments['age_band'][index], cleaned_assessments['gender'][index], cleaned_assessments['highest_education'][index], cleaned_assessments['disability'][index], assessments['id_assessment'][i], assessments['assessment_type'][i], assessments['weight'][i]])
                
                


# In[ ]:


for index, row in cleaned_assessments.loc[cleaned_assessments['final_result'] == 'Withdrawn'].iterrows():
    for i, r in assessments.iterrows():
        if cleaned_assessments['code_module'][index] == assessments['code_module'][i]:
            if cleaned_assessments['code_presentation'][index] == assessments['code_presentation'][i]:
                cleaned_assessments.append([cleaned_assessments['code_module'][index], cleaned_assessments['code_presentation'][index], cleaned_assessments['id_student'][index], cleaned_assessments['region'][index], cleaned_assessments['imd_band'][index], cleaned_assessments['age_band'][index], cleaned_assessments['gender'][index], cleaned_assessments['highest_education'][index], cleaned_assessments['disability'][index], assessments['id_assessment'][i], assessments['assessment_type'][i], assessments['weight'][i]])


# In[ ]:


pd.concat(x for _, x in cleaned_assessments.groupby("id_assessment") if len(x) > 1).head()


# In[ ]:


for i, r in assessments[student_info.loc['final_result'] == 'Withdrawn'].iterrows():
        cleaned_assessments.append(courses.loc[(courses['code_module'] == row['code_module']) & (courses['code_presentation'] == row['code_presentation']), 'module_presentation_length']


# In[ ]:


student_assessment


# In[ ]:


assessments


# In[ ]:


cleaned_assessments


# In[ ]:





# In[ ]:


for index, row in student_info.iterrows():
    for i, r in assessments.iterrows():
        if student_info['code_module'][index] == assessments['code_module'][i]:
            if student_info['code_presentation'][index] == assessments['code_presentation'][i]:
                new_df = new_df.append([student_info['code_module'][index], student_info['code_presentation'][index], student_info['id_student'][index], assessments['id_assessment'][i], assessments['assessment_type'][i], assessments['weight'][i]])
                print(f"{len(new_df)}/ rows appended", end="\r")

