
# pylint: disable=C0321,C0103,E1221,C0301,E1305,E1121,C0302,C0330
# -*- coding: utf-8 -*-
"""

Methoe to process data : load in memory, split, or save



"""
import os, sys,copy, glob, pathlib, pprint, json, pandas as pd, numpy as np, scipy as sci, sklearn
from IPython.terminal.ipapp import TerminalIPythonApp
from utilmy import pd_read_file


def log(*s):
    print(*s)


def log2(*s):
    print(*s)



def data_load_memory(dfX=None, nsample=-1):
    """
        dfX str, pd.DataFrame,   Spark DataFrame
      
    """
    if isinstance(dfX, pd.DataFrame):
       return dfX

    if isinstance(dfX, tuple):
       if isinstance(dfX[1], list):
            cols = dfX[1]
            if isinstance(dfX[0], pd.DataFrame) :
                return dfX[0][cols]

            if isinstance(dfX[0], str) :
                path = dfX[0]
                dfX = pd_read_file( path + "/*.parquet" , nrows= nsample)
                dfX = dfX[cols]
                return dfX

       if isinstance(dfX[1], dict):
            dd   = dfX[1]
            cols = dd.get('cols', None)

            if isinstance(dfX[0], pd.DataFrame) :
                return dfX[0][cols]

            if isinstance(dfX[0], str) :
                path = dfX[0]
                dfX  = pd_read_file( path + "/*.parquet" , nrows= nsample)
                dfX  = dfX[cols]
                return dfX


    if isinstance(dfX, str):
        
        path = dfX
        #path = dfX[0]
        print(path)
        dfX  = pd_read_file( path + "/*.parquet", nrows= nsample )        
        return dfX


def data_load_memory_iterator(dfX=None, nsample=-1):
    """
        dfX str, pd.DataFrame,   Spark DataFrame

        for dfi in data_load_memory_iterator(dfX=None, nsample=-1):


    """
    if isinstance(dfX, pd.DataFrame):
       return dfX

    if isinstance(dfX, str):
        path  = dfX
        flist = glob.glob( path + "/*.parquet" )
        for fi in flist :
           dfXi  = pd_read_file(fi , nrows= nsample )        
           yield dfXi

def data_generator(dfX,method='pandas',nsample=-1):
    '''
        This Function will take dfx as str or pandas dataframe and yield dataframes in chunks so loading of 
        whole dataset is not required in the memory

    '''
    
    if isinstance(dfX,pd.DataFrame):
        return dfX
    
    if method=='pandas':
        if isinstance(dfX,str):
            if nsample<0:
                nsample=None
            chunks = pd.read_csv(dfX,chunksize=nsample)
            chunks = iter(chunks)
            return chunks
    elif method=='dask':
        from dask import dataframe as dd
        dask_df = dd.read_csv(dfX)
        return dask_df
    


def data_save(dfX=None, path=None, fname='file'):
    """
        dfX: pd.DataFrame, with automatic iterator ii

    """
    flist = glob.glob(path + "/*.parquet")
    imax  = len(flist) + 1  ### Add file
    os.makedirs(path, exist_ok=True)
    dfX.to_parquet( path + f"/{fname}_{imax}.parquet" )



def data_split(dfX, data_pars):
    """  Mini Batch data Split on Disk
    """
    import pandas as pd,  glob
    from utilmy import pd_read_file
    model_path = data_pars.get('model_path',os.getcwd())
    colsX = data_pars.get('colsX',[])
    coly = data_pars.get('coly','')
    split = data_pars.get('split',0.8)
    if  isinstance(dfX, pd.DataFrame) and  data_pars['data_type'] == 'ram'  :
        log2("##### Data Split in RAM  ###################################################")
        log2(dfX.shape)
        dfX    = dfX.sample(frac=1.0)
        itrain = int(split * len(dfX))
        ival   = int(1-split* len(dfX))
        data_pars['train'] = { 'Xtrain' : dfX[colsX].iloc[:itrain, :],
                               'ytrain' : dfX[coly].iloc[:itrain],
                               'Xtest'  : dfX[colsX].iloc[itrain:ival, :],
                               'ytest'  : dfX[coly].iloc[itrain:ival],

                               'Xval'   : dfX[colsX].iloc[ival:, :],
                               'yval'   : dfX[coly].iloc[ival:],
                             }
        return data_pars, ival


    if isinstance(dfX, str) :
        log2("##### Data on Disk Split ############################################")
        m = { 'Xtrain' : model_path + "train/Xtrain/" ,
              'ytrain' : model_path + "train/ytrain/",
              'Xtest'  : model_path + "train/Xtest/",
              'ytest'  : model_path + "train/ytest/",

              'Xval'   : model_path + "train/Xval/",
              'yval'   : model_path + "train/yval/",
            }
        for key, path in m.items() :
           os.makedirs(path, exist_ok =True)

        #flist = glob.glob(dfX + "*")
        flist =  [dfX ]  ### filter
        for i, fi in enumerate(flist) :
            dfXi = pd_read_file(fi)
            log2(dfXi.shape)
            dfX    = dfXi.sample(frac=1.0)
            itrain = int(split * len(dfXi))
            ival   = int(1-split * len(dfXi))
            dfXi[colsX].iloc[:itrain, :].to_parquet(m['Xtrain']     + f"/file_{i}.parquet" )
            dfXi[[coly]].iloc[:itrain].to_parquet(  m['ytrain']     + f"/file_{i}.parquet" )

            dfXi[colsX].iloc[itrain:ival, :].to_parquet(m['Xtest']  + f"/file_{i}.parquet" )
            dfXi[[coly]].iloc[itrain:ival].to_parquet(  m['ytest']  + f"/file_{i}.parquet" )

            dfXi[colsX].iloc[ival:, :].to_parquet(      m['Xval']   + f"/file_{i}.parquet" )
            dfXi[[coly]].iloc[ival:].to_parquet(        m['yval']   + f"/file_{i}.parquet" )

        #### date_type :  'ram', 'pandas', tf_data,  torch_data,  #####################
        data_pars['data_type'] = data_pars.get('data_type', 'ram')  ### Tf dataset, pytorch
        data_pars['train']     = m
        ival = 0
        return data_pars, ival

import os

def test1():
    '''
        This Test has been created for working of Data Split Method
    '''
    print(f'OS Current Working Directory:{os.getcwd()}')
    df_pandas = pd.read_csv('datasets/petfinder_mini.csv') #Pass it as Pandas Dataframe
    df_path = 'datasets/petfinder_mini.csv' #Pass it as path to file.
    
    data_pars = {

        'data_type':'ram',
        'colsX':['Age','Breed1'],
        'coly':'Type',
        'model_path':'/home/tushargoel/Desktop/dsa2',

    }
    
    data = data_split(df_path,data_pars)
    print(data)

def test2():
    '''
        This Test has been created for working of Data Load in Memory Method
    '''
    df_pandas = pd.read_csv('datasets/petfinder_mini.csv') #Pass it as Pandas Dataframe
    df_path =  'train/Xtrain' #Pass the parquet files folder as path

    data = data_load_memory(df_path)
    print(data)

def test3():
    '''
        Loading of Huge Data Files in chunks using pandas and Dask
    '''

    method='dask'
    df_path = 'datasets/petfinder_mini.csv'

    if method=='pandas':
        
        iterations = data_generator(df_path,method,10)

        while True:
            try:
                df = next(iterations)
                print(df)
            except:
                break
    
    elif method=='dask':
        
        df = data_generator(df_path,method)
        print(df.head())
        



if __name__ == '__main__':
    import fire 
    fire.Fire(test3)




"""
    if isinstance(dfX, pd.DataFrame):
        log2(dfX.shape)
        dfX    = dfX.sample(frac=1.0)
        itrain = int(0.6 * len(dfX))
        ival   = int(0.8 * len(dfX))
        dfX[colsX].iloc[:itrain, :].to_parquet(m['Xtrain']     + "/file_01.parquet" )
        dfX[[coly]].iloc[:itrain].to_parquet(  m['ytrain']     + "/file_01.parquet" )

        dfX[colsX].iloc[itrain:ival, :].to_parquet(m['Xtest']  + "/file_01.parquet" )
        dfX[[coly]].iloc[itrain:ival].to_parquet(  m['ytest']  + "/file_01.parquet" )

        dfX[colsX].iloc[ival:, :].to_parquet(      m['Xval']  + "/file_01.parquet"  )
        dfX[[coly]].iloc[ival:].to_parquet(        m['yval']  + "/file_01.parquet"  )
        
"""




