#!/usr/bin/env python
# coding: utf-8

# In[1]:


from functions import *

@register_cell_magic
def markdown(line, cell):
    return md(cell.format(**globals()))


# <a id='Courses'></a>
# 
# ---
# 
# <h2>Courses Dataframe</h2>
# 
# ---

# The courses datframe has information for all modules and their presentations.

# In[2]:


courses.head()


# ---
# 
# <h4>Contents</h4>
# 
# * <b>code_module</b>: The code module represents the code name of the course. Modules are identified with three capital letters which run sequentially between AAA and GGG
# * <b>code_presentation</b>: The presentations are codified by their year and offering semester. B is for February and J is for October. 2013B for example is February of 2013. 
# * <b>mode_presentation_length</b>: The module presentation length is the length of the course in days.

# ---
# 
# <h4>Courses Information</h4>

# In[3]:


courses_rowlen = analyze_df(courses, rowlen=True)
courses_collen = analyze_df(courses, collen=True)
courses_types = analyze_df(courses, types=True)
courses_nulls = analyze_df(courses, nulls=True)
courses_nunique = analyze_df(courses, uniques=True)
courses_dupes = analyze_df(courses, dupes=True)
courses_nums = analyze_df(courses, nums=True)


# In[4]:


md(f'''

<b>Size</b>
    
* Number of Rows: {courses_rowlen}
* Number of Columns: {courses_collen}

<b>Null Values:</b>
    
* {courses_nulls}

<b>Unique Column Counts:</b>
''')


# In[5]:


courses.nunique()


# <b>Unique Categorical Values</b>:

# In[6]:


print(f'''
       Code Modules: {courses['code_module'].explode().unique()}
       Code Presentations: {courses['code_presentation'].explode().unique()}
      ''')


# ---
# 
# <h4>Modules and Presentations</h4>

# In[7]:


mod_count = courses['code_module'].nunique()
presentation_count = courses['code_presentation'].nunique()
min_mod_count = courses['module_presentation_length'].min()
max_mod_count = courses['module_presentation_length'].max()
avg_mod_count = round(courses['module_presentation_length'].mean(), 1)

md(f'''* There are {mod_count} unique modules delivered over {presentation_count} presentations as detailed below:''')


# In[8]:


# making a crosstab to map each code module to its presentation
pd.crosstab(index=courses['code_module'], columns=courses['code_presentation'])


# In[9]:


get_ipython().run_cell_magic('markdown', '', '\n---\n\n<h4>Module Presentation Length</h4>\n\n* Modules range from {min_mod_count} to {max_mod_count} days in length.\n* The average module is {avg_mod_count} days.')

