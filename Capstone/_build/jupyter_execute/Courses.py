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


get_size(courses)


# **Data Types**

# In[4]:


get_dtypes(courses)


# **Null Values:**

# In[5]:


null_vals(courses)


# **Unique Counts:**

# In[6]:


dataframe(courses.nunique(), columns=['Count']).reset_index()


# **Unique Categorical Values**:

# In[7]:


unique_vals(courses)


# **Duplicate Values**

# In[8]:


get_dupes(courses)


# **Statistics:**

# In[9]:


courses.describe().round(1)


# ---
# 
# ## Modules and Presentations

# In[10]:


mod_count = courses['code_module'].nunique()
presentation_count = courses['code_presentation'].nunique()
min_mod_count = courses['module_presentation_length'].min()
max_mod_count = courses['module_presentation_length'].max()
avg_mod_count = round(courses['module_presentation_length'].mean(), 1)

md(f'''* There are {mod_count} unique modules delivered over {presentation_count} presentations as detailed below:''')


# In[11]:


# making a crosstab to map each code module to its presentation
pd.crosstab(index=courses['code_module'], columns=courses['code_presentation'])


# In[12]:


md("""
## Module Presentation Length

* Modules range from {min_mod_count} to {max_mod_count} days in length.
* The average module is {avg_mod_count} days.
""")


# In[ ]:





# In[ ]:




