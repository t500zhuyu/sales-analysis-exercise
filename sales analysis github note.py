#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries
import os
import pandas as pd


# In[2]:


file_path = r'C:\Users\luist\OneDrive\data analysis\sql practicas y proyectos\bases de datos internet\Data-Analysis-Sales-US-master github\all_data.csv'

# Replace backslashes with forward slashes
file_path = file_path.replace('\\', '/')

print(file_path)


# In[3]:


# importing the csv file, then showing the first rows of the table
all_data = pd.read_csv('C:/Users/luist/OneDrive/data analysis/sql practicas y proyectos/bases de datos internet/Data-Analysis-Sales-US-master github/all_data.csv')
all_data.head()


# In[4]:


# cleaning the data
# find Nan data in the rows
# all_data.isna() generates a Boolean DataFrame where True represents missing (NaN) values and False represents non-missing values.
#.any(axis=1) checks for rows where at least one column contains a missing value (NaN).

nan_df = all_data[all_data.isna().any(axis=1)]
# the next code show the first lines of the Nan rows
display(nan_df.head())

# drop the rows with Nan with dropna
all_data = all_data.dropna(how='all')
all_data.head()


# In[6]:


# So, the entire code all_data = all_data[all_data['Order Date'].str[0:2]!='Or'] 
# is used to remove rows from the DataFrame all_data where the 'Order Date' column 
# starts with 'Or'. This can be helpful for data cleaning when there are rows 
# with invalid or placeholder values that need to be excluded from the analysis.
all_data = all_data[all_data['Order Date'].str[0:2]!='Or']


# In[7]:


# this code make the data of the columns into numeric data type (int)
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])


# In[8]:


# the next code add column month, this is part of the order date column
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
#showing the table with the new column
all_data.head()


# In[9]:


# adding a column, city column
def get_city(address):
    return address.split(",")[1].strip(" ")

def get_state(address):
    return address.split(",")[2].split(" ")[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)}  ({get_state(x)})")
all_data.head()


# In[ ]:


Data Exploration
get_ipython().run_line_magic('pinfo', 'month')


# In[10]:


all_data['Sales'] = all_data['Quantity Ordered'].astype('int') * all_data['Price Each'].astype('float')


# In[11]:


# showing the sales by month
all_data.groupby(['Month']).sum()


# In[12]:


# in this next code we use matplotlib to create a chart
# sales per month
import matplotlib.pyplot as plt

months = range(1,13)
# print(months)

plt.bar(months,all_data.groupby(['Month']).sum()['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()


# In[ ]:


get_ipython().run_line_magic('pinfo', 'product')


# In[13]:


all_data.groupby(['City']).sum()


# In[14]:


keys = [city for city, df in all_data.groupby(['City'])]

plt.bar(keys,all_data.groupby(['City']).sum()['Sales'])
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.xticks(keys, rotation='vertical', size=8)
plt.show()


# Question 3: What time should we display advertisements to maximize likelihood of customer's buying product?

# In[15]:


# Add hour column
all_data['Hour'] = pd.to_datetime(all_data['Order Date']).dt.hour
all_data['Minute'] = pd.to_datetime(all_data['Order Date']).dt.minute
all_data['Count'] = 1
all_data.head()


# In[16]:


keys = [pair for pair, df in all_data.groupby(['Hour'])]

plt.plot(keys, all_data.groupby(['Hour']).count()['Count'])
plt.xticks(keys)
plt.grid()
plt.show()

# My recommendation is slightly before 11am or 7pm


# Question 4: What products are most often sold together?

# In[17]:


# https://stackoverflow.com/questions/43348194/pandas-select-rows-if-id-appear-several-time
df = all_data[all_data['Order ID'].duplicated(keep=False)]

# Referenced: https://stackoverflow.com/questions/27298178/concatenate-strings-from-several-rows-using-pandas-groupby
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df2 = df[['Order ID', 'Grouped']].drop_duplicates()


# In[18]:


# Referenced: https://stackoverflow.com/questions/52195887/counting-unique-pairs-of-numbers-into-a-python-dictionary
from itertools import combinations
from collections import Counter

count = Counter()

for row in df2['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key,value in count.most_common(10):
    print(key, value)

What product sold the most? Why do you think it sold the most?
# In[19]:


product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']

keys = [pair for pair, df in product_group]
plt.bar(keys, quantity_ordered)
plt.xticks(keys, rotation='vertical', size=8)
plt.show()


# In[20]:


# Referenced: https://stackoverflow.com/questions/14762181/adding-a-y-axis-label-to-secondary-y-axis-in-matplotlib

prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(keys, quantity_ordered, color='g')
ax2.plot(keys, prices, color='b') # this is the blue line which represents the prices

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(keys, rotation='vertical', size=8)

fig.show()


# In[ ]:





# In[ ]:





# In[ ]:




