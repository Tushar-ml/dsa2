# pylint: disable=C0321,C0103,E1221,C0301,E1305,E1121,C0302,C0330
# -*- coding: utf-8 -*-
"""

https://github.com/mljar/mljar-supervised

  python  test_automl.py  train    > zlog/log_titanic_train.txt 2>&1
  python  test_automl.py  predict  > zlog/log_titanic_predict.txt 2>&1


conda install -c conda-forge fastparquet

 dtreeviz==1.0, which is not installed.
 fastparquet==0.4.1, which is not installed.
 wordcloud==1.7.0, which is not installed.


 catboost==0.24.1, but you'll have catboost 0.22 which is incompatible.
 category-encoders==2.2.2, but you'll have category-encoders 2.1.0 which is incompatible.
 lightgbm==3.0.0, but you'll have lightgbm 2.3.0 which is incompatible.
 numpy>=1.18.5, but you'll have numpy 1.18.1 which is incompatible.
 pandas==1.1.2, but you'll have pandas 0.25.3 which is incompatible.
 pyarrow==0.17.0, but you'll have pyarrow 2.0.0 which is incompatible.
 scipy==1.4.1, but you'll have scipy 1.3.1 which is incompatible.
 seaborn==0.10.1, but you'll have seaborn 0.10.0 which is incompatible.
 shap==0.36.0, but you'll have shap 0.35.0 which is incompatible.
 tabulate==0.8.7, but you'll have tabulate 0.8.6 which is incompatible.
 xgboost==1.2.0, but you'll have xgboost 1.3.3 which is incompatible.




"""
import warnings, copy, os, sys
warnings.filterwarnings('ignore')

####################################################################################
###### Path ########################################################################
root_repo      =  os.path.abspath(os.getcwd()).replace("\\", "/") + "/"     ; print(root_repo)
THIS_FILEPATH  =  os.path.abspath(__file__) 

sys.path.append(root_repo)
from source.util_feature import save,os_get_function_name




def global_pars_update(model_dict,  data_name, config_name):
    print("config_name", config_name)
    dir_data  = root_repo + "/data/"  ; print("dir_data", dir_data)

    m                      = {}
    m['config_path']       = THIS_FILEPATH  
    m['config_name']       = config_name

    #### peoprocess input path
    m['path_data_preprocess'] = dir_data + f'/input/{data_name}/train/'

    #### train input path
    dir_data_url              = "https://github.com/arita37/dsa2_data/tree/master/"  #### Remote Data directory
    m['path_data_train']      = dir_data_url + f'/input/{data_name}/train/'
    m['path_data_test']       = dir_data_url + f'/input/{data_name}/test/'
    #m['path_data_val']       = dir_data + f'/input/{data_name}/test/'

    #### train output path
    m['path_train_output']    = dir_data + f'/output/{data_name}/{config_name}/'
    m['path_train_model']     = dir_data + f'/output/{data_name}/{config_name}/model/'
    m['path_features_store']  = dir_data + f'/output/{data_name}/{config_name}/features_store/'
    m['path_pipeline']        = dir_data + f'/output/{data_name}/{config_name}/pipeline/'


    #### predict  input path
    m['path_pred_data']       = dir_data + f'/input/{data_name}/test/'
    m['path_pred_pipeline']   = dir_data + f'/output/{data_name}/{config_name}/pipeline/'
    m['path_pred_model']      = dir_data + f'/output/{data_name}/{config_name}/model/'

    #### predict  output path
    m['path_pred_output']     = dir_data + f'/output/{data_name}/pred_{config_name}/'

    #####  Generic
    m['n_sample']             = model_dict['data_pars'].get('n_sample', 5000)

    model_dict[ 'global_pars'] = m
    return model_dict



####################################################################################
##### Params########################################################################
config_default   = 'config1'    ### name of function which contains data configuration


########
cols_input_type_1 = {
     "coly"   :   "Survived"
    ,"colid"  :   "PassengerId"
    ,"colcat" :   ["Sex", "Embarked" ]
    ,"colnum" :   ["Pclass", "Age","SibSp", "Parch","Fare"]
    ,"coltext" :  []
    ,"coldate" :  []
    ,"colcross" : [ "Name", "Sex", "Ticket","Embarked","Pclass", "Age", "SibSp", ]
}


####################################################################################
def config1() :
    """
       ONE SINGLE DICT Contains all needed informations for
       used for titanic classification task
    """
    data_name    = "titanic"         ### in data/input/
    model_class  = 'AutoML'  ### ACTUAL Class name for model_sklearn.py
    n_sample     = 1000

    def post_process_fun(y):   ### After prediction is done
        return  int(y)

    def pre_process_fun(y):    ### Before the prediction is done
        return  int(y)


    model_dict = {'model_pars': {
        ### LightGBM API model   #######################################
         'model_class': model_class
        ,'model_pars' : {
            'total_time_limit' : 20,
            'algorithms' : 'auto',
            'results_path' :   root_repo  + f'/data/output/{data_name}/{os_get_function_name()}/automl_1',
            'eval_metric' : 'auto'

            # mode='Explain',
            # ml_task='auto', model_time_limit=None, algorithms='auto', train_ensemble=True,
            # stack_models='auto', eval_metric='auto', validation_strategy='auto', explain_level='auto',
            # golden_features='auto', features_selection='auto', start_random_models='auto',
            # hill_climbing_steps='auto', top_models_to_improve='auto', verbose=1, random_state=1234)
                        }

        , 'post_process_fun' : post_process_fun   ### After prediction  ##########################################
        , 'pre_process_pars' : {'y_norm_fun' :  pre_process_fun ,  ### Before training  ##########################


        ### Pipeline for data processing ##############################
        'pipe_list': [
        #### coly target prorcessing
        {'uri': 'source/prepro.py::pd_coly',                 'pars': {}, 'cols_family': 'coly',       'cols_out': 'coly',           'type': 'coly'         },


        {'uri': 'source/prepro.py::pd_colnum_bin',           'pars': {}, 'cols_family': 'colnum',     'cols_out': 'colnum_bin',     'type': ''             },
        {'uri': 'source/prepro.py::pd_colnum_binto_onehot',  'pars': {}, 'cols_family': 'colnum_bin', 'cols_out': 'colnum_onehot',  'type': ''             },

        #### catcol INTO integer,   colcat into OneHot
        {'uri': 'source/prepro.py::pd_colcat_bin',           'pars': {}, 'cols_family': 'colcat',     'cols_out': 'colcat_bin',     'type': ''             },
        # {'uri': 'source/prepro.py::pd_colcat_to_onehot',     'pars': {}, 'cols_family': 'colcat_bin', 'cols_out': 'colcat_onehot',  'type': ''             },


        ### Cross_feat = feat1 X feat2
        # {'uri': 'source/prepro.py::pd_colcross',             'pars': {}, 'cols_family': 'colcross',   'cols_out': 'colcross_pair',  'type': 'cross'},


        #### Example of Custom processor
        #{'uri':  THIS_FILEPATH + '::pd_col_myfun',   'pars': {}, 'cols_family': 'colnum',   'cols_out': 'col_myfun',  'type': '' },                


        ],
               }
        },

      'compute_pars': { 'metric_list': ['accuracy_score','average_precision_score']

                        ,'mlflow_pars' : None # {}   ### Not empty --> use mlflow
                      },

      'data_pars': { 'n_sample' : n_sample,

          'download_pars' : None,


          'cols_input_type' : cols_input_type_1,
          ### family of columns for MODEL  #########################################################
          #  "colnum", "colnum_bin", "colnum_onehot", "colnum_binmap",  #### Colnum columns
          #  "colcat", "colcat_bin", "colcat_onehot", "colcat_bin_map",  #### colcat columns
          #  'colcross_single_onehot_select', "colcross_pair_onehot",  'colcross_pair',  #### colcross columns  'coldate', 'coltext',
          'cols_model_group': [ 'colnum_bin',
                                'colcat_bin',
                                # 'coltext',
                                # 'coldate',
                                #'colcross_pair',
                               
                               ### example of custom
                               # 'col_myfun'
                              ]

          ### Filter data rows   ##################################################################
         ,'filter_pars': { 'ymax' : 2 ,'ymin' : -1 }

         }
      }

    ##### Filling Global parameters    ############################################################
    model_dict        = global_pars_update(model_dict, data_name, config_name=os_get_function_name() )
    return model_dict



