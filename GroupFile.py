#!/usr/bin/env python
# coding: utf-8

# In[1]:


def groupfile():
    
    from nptdms import TdmsFile
    import os, shutil, re, csv
    import pandas as pd
    import numpy as np
    fullpath = os.getcwd()
    fileall = os.listdir(fullpath)
    if 'groupfile.xlsx' in fileall:
        os.remove('groupfile.xlsx')
        print('remove previous groupfile.xlsx')
    _nsre = re.compile('([0-9]+)')
    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split(_nsre, s)]
    pau_file = [os.path.join(root, name) for root, dirs, files in os.walk(fullpath) for name in files if name == 'PauseSummary.csv']
    pau_file.sort(key=natural_sort_key)

    v_file = [os.path.join(root, name) for root, dirs, files in os.walk(fullpath) for name in files if name == 'V_category.csv']
    v_file.sort(key=natural_sort_key)

    dis_file = [os.path.join(root, name) for root, dirs, files in os.walk(fullpath) for name in files if name == 'TotalDistance.csv']
    dis_file.sort(key=natural_sort_key)
    with pd.ExcelWriter('groupfile.xlsx', engine = 'xlsxwriter') as writer:
        i=j=k=0
        for file in pau_file:
            tmp = pd.read_csv(file)
            tmp = pd.DataFrame(tmp)
            if i==0:
                pause_dt = tmp
            else:
                tmp = tmp.drop(columns='Sample') 
                #pause_dt = pd.merge(pause_dt,tmp,on = 'Sample')
                pause_dt = pd.concat([pause_dt,tmp],axis = 1)
            i+=1

        for file in v_file:
            tmp = pd.read_csv(file)
            tmp = pd.DataFrame(tmp)
            if j==0:
                vel_dt = tmp
            else:
                vel_dt = pd.concat([vel_dt,tmp],axis = 1)
            j+=1    

        for file in dis_file:
            tmp = pd.read_csv(file)
            tmp = pd.DataFrame(tmp)
            if k==0:
                dis_dt = tmp
            else:
                dis_dt = pd.concat([dis_dt,tmp],axis = 1)
            k+=1 

        pause_dt.to_excel(writer,sheet_name = 'PauseSummary',index = False)
        vel_dt.to_excel(writer,sheet_name = 'V_Category',index = False)
        dis_dt.to_excel(writer,sheet_name = 'TotalDistance',index = False)

