'''
import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('datasets/petfinder-mini/petfinder-mini.csv')

col = ['Type', 'Breed1', 'Gender', 'Color1', 'Color2', 'MaturitySize','FurLength', 'Vaccinated', 'Sterilized', 'Health']

df.drop(['Description'],axis=1,inplace=True)
df[col] = df[col].astype(str).apply(LabelEncoder().fit_transform)
#df.to_csv('datasets/petfinder-mini/petfinder-mini.csv')
df = df.astype('int32')
df.to_parquet('datasets/petfinder_mini.parquet',index=False)
'''
import os
from petastorm import make_batch_reader
from petastorm.tf_utils import make_petastorm_dataset
import tensorflow as tf
from tensorflow.data.experimental import unbatch
from tensorflow.io import decode_raw
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.layers import Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
# from pyspark.context import SparkContext
# from pyspark.sql.session import SparkSession
#sc = SparkContext('local')
# spark = SparkSession(sc)
from tensorflow.keras import layers



from adatasets import test_dataset_classification_fake
df, d = test_dataset_classification_fake(nrows=100)
print(df)
colnum, colcat, coly = d['colnum'], d['colcat'], d['coly']

path = os.path.abspath("data/input/ztest/fake/").replace("\\","/")
os.makedirs(path, exist_ok=True)

df.to_parquet(path + "/feature_01.parquet")
df.to_parquet(path + "/feature_02.parquet")



def pack_features_vector(features, labels):
    """Pack the features into a single array."""
    features = tf.stack(list(features.values()), axis=1)
    return features, labels

path2 = 'file:' + path +"/feature_01.parquet" #.replace("D:/", "")


batch_size = 32
with make_batch_reader( path2 ) as reader:
    dataset  = make_petastorm_dataset(reader)
    iterator = dataset.make_one_shot_iterator()

    tensor = iterator.get_next()

    print("dataset", dataset, tensor )


    model = tf.keras.Sequential([
           layers.Flatten(),
           layers.Dense(256, activation='elu'),
           layers.Dense(32,  activation='elu'),
           layers.Dense(1,   activation='sigmoid')
           ])
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.fit([tensor],
           steps_per_epoch=1,
           epochs=1,
           verbose=1
           )
    print('Hurray Successfully Initiated')




########################################################################################################################
def fIt_(dataset_url, training_iterations, batch_size, evaluation_interval):
    """
https://github.com/uber/petastorm/blob/master/petastorm/reader.py#L61-L134

def make_batch_reader(dataset_url_or_urls,
                      schema_fields=None,
                      reader_pool_type='thread', workers_count=10,
                      shuffle_row_groups=True, shuffle_row_drop_partitions=1,
                      predicate=None,
                      rowgroup_selector=None,
                      num_epochs=1,
                      cur_shard=None, shard_count=None,
                      cache_type='null', cache_location=None, cache_size_limit=None,
                      cache_row_size_estimate=None, cache_extra_settings=None,
                      hdfs_driver='libhdfs3',
                      transform_spec=None,
                      filters=None,
                      s3_config_kwargs=None,
                      zmq_copy_buffers=True,
                      filesystem=None):

    Creates an instance of Reader for reading batches out of a non-Petastorm Parquet store.
    Currently, only stores having native scalar parquet data types are supported.
    Use :func:`~petastorm.make_reader` to read Petastorm Parquet stores generated with
    :func:`~petastorm.etl.dataset_metadata.materialize_dataset`.
    NOTE: only scalar columns or array type (of primitive type element) columns are currently supported.
    NOTE: If without `schema_fields` specified, the reader schema will be inferred from parquet dataset. then the
    reader schema fields order will preserve parqeut dataset fields order (partition column come first), but if
    setting `transform_spec` and specified `TransformSpec.selected_fields`, then the reader schema fields order
    will be the order of 'selected_fields'.
     dataset_url_or_urls: a url to a parquet directory or a url list (with the same scheme) to parquet files.
        e.g. ``'hdfs://some_hdfs_cluster/user/yevgeni/parquet8'``, or ``'file:///tmp/mydataset'``,
        or ``'s3://bucket/mydataset'``, or ``'gs://bucket/mydataset'``,
        or ``[file:///tmp/mydataset/00000.parquet, file:///tmp/mydataset/00001.parquet]``.
     schema_fields: A list of regex pattern strings. Only columns matching at least one of the
        patterns in the list will be loaded.
     reader_pool_type: A string denoting the reader pool type. Should be one of ['thread', 'process', 'dummy']
        denoting a thread pool, process pool, or running everything in the master thread. Defaults to 'thread'
     workers_count: An int for the number of workers to use in the reader pool. This only is used for the
        thread or process pool. Defaults to 10
     shuffle_row_groups: Whether to shuffle row groups (the order in which full row groups are read)
     shuffle_row_drop_partitions: This is is a positive integer which determines how many partitions to
        break up a row group into for increased shuffling in exchange for worse performance (extra reads).
        For example if you specify 2 each row group read will drop half of the rows within every row group and
        read the remaining rows in separate reads. It is recommended to keep this number below the regular row
        group size in order to not waste reads which drop all rows.
     predicate: instance of :class:`.PredicateBase` object to filter rows to be returned by reader. The predicate
        will be passed a pandas DataFrame object and must return a pandas Series with boolean values of matching
        dimensions.
     rowgroup_selector: instance of row group selector object to select row groups to be read
     num_epochs: An epoch is a single pass over all rows in the dataset. Setting ``num_epochs`` to
        ``None`` will result in an infinite number of epochs.
     cur_shard: An int denoting the current shard number. Each node reading a shard should
        pass in a unique shard number in the range [0, shard_count). shard_count must be supplied as well.
        Defaults to None
     shard_count: An int denoting the number of shards to break this dataset into. Defaults to None
     cache_type: A string denoting the cache type, if desired. Options are [None, 'null', 'local-disk'] to
        either have a null/noop cache or a cache implemented using diskcache. Caching is useful when communication
        to the main data store is either slow or expensive and the local machine has large enough storage
        to store entire dataset (or a partition of a dataset if shard_count is used). By default will be a null cache.
     cache_location: A string denoting the location or path of the cache.
     cache_size_limit: An int specifying the size limit of the cache in bytes
     cache_row_size_estimate: An int specifying the estimated size of a row in the dataset
     cache_extra_settings: A dictionary of extra settings to pass to the cache implementation,
     hdfs_driver: A string denoting the hdfs driver to use (if using a dataset on hdfs). Current choices are
        libhdfs (java through JNI) or libhdfs3 (C++)
     transform_spec: An instance of :class:`~petastorm.transform.TransformSpec` object defining how a record
        is transformed after it is loaded and decoded. The transformation occurs on a worker thread/process (depends
        on the ``reader_pool_type`` value).
     filters: (List[Tuple] or List[List[Tuple]]): Standard PyArrow filters.
        These will be applied when loading the parquet file with PyArrow. More information
        here: https://arrow.apache.org/docs/python/generated/pyarrow.parquet.ParquetDataset.html
     s3_config_kwargs: dict of parameters passed to ``botocore.client.Config``
     zmq_copy_buffers: A bool indicating whether to use 0mq copy buffers with ProcessPool.
     filesystem: An instance of ``pyarrow.FileSystem`` to use. Will ignore s3_config_kwargs and
        other filesystem configs if it's provided.
    :return: A :class:`Reader` object
    

    :return:
    """
    # model0 =  Keras model

    batch_size = 128
    num_classes = 10
    epochs = 12

    from petastorm.reader import Reader, make_batch_reader
    from petastorm.tf_utils import make_petastorm_dataset

    Xtrain, Xtest, yt   =get_dataset( , mode='petastorm')

    ### Inside fit
    train_reader = Reader( dataset_url_train, num_epochs=epochs)
    test_reader =  Reader( dataset_url_test,  num_epochs=epochs)

    train_dataset = make_petastorm_dataset(train_reader)
    train_dataset = train_dataset.map(lambda x: (tf.reshape(x.image, (28, 28, 1)), tf.reshape(x.digit, [1])))
    train_dataset = train_dataset.batch(batch_size, drop_remainder=True)


    test_dataset = make_petastorm_dataset(test_reader)
    test_dataset = test_dataset.map(lambda x: (tf.reshape(x.image, (28, 28, 1)), tf.reshape(x.digit, [1])))
    test_dataset = test_dataset.batch(batch_size, drop_remainder=True)

    hist = model0.fit(train_dataset,
              verbose=1,
              epochs=1,
              steps_per_epoch=100,
              validation_steps=10,
              validation_data=test_dataset)

    score = model.evaluate(test_dataset, steps=10, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    train_reader.close()
    test_reader.close()





from __future__ import division, print_function

import argparse
import os

import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.models import Sequential

from examples.mnist import DEFAULT_MNIST_DATA_PATH
from petastorm.reader import Reader
from petastorm.tf_utils import make_petastorm_dataset


def train_and_test(dataset_url, training_iterations, batch_size, evaluation_interval):
    batch_size = 128
    num_classes = 10
    epochs = 12

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(28, 28, 1)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    with Reader(os.path.join(dataset_url, 'train'), num_epochs=epochs) as train_reader:
        with Reader(os.path.join(dataset_url, 'test'), num_epochs=epochs) as test_reader:
            train_dataset = make_petastorm_dataset(train_reader) 
            train_dataset = train_dataset.map(lambda x: (tf.reshape(x.image, (28, 28, 1)), tf.reshape(x.digit, [1]))) 
            train_dataset = train_dataset.batch(batch_size, drop_remainder=True)


            test_dataset = make_petastorm_dataset(test_reader) 
            test_dataset = test_dataset.map(lambda x: (tf.reshape(x.image, (28, 28, 1)), tf.reshape(x.digit, [1]))) 
            test_dataset = test_dataset.batch(batch_size, drop_remainder=True)

            model.fit(train_dataset,
                      verbose=1,
                      epochs=1,
                      steps_per_epoch=100,
                      validation_steps=10,
                      validation_data=test_dataset)

            score = model.evaluate(test_dataset, steps=10, verbose=0)
            print('Test loss:', score[0])
            print('Test accuracy:', score[1])

    train_reader.close()
    test_reader.close()


def main():
    # Training settings
    parser = argparse.ArgumentParser(description='Petastorm Tensorflow MNIST Example')
    default_dataset_url = 'file://{}'.format(DEFAULT_MNIST_DATA_PATH)
    parser.add_argument('--dataset-url', type=str,
                        default=default_dataset_url, metavar='S',
                        help='hdfs:// or file:/// URL to the MNIST petastorm dataset'
                             '(default: %s)' % default_dataset_url)
    parser.add_argument('--training-iterations', type=int, default=100, metavar='N',
                        help='number of training iterations to train (default: 100)')
    parser.add_argument('--batch-size', type=int, default=100, metavar='N',
                        help='input batch size for training (default: 100)')
    parser.add_argument('--evaluation-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before evaluating the model accuracy (default: 10)')
    args = parser.parse_args()

    train_and_test(
        dataset_url=args.dataset_url,
        training_iterations=args.training_iterations,
        batch_size=args.batch_size,
        evaluation_interval=args.evaluation_interval,
    )




"""
https://github.com/uber/petastorm/tree/master/examples/hello_world/external_dataset

"""
from petastorm.tf_utils import tf_tensors, make_petastorm_dataset
def tensorflow_hello_world(dataset_url='file:///tmp/external_dataset'):
    # Example: tf_tensors will return tensors with dataset data
    with make_batch_reader(dataset_url) as reader:
        tensor = tf_tensors(reader)
        with tf.Session() as sess:
            # Because we are using make_batch_reader(), each read returns a batch of rows instead of a single row
            batched_sample = sess.run(tensor)
            print("id batch: {0}".format(batched_sample.id))

    # Example: use tf.data.Dataset API
    with make_batch_reader(dataset_url) as reader:
        dataset = make_petastorm_dataset(reader)
        iterator = dataset.make_one_shot_iterator()
        tensor = iterator.get_next()
        with tf.Session() as sess:
            batched_sample = sess.run(tensor)
            print("id batch: {0}".format(batched_sample.id))





"""Minimal example of how to read samples from a dataset generated by `generate_external_dataset.py`
using pytorch, using make_batch_reader() instead of make_reader()"""
from petastorm import make_batch_reader
from petastorm.pytorch import DataLoader


def pytorch_hello_world(dataset_url='file:///tmp/external_dataset'):
    with DataLoader(make_batch_reader(dataset_url)) as train_loader:
        sample = next(iter(train_loader))
        # Because we are using make_batch_reader(), each read returns a batch of rows instead of a single row
        print("id batch: {0}".format(sample['id']))



"""Minimal example of how to read samples from a dataset generated by `generate_non_petastorm_dataset.py`
using plain Python"""

from petastorm import make_batch_reader


def python_hello_world(dataset_url='file:///tmp/external_dataset'):
    # Reading data from the non-Petastorm Parquet via pure Python
    with make_batch_reader(dataset_url, schema_fields=["id", "value1", "value2"]) as reader:
        for schema_view in reader:
            # make_batch_reader() returns batches of rows instead of individual rows
            print("Batched read:\nid: {0} value1: {1} value2: {2}".format(
                schema_view.id, schema_view.value1, schema_view.value2))













