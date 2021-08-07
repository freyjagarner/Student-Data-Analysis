#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_cell_magic('capture', '', 'from functions import *\n\n@register_cell_magic\ndef markdown(line, cell):\n    return md(cell.format(**globals()))')


# # Assessments
# 
# The assessments dataframe contains information about the unique assessments in each code module and presentation.

# assessments.head()

# ---
# 
# ## Assessments Contents
# 
# * **code_module**: The code module represents the code name of the course the assessment was held for.
# * **code_presentation**: The presentation represents the presentation which the test was held for.
# * **id_assessment**: The assessment ID is the unique identifier for each assessment.
# * **assessment_type**: The assessment type represents the kind of assessment it was.
#     - There are three assessment types:
#         * TMA: Tutor Marked Assessment
#         * CMA: Computer Marked Assessment
#         * Exam: The Final Exam
# * **date**: The date is how many days from the start of the course the assessment took place
# * **weight**: The weight is the weighted value of the assessment. Exams should have a weight of 100 which the rest of the assessments should add to 100 in total.

# **Size**

# In[2]:


md(f'''* Number of Rows: {len(assessments)}
* Number of Columns: {len(assessments.columns)}''')


# **Data Types**

# In[3]:


assessments.dtypes


# * id_student and id_assessments are both categorical values and so should be converted to objects

# In[4]:


# converting the data types
assessments = assessments.astype({'id_assessment': int})
assessments = assessments.astype({'id_assessment': object})


# **Null Values**

# In[5]:


# prints the sum of a columns null value
assessments.isnull().sum()


# * We have 2,873 null data points for assessment date. The documentation of this dataset states that if the exam date is missing then it is as the end of the last presentation week. We can find this information in the courses dataframe.

# In[6]:


# adding the dates for the null test dates
for index, row in assessments[assessments['date'].isna()].iterrows():
    assessments.at[index, 'date'] = courses.loc[(courses['code_module'] == row['code_module']) & (courses['code_presentation'] == row['code_presentation']), 'module_presentation_length']

# reprinting to ensure it worked
assessments.isnull().sum()


# * There are 173 null values for score. These records are, unfortunately not of much interest to us, since score is what we are trying to find the relationship for, and so we will discard them. This leaves us with no null data in assessments.

# **Unique Counts**

# In[7]:


assessments.nunique()


# **Unique Categorical Values**

# In[8]:


unique_vals(assessments)


# **Duplicate Values:**

# In[9]:


duplicate_vals(assessments)


# **Statistics**

# In[34]:


assessments.describe()

