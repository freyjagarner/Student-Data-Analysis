#!/usr/bin/env python
# coding: utf-8

# In[1]:


from functions import *

@register_cell_magic
def markdown(line, cell):
    return md(cell.format(**globals()))


# <a id='StudentInfo'></a>
# 
# <h2>Student Info and Student Registration Dataframes</h2>
# 
# ---

# <h4>Student Info</h4>
# 
# The student info dataframe contains information about students including the module and presentation they took, demographic information and the final result of their studies.

# In[2]:


# looking at the student_info dataframe
student_info.head()


# <h4>Contents</h4>
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

# ---
# 
# <h3>Student Registration</h3>
# 
# The student registration dataframe contains information about the dates that students registered and,if applicable, unregistered from the module.
# 
# <h4>Contents</h4>
# 
# * <b>date_registration</b> is the date that the student registered for the module relative to the start of the module. A negative value indicates that many days before the module began.
# * <b>date_unregistration</b> is the date that the student unregistered from the course module in relation to the start date of the course. 
# 

# In[3]:


# looking at the student_registration dataframe
student_registration.head()


# ```{note}
# The student registration dataframe matches 1:1 with the student_info dataframe only adding the date the student registered and the date, if applicable, they unregistered, and so we will merge these two dataframes
# ```

# In[4]:


# left join and merge student info with student registration
stud_info = student_info.merge(student_registration, how='left', on=['code_module', 'code_presentation', 'id_student'])


# In[ ]:




