
# pylint: disable=C0321,C0103,E1221,C0301,E1305,E1121,C0302,C0330
# -*- coding: utf-8 -*-
"""

Methoe to process data : load in memory, split, or save



"""
import os, sys,copy, glob, pathlib, pprint, json, pandas as pd, numpy as np, scipy as sci, sklearn
from utilmy import pd_read_file



def data_load_memory(dfX=None, nsample=-1):
    """
        dfX str, pd.DataFrame,   Spark DataFrame
      
    """
    if isinstance(dfX, pd.DataFrame):
       return dfX

    if isinstance(dfX, tuple):
       if isintance(dfX[1], list):
            cols = dfX[1]
            if isinstance(dfX[0], pd.DataFrame):
                return dfX[0][cols]

            if isinstance(dfX[0], str) :
                path = dfX[0]
                dfX = pd_read_file( path + "/*.parquet" , nrows= nsample)
                dfX = dfX[cols]
                return dfX

       if isintance(dfX[1], dict):
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
        path = dfX[0]
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
           yield dfX

    if isinstance(dfX, tuple):
       if isintance(dfX[1], list):
            cols = dfX[1]
            if isinstance(dfX[0], pd.DataFrame) :
                return dfX[0][cols]

            if isinstance(dfX[0], str) :
                path = dfX[0]
                dfX = pd_read_file( path + "/*.parquet" , nrows= nsample)
                dfX = dfX[cols]
                return dfX

       if isintance(dfX[1], dict):
            dd   = dfX[1]
            cols = dd.get('cols', None)

            if isinstance(dfX[0], pd.DataFrame) :
                return dfX[0][cols]

            if isinstance(dfX[0], str) :
                path = dfX[0]
                flist 
                dfX  = pd_read_file( path + "/*.parquet" , nrows= nsample)
                dfX  = dfX[cols]
                return dfX



def data_save(dfX=None, path=None, fname='file'):
    """
        dfX: pd.DataFrame, with automatic iterator ii

    """
    flist = glob.glob(path + "/*.parquet")
    imax  = len(flist) + 1  ### Add file
    os.makedirs(path, exist_ok=True)
    dfX[cols].to_parquet( path + f"/{fname}_{imax}.parquet" )



def data_split(dfX, data_pars, model_path, colsX, coly):
    """  Mini Batch data Split on Disk
    """
    import pandas as pd

    ##### Dense Dict :  #################################################
    if data_pars['data_type'] == 'ram':
        log2(dfX.shape)
        dfX    = dfX.sample(frac=1.0)
        itrain = int(0.6 * len(dfX))
        ival   = int(0.8 * len(dfX))
        data_pars['train'] = { 'Xtrain' : dfX[colsX].iloc[:itrain, :],
                               'ytrain' : dfX[coly].iloc[:itrain],
                               'Xtest'  : dfX[colsX].iloc[itrain:ival, :],
                               'ytest'  : dfX[coly].iloc[itrain:ival],

                               'Xval'   : dfX[colsX].iloc[ival:, :],
                               'yval'   : dfX[coly].iloc[ival:],
                             }
        return data_pars

    ##### Split on  Path  ###############################################
    m = { 'Xtrain' : model_path + "train/Xtrain/" ,
          'ytrain' : model_path + "train/ytrain/",
          'Xtest'  : model_path + "train/Xtest/",
          'ytest'  : model_path + "train/ytest/",

          'Xval'   : model_path + "train/Xval/",
          'yval'   : model_path + "train/yval/",
        }
    for key, path in m.items() :
       os.makedirs(path, exist_ok =True)


    if isinstance(dfX, str) :
        import glob
        from utilmy import pd_read_file
        flist = glob.glob(dfX + "*")
        flist =  [t for  t in flist ]  ### filter
        for i, fi in enumerate(flist) :
            dfXi = pd_read_file(fi)
            log2(dfXi.shape)
            dfX    = dfXi.sample(frac=1.0)
            itrain = int(0.6 * len(dfXi))
            ival   = int(0.8 * len(dfXi))
            dfXi[colsX].iloc[:itrain, :].to_parquet(m['Xtrain']  + f"/file_{i}.parquet" )
            dfXi[[coly]].iloc[:itrain].to_parquet(  m['ytrain']  + f"/file_{i}.parquet" )

            dfXi[colsX].iloc[itrain:ival, :].to_parquet(m['Xtest']  + f"/file_{i}.parquet" )
            dfXi[[coly]].iloc[itrain:ival].to_parquet(  m['ytest']  + f"/file_{i}.parquet" )

            dfXi[colsX].iloc[ival:, :].to_parquet(      m['Xval']  + f"/file_{i}.parquet" )
            dfXi[[coly]].iloc[ival:].to_parquet(        m['yval']  + f"/file_{i}.parquet"  )


    if isinstance(dfX, pd.DataFrame):
        log2(dfX.shape)
        dfX    = dfX.sample(frac=1.0)
        itrain = int(0.6 * len(dfX))
        ival   = int(0.8 * len(dfX))
        dfX[colsX].iloc[:itrain, :].to_parquet(m['Xtrain']  + "/file_01.parquet" )
        dfX[[coly]].iloc[:itrain].to_parquet(  m['ytrain']  + "/file_01.parquet" )

        dfX[colsX].iloc[itrain:ival, :].to_parquet(m['Xtest']  + "/file_01.parquet" )
        dfX[[coly]].iloc[itrain:ival].to_parquet(  m['ytest']  + "/file_01.parquet" )

        dfX[colsX].iloc[ival:, :].to_parquet(      m['Xval']  + "/file_01.parquet" )
        dfX[[coly]].iloc[ival:].to_parquet(        m['yval']  + "/file_01.parquet"  )


    #### date_type :  'ram', 'pandas', tf_data,  torch_data,  #####################
    data_pars['data_type'] = data_pars.get('data_type', 'ram')  ### Tf dataset, pytorch
    data_pars['train']     = m
    return data_pars