def pd_col_myfun(df=None, col=None, pars={}):
    """
         Example of custom Processor
    """
    from source.util_feature import save, load
    prefix = 'col_myfun`'
    if 'path_pipeline' in pars :   #### Inference time LOAD previous pars
        prepro   = load(pars['path_pipeline'] + f"/{prefix}_model.pkl" )
        pars     = load(pars['path_pipeline'] + f"/{prefix}_pars.pkl" )
        pars     = {} if pars is None else  pars
    #### Do something #################################################################
    df_new         = df[col]  ### Do nithi
    df_new.columns = [  col + "_myfun"  for col in df.columns ]
    cols_new       = list(df_new.columns)

    prepro   = None
    pars_new = None



    ###################################################################################
    if 'path_features_store' in pars and 'path_pipeline_export' in pars:
       save(prepro,         pars['path_pipeline_export'] + f"/{prefix}_model.pkl" )
       save(cols_new,       pars['path_pipeline_export'] + f"/{prefix}.pkl" )
       save(pars_new,       pars['path_pipeline_export'] + f"/{prefix}_pars.pkl" )

    col_pars = {'prefix' : prefix , 'path' :   pars.get('path_pipeline_export', pars.get('path_pipeline', None)) }
    col_pars['cols_new'] = {
        'col_myfun' :  cols_new  ### list
    }
    return df_new, col_pars




#####################################################################################
########## Profile data #############################################################
from core_run import  data_profile
# def data_profile(path_data="", path_output="", n_sample= 5000):
"""

def data_profile(path_data="", path_output="", n_sample= 5000):
   from source.run_feature_profile import run_profile
   run_profile(path_data   = path_data,
               path_output = path_output + "/profile/",
               n_sample    = n_sample,
              )
"""



###################################################################################
########## Preprocess #############################################################
### def preprocess(config='', nsample=1000):
from core_run import preprocess

"""
def preprocess(config=None, nsample=None):
    config_name  = config  if config is not None else config_default
    mdict        = globals()[config_name]()
    m            = mdict['global_pars']
    print(mdict)

    from source import run_preprocess
    run_preprocess.run_preprocess(config_name   =  config_name,
                                  config_path   =  m['config_path'],
                                  n_sample      =  nsample if nsample is not None else m['n_sample'],

                                  ### Optonal
                                  mode          =  'run_preprocess')
"""



##################################################################################
########## Train #################################################################
from core_run import train
"""
def train(config=None, nsample=None):

    config_name  = config  if config is not None else config_default
    mdict        = globals()[config_name]()
    m            = mdict['global_pars']
    print(mdict)
    
    from source import run_train
    run_train.run_train(config_name       =  config_name,
                        config_path       =  m['config_path'],
                        n_sample          =  nsample if nsample is not None else m['n_sample']
                        )
"""



###################################################################################
######### Check data ##############################################################
def check():
   pass




####################################################################################
####### Inference ##################################################################
# predict(config='', nsample=10000)
from core_run import predict

"""
def predict(config=None, nsample=None):
    config_name  = config  if config is not None else config_default
    mdict        = globals()[config_name]()
    m            = mdict['global_pars']


    from source import run_inference
    run_inference.run_predict(config_name = config_name,
                              config_path = m['config_path'],
                              n_sample    = nsample if nsample is not None else m['n_sample'],

                              #### Optional
                              path_data   = m['path_pred_data'],
                              path_output = m['path_pred_output'],
                              model_dict  = None
                              )
"""


###########################################################################################################
###########################################################################################################
"""
python   test_automl.py  data_profile
python   test_automl.py  preprocess  --nsample 100
python   test_automl.py  train       --nsample 200
python   test_automl.py  check
python   test_automl.py  predict


"""
if __name__ == "__main__":
    d = { 'data_profile': data_profile,  'train' : train, 'predict' : predict, 'config' : config_default }
    import fire
    fire.Fire(d)
    



