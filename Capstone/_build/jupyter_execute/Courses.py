#!/usr/bin/env python
# coding: utf-8

# In[1]:


from functions import *

@register_cell_magic
def markdown(line, cell):
    return md(cell.format(**globals()))


# # Courses
# 
# ---

# ## General

# The courses dataframe has information for all modules and their presentations.

# In[10]:


courses.head()


# ---
# 
# ### Contents
# 
# * **code_module**: The code module represents the code name of the course. Modules are identified with three capital letters which run sequentially between AAA and GGG
# * **code_presentation**: The presentations are codified by their year and offering semester. B is for February and J is for October. 2013B for example is February of 2013. 
# * **mode_presentation_length**: The module presentation length is the length of the course in days.

# ---
# 
# ### Courses Information

# In[11]:


courses_types = analyze_df(courses, types=True)
courses_nulls = analyze_df(courses, nulls=True)
courses_nunique = analyze_df(courses, uniques=True)
courses_dupes = analyze_df(courses, dupes=True)
courses_nums = analyze_df(courses, nums=True)


# In[12]:


md(f'''
**Size**
    
* Number of Rows: {analyze_df(courses, rowlen=True)}
* Number of Columns: {analyze_df(courses, collen=True)}

**Data Types**
''')


# In[13]:


courses.dtypes


# **Null Values:**

# In[14]:


courses_nulls


# **Unique Counts:**

# In[15]:


courses.nunique()


# **Unique Categorical Values**:

# In[16]:


unique_vals(courses)


# **Duplicate Values**

# In[17]:


analyze_df(courses, dupes=True)


# **Statistics:**

# In[18]:


courses.describe().round(1)


# ---
# 
# ### Modules and Presentations

# In[19]:


mod_count = courses['code_module'].nunique()
presentation_count = courses['code_presentation'].nunique()
min_mod_count = courses['module_presentation_length'].min()
max_mod_count = courses['module_presentation_length'].max()
avg_mod_count = round(courses['module_presentation_length'].mean(), 1)

md(f'''* There are {mod_count} unique modules delivered over {presentation_count} presentations as detailed below:''')


# In[20]:


# making a crosstab to map each code module to its presentation
pd.crosstab(index=courses['code_module'], columns=courses['code_presentation'])


# In[21]:


get_ipython().run_cell_magic('markdown', '', '\n---\n\n### Module Presentation Length\n\n* Modules range from {min_mod_count} to {max_mod_count} days in length.\n* The average module is {avg_mod_count} days.')


# In[ ]:




