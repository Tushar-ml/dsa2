import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,DenseFeatures
import pandas as pd
import pprint
import zipfile
import numpy as np
from sklearn.preprocessing import LabelEncoder
from glob import glob



def pack_features_vector(features, labels):
    """Pack the features into a single array."""
    features = tf.stack(list(features.values()), axis=1)
    return features, labels


class dictEval(object):
    '''
    https://www.tutorialspoint.com/How-to-recursively-iterate-a-nested-Python-dictionary
    https://stackoverflow.com/questions/45335445/recursively-replace-dictionary-values-with-matching-key
def replace_item(obj, key, replace_value):
    for k, v in obj.items():
        if isinstance(v, dict):
            obj[k] = replace_item(v, key, replace_value)
    if key in obj:
        obj[key] = replace_value
    return obj
    '''
    global dst
    import glob

    def __init__(self):
        self.dst = {}

    def reset(self):
        self.dst = {}

    def eval_dict(self,src, dst={}):
        for key, value in src.items():
            if isinstance(value, dict):
                node     = dst.setdefault(key, {})
                dst[key] = self.eval_dict(value, node)

            else:
                if ":@lazy" not in key :
                    dst[key] = value
                    continue

                ###########################################################################################
                key2           = key.split(':@lazy')[0]
                path_pattern   = value

                if 'tf' in key :
                    #log('TF is HEre')
                    self.tf_dataset_create(key2,path_pattern,)

                if 'pandas' in key :
                    self.pandas_create(key2, path_pattern, )
        return dst
        
    def tf_dataset_create(self, key2, path_pattern, batch_size=32, **kw):
        """
          https://www.tensorflow.org/api_docs/python/tf/data/experimental/make_csv_dataset
                tf.data.experimental.make_csv_dataset(
            file_pattern, batch_size, column_names=None, column_defaults=None,
            label_name=None, select_columns=None, field_delim=',',
            use_quote_delim=True, na_value='', header=True, num_epochs=None,
            shuffle=True, shuffle_buffer_size=10000, shuffle_seed=None,
            prefetch_buffer_size=None, num_parallel_reads=None, sloppy=False,
            num_rows_for_inference=100, compression_type=None, ignore_errors=False
        )
        :return:
        """
        # import glob
        # flist = glob.glob(path_pattern + "/*")
        print(f'Path Pattern Observed: {path_pattern}')
        dataset = tf.data.experimental.make_csv_dataset(path_pattern,label_name='y',  batch_size=batch_size, ignore_errors=True)
        dataset = dataset.map(pack_features_vector)
        print(dataset)
        dst[key2] = dataset.repeat()


    def pandas_create(self, key2, path, ):
        import glob
        from utilmy import pd_read_file
        # flist = glob.glob(path)
        dst[key2] = pd_read_file(path)


def log(*s):
    print(*s)



###################################################################################
if __name__ == '__main__':
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
    }



    test = dictEval()
    data_pars2 = test.eval_dict(data_pars)
    print(dst)

    from tensorflow.keras import layers
    model = tf.keras.Sequential([
        layers.Flatten(),
        layers.Dense(256, activation='elu'),
        layers.Dense(32, activation='elu'),
        layers.Dense(1,activation='sigmoid') 
        ])


    model.compile(optimizer='adam',
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                metrics=['accuracy'])    
    model.fit(dst['Xtrain'],
            steps_per_epoch=20,
            epochs=30,
            verbose=1
            )






dst = dict()
def eval_dict(src, dst={}):
    import pandas as pd
    for key, value in src.items():
        if isinstance(value, dict):
            node = dst.setdefault(key, {})
            eval_dict(value, node)
        else:
            if "@lazy" not in key :
               dst[key] = value
            else :
                key2 = key.split(":")[-1]
                if 'pandas.read_csv' in key :
                    dst[key2] = pd.read_csv(value)
                elif 'pandas.read_parquet' in key :
                    dst[key2] = pd.read_parquet(value)
    return dst





"""    
if ext == 'zip':
    zf = zipfile.ZipFile(value)
    fileNames = zf.namelist()
    for idx,file in enumerate(fileNames):
        if file.split('.')[-1] in ['csv','txt']:
            file = 'datasets/'+file
            dst[key2+'_'+str(idx)] = pd.read_csv(file)
elif ext in ['csv','txt']:
        dst[key2] = pd.read_csv(value)
elif ext == 'parquet':
        dst[key2] = pd.read_parquet(value)
return dst
"""

"""
if ext == 'zip':
    zf        = zipfile.ZipFile(path_pattern)
    fileNames = zf.namelist()
    for idx,file in enumerate(fileNames):
        if file.split('.')[-1] in ['csv','txt']:
            file = 'datasets/'+file
            try:
                dataset = tf.data.experimental.make_csv_dataset(file, label_name=coly, batch_size=32, ignore_errors=True)
                dataset = dataset.map(pack_features_vector)
                dst[key2+'_'+str(idx)] = dataset.repeat()
            except:
                pass
elif ext in ['csv','txt']:
            dataset = tf.data.experimental.make_csv_dataset(path_pattern, label_name=coly, batch_size=32, ignore_errors=True)
            dataset = dataset.map(pack_features_vector)
            dst[key2] = dataset.repeat()
elif ext == 'parquet':
        filename = path_pattern.split('.')[0] + '.csv'
        pd.read_parquet(path_pattern).to_csv(filename)
        pd.read_parquet(path_pattern).to_csv(filename)
        dataset = tf.data.experimental.make_csv_dataset(filename, label_name=coly, batch_size=32, ignore_errors=True)
        dataset = dataset.map(pack_features_vector)
        dst[key2] = dataset.repeat()
"""


"""
    dst = {}
    dataset_url = 'http://storage.googleapis.com/download.tensorflow.org/data/petfinder-mini.zip'
    csv_file    = 'datasets/petfinder-mini/petfinder-mini.csv'
    zip_file = 'datasets/petfinder_mini.zip'
    #tf.keras.utils.get_file('petfinder_mini.zip', dataset_url,extract=True, cache_dir='.')
    #Uncomment This File for preprocessing the CSV File
df = pd.read_csv('datasets/petfinder-mini/petfinder-mini.csv')
    col = ['Type', 'Breed1', 'Gender', 'Color1', 'Color2', 'MaturitySize',
        'FurLength', 'Vaccinated', 'Sterilized', 'Health',
        ]
    df.drop(['Description'],axis=1,inplace=True)
    df[col] = df[col].astype(str).apply(LabelEncoder().fit_transform)
    df.to_csv('datasets/petfinder-mini/petfinder-mini.csv')
"""
