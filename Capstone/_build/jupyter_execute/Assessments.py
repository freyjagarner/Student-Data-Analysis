#!/usr/bin/env python
# coding: utf-8

# In[1]:


from functions import *

@register_cell_magic
def markdown(line, cell):
    return md(cell.format(**globals()))

("")


# ---
# 
# <h2>Assessments Dataframe</h2>

# The assessments dataframe contains information about the unique assessments in each code module and presentation.

# In[17]:


assessments.head()


# ---
# 
# <h4>Assessments Contents</h4>
# 
# * <b>code_module</b>: The code module represents the code name of the course the assessment was held for.
# * <b>code_presentation</b>: The presentation represents the presentation which the test was held for.
# * <b>id_assessment</b>: The assessment ID is the unique identifier for each assessment.
# * <b>assessment_type</b>: The assessment type represents the kind of assessment it was.
#     - There are three assessment types:
#         * TMA: Tutor Marked Assessment
#         * CMA: Computer Marked Assessment
#         * Exam: The Final Exam
# * <b>date</b>: The date is how many days from the start of the course the assessment took place
# * <b>weight</b>: The weight is the weighted value of the assessment. Exams should have a weight of 100 which the rest of the assessments should add to 100 in total.

# <b>Size</b>

# In[18]:


md(f'''* Number of Rows: {len(assessments)}
* Number of Columns: {len(assessments.columns)}''')


# <b>Data Types</b>

# In[19]:


assessments.dtypes


# * id_student and id_assessments are both categorical values and so should be converted to objects

# In[23]:


# converting the data types
assessments = assessments.astype({'id_assessment': int})
assessments = assessments.astype({'id_assessment': object})


# <b>Null Values</b>

# In[24]:


# prints the sum of a columns null value
assessments.isnull().sum()


# * We have 2,873 null data points for assessment date. The documentation of this dataset states that if the exam date is missing then it is as the end of the last presentation week. We can find this information in the courses dataframe.

# In[25]:


# adding the dates for the null test dates
for index, row in assessments[assessments['date'].isna()].iterrows():
    assessments.at[index, 'date'] = courses.loc[(courses['code_module'] == row['code_module']) & (courses['code_presentation'] == row['code_presentation']), 'module_presentation_length']

# reprinting to ensure it worked
assessments.isnull().sum()


# * There are 173 null values for score. These records are, unfortunately not of much interest to us, since score is what we are trying to find the relationship for, and so we will discard them. This leaves us with no null data in assessments.

# <b>Unique Counts</b>

# In[27]:


assessments.nunique()


# <b>Unique Categorical Values</b>

# In[30]:


unique_vals(assessments)


# <b>Duplicate Values:</b>

# In[32]:


duplicate_vals(assessments)


# <b>Statistics</b>

# In[34]:


assessments.describe()

