#!/usr/bin/env python
# coding: utf-8

# In[1]:


from functions import *


# # Courses
# 
# ---

# ## General

# The courses dataframe has information for all modules and their presentations.

# In[2]:


# show head of courses dataframe
courses.head()


# ---
# 
# ## Courses Contents
# 
# * **code_module**: The code module represents the code name of the course. Modules are identified with three capital letters which run sequentially between AAA and GGG
# * **code_presentation**: The presentations are codified by their year and offering semester. B is for February and J is for October. 2013B for example is February of 2013. 
# * **mode_presentation_length**: The module presentation length is the length of the course in days.

# ---
# 
# ## Courses Information

# **Size**

# In[3]:


# get row & column count for courses dataframe
get_size(courses)


# **Data Types**

# In[4]:


# show data types for courses dataframe
get_dtypes(courses)


# **Null Values:**

# In[5]:


# show null values for columns in courses
null_vals(courses)


# **Duplicate Values**

# In[6]:


# show duplicate values in courses if any
get_dupes(courses)


# **Unique Counts:**

# In[7]:


# get counts for the unque values in courses columns
count_unique(courses)


# **Unique Categorical Values**:

# In[8]:


# get the unique categorical values in courses
unique_vals(courses)


# **Statistics:**

# In[9]:


# show statistical breakdown of numerical values in courses
courses.describe().round(1)


# ---
# 
# ## Modules and Presentations

# In[10]:


# store the number of unique modules
mod_count = courses['code_module'].nunique()
# store the number of unique presentations
presentation_count = courses['code_presentation'].nunique()
# store the minimum module length in days
min_mod_count = courses['module_presentation_length'].min()
# store the maximum module length in dats
max_mod_count = courses['module_presentation_length'].max()
# store the average module length in days
avg_mod_count = round(courses['module_presentation_length'].mean(), 1)

md(f'''There are {mod_count} unique modules delivered over {presentation_count} presentations as detailed below:''')


# In[11]:


# making a crosstab to map each code module to its presentation
pd.crosstab(index=courses['code_module'], columns=courses['code_presentation'])


# In[12]:


md(f"""
## Module Presentation Length

* Modules range from {min_mod_count} to {max_mod_count} days in length.
* The average module is {avg_mod_count} days.
""")


# In[ ]:




