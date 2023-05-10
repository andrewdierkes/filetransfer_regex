#!/usr/bin/env python
# coding: utf-8

# In[56]:


import os
import pathlib
import shutil
import re


# In[169]:


#create paths for source of data and desired location
_path = pathlib.Path.cwd()
destination = os.path.join(_path, input('input subdirectory name'))

#ALTERNATIVE below; iterate thru files in directory, finding only directories and creating the full path name

#directory_list = []
#for var in os.listdir():
    #if os.path.isdir(var):
        #directory_list.append(os.path.join(_path, var))


# In[170]:


#generate a list of all assay_names & file paths; zip these together into a dictionary
DES_list = []
file_list = []

for _filepath in _path.iterdir():
    if _filepath.suffix != '.tsv':
        continue
    if _filepath.suffix == '.tsv':
        file_list.append(_filepath)
        
        with open(_filepath, 'rt') as file:
            data = file.read()
            
            DES_search = re.compile(r'DES:.*')
            DES_value = re.findall(DES_search, data) 
            DES_list.append(DES_value)


# In[171]:


def delist(args):
    'Taking mutliple lists within a list and returning a single list of values'
    delist = [var for small_list in args for var in small_list]
    return(delist)


# In[172]:


#delist
DES = delist(DES_list)

des_file = dict(zip(DES, file_list))


# In[173]:


def finder(regex_pattern, data):
    '''regex_pattern is simply the assay name you'd like
    data is the dictionary you're using with key(DES):value(file)'''
    pattern = re.compile(regex_pattern)
    
    desired_files = []
    
    for key, value in data.items():
        if pattern.search(key):
            desired_files.append(value)
    
    return desired_files



# In[192]:


desired_des = [r'DES: 4104_*',r'DES: 4108_*',r'DES: 4114_*',r'DES: 4115_*']

#working on input
#desired_des_input = input('create a list of regex you want')
#desired_des_list = desired_des_input.split(',')
#print(test)

#iterate thru a variety of regex which will be fed to finder function
for var in desired_des:
    desired_file = finder(var, des_file)
    
    tail_list = [] 
    
    #move desired files into new folder
    for var in desired_file:
        #split the path into base
        try:
            head, tail = os.path.split(var)

            src_path = os.path.join(_path, tail)
            dst_path = os.path.join(destination, tail)
            shutil.move(src_path, dst_path) 
        except:
            continue


# In[ ]:




