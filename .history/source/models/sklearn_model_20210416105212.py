'''from sklearn.linear_model import *
from sklearn.svm import *
from sklearn.tree import *
from sklearn.ensemble import *'''














'''if __name__ == '__main__':
    ## pip install adataset
    root = ""
    from adatasets import test_dataset_classification_fake
    df, p = test_dataset_classification_fake(nrows=100)
    print(df.columns)
    df = df.astype('float')
    df.to_parquet(root+ 'datasets/parquet/f01.parquet')
    df.to_parquet(root + 'datasets/parquet/f02.parquet' )
    parquet_path = root + 'datasets/parquet/f*.parquet'

    df[ [p['coly']] ].to_parquet(root + 'datasets/parquet/label_01.parquet' )
    df[ [p['coly']] ].to_parquet(root + 'datasets/parquet/label_01.parquet' )
    parquet_path_y = root + 'datasets/parquet/label*.parquet'


    df.to_csv(root + 'datasets/csv/f01.csv',index=False )
    df.to_csv(root + 'datasets/csv/f02.csv' ,index=False)
    csv_path     = root + 'datasets/csv/f01.csv'


    df.to_csv(root + 'datasets/zip/f01.zip', compression='gzip' )
    df.to_csv(root + 'datasets/zip/f02.zip', compression='gzip' )
    zip_path     = root + 'datasets/zip/*.zip'



    data_pars = {

        ### ModelTarget-Keyname : Path
        'Xtrain:@lazy_tf'  : csv_path, #CSV file extraction #Tensorflow Dataset
        #'Xtest:@lazy_tf'   : zip_path,     #zip File Extraction
        'Xval:@lazy_pandas': csv_path,     #Pandas


        #'ytrain:@lazy_tf' : parquet_path_y,     #Pandas
        #'ytest:@lazy_tf ' : parquet_path_y,     #Pandas


        'pars': 23,
        "batch_size" : 32,
        "n_train": 500, 
        "n_test": 500,

        'sub-dict' :{ 'one' : {'twp': 2 } }
    }'''

'''
import pandas as pd
df = pd.DataFrame({'A':[2,3,5], 'B': [4,6,10]})
print(df.set_index('A').columns)'''


import numpy as np 

a = np.array([5, 7, 3, 1])
b = np.array([90, 50, 0]) 

c = a * b
print (c)
