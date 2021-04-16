# pylint: disable=C0321,C0103,E1221,C0301,E1305,E1121,C0302,C0330
# -*- coding: utf-8 -*-
"""

ipython toutlier.py  train_test




"""
import warnings, copy, os, sys, gc, time, glob
warnings.filterwarnings('ignore')


####################################################################################
###### Path ########################################################################
root_repo      =  os.path.abspath(os.getcwd()).replace("\\", "/")      ; print(root_repo)
THIS_FILEPATH  =  os.path.abspath(__file__)
sys.path.append(root_repo + "/ml_dsa/")
from source.util_feature import os_get_function_name


def global_pars_update(model_dict,  data_name, config_name,
                       dir_data=None, dir_input_tr=None, dir_input_te=None):
    print("config_name", config_name)
    root_repo2    =  os.path.abspath(os.getcwd()).replace("\\", "/")  ; print(root_repo)


    #### Actual 
    dir_data     = dir_data3   if dir_data is  None else dir_data
    dir_input_tr = dir_input3_tr  if dir_input_tr is  None else dir_input_tr 
    dir_input_te = dir_input3_te  if dir_input_te is  None else dir_input_te 
    print("dir_data_input", dir_input_tr)




    ########################################################################
    m                      = {}
    m['config_path']       = THIS_FILEPATH
    m['config_name']       = config_name

    #### peoprocess input path
    m['path_data_preprocess'] = dir_input_tr 


    #### train input path
    m['path_data_train']      = dir_input_tr 
    m['path_data_test']       = dir_input_te 
    #m['path_data_val']       = dir_data + f'/input/{data_name}/test/'


    #### train output path
    m['path_train_output']    = dir_data + f'/output/{data_name}/{config_name}/'
    m['path_train_model']     = dir_data + f'/output/{data_name}/{config_name}/model/'
    m['path_features_store']  = dir_data + f'/output/{data_name}/{config_name}/features_store/'
    m['path_pipeline']        = dir_data + f'/output/{data_name}/{config_name}/pipeline/'


    #### predict  input path
    m['path_pred_data']       = dir_input_te 
    m['path_pred_pipeline']   = dir_data + f'/output/{data_name}/{config_name}/pipeline/'
    m['path_pred_model']      = dir_data + f'/output/{data_name}/{config_name}/model/'

    #### predict  output path
    m['path_pred_output']     = dir_data + f'/output/{data_name}/pred_{config_name}/'

    #####  Generic
    m['n_sample']             = model_dict['data_pars'].get('n_sample', 5000)

    model_dict[ 'global_pars'] = m
    return model_dict


####################################################################################
config_default  = 'config1'   ### name of function which contains data configuration



####################################################################################
##### Params########################################################################
colnum  = ['ok']

cols_input_type_1 = {
     "coly"   :   "y"     ### isfraud 1/0
    ,"colid"  :   "ip"
    ,"colcat" :   [  ]

    ,"colnum" :   colnum[:5]


    ,"coldate"  : []
    ,"colcross" : []
}



#### SHOULD BE OUTSIDE OF the config_template DUE TO Pickle iSSUE
def post_process_fun(y):   ### After prediction is done
    return  int(y)

def pre_process_fun(y):    ### Before the prediction is done
    return  int(y)


#####################################################################################################
#####################################################################################################
def  config_template(path_model_out="") :
    """
    """
    config_name  = os_get_function_name()
    data_name    = "/hdfs/"   ### in data/input/
    model_class  = 'IForest'  ### ACTUAL Class name for model_sklearn.py
    n_sample     = 10000

    model_dict = {
    'model_pars': {
         ### API model   #######################################
         'model_class': model_class
        ,'model_pars' : { 'n_estimators': 10,}
        ,'model_extra': {}
        ,'post_process_fun' : post_process_fun                     ### After prediction  
        ,'pre_process_pars' : {'y_norm_fun' :  pre_process_fun ,  ### Before training  

          "mode" : "run_preprocess",  # "load_preprocess"

          ### Pipeline for data processing ##############################
          'pipe_list': [
              {'uri': 'source/prepro.py::pd_coly',                 'pars': {}, 'cols_family': 'coly',       'cols_out': 'coly',           'type': 'coly'         },
              {'uri': 'source/prepro.py::pd_colnum_normalize',           
                 'pars': { 'pipe_list': [ 
                                       {'name': 'quantile_cutoff'} ,
                                       {'name': 'fillna', 'na_val' : 0.0 }, 
                                       ]}, 
                 'cols_family': 'colnum',     'cols_out': 'colnum_norm',     'type': ''             },

              # {'uri': 'source/prepro.py::pd_colnum_bin',           'pars': {}, 'cols_family': 'colnum',     'cols_out': 'colnum_bin',     'type': ''             },
              # {'uri': 'source/prepro.py::pd_colnum_binto_onehot',  'pars': {}, 'cols_family': 'colnum_bin', 'cols_out': 'colnum_onehot',  'type': ''             },
              {'uri': 'source/prepro.py::pd_colcat_bin',           'pars': {}, 'cols_family': 'colcat',     'cols_out': 'colcat_bin',     'type': ''             },
              # {'uri': 'source/prepro.py::pd_colcat_to_onehot',     'pars': {}, 'cols_family': 'colcat_bin', 'cols_out': 'colcat_onehot',  'type': ''             },
              # {'uri': 'source/prepro.py::pd_colcross',             'pars': {}, 'cols_family': 'colcross',   'cols_out': 'colcross_pair',  'type': 'cross'},
          ],
        }
    },
    'compute_pars': { 'metric_list': ['accuracy_score','average_precision_score',
                                      'f1_score',  'balanced_accuracy_score'   ],
                      'probability': True,  ## Return proba
                      'compute_pars' : {},
                      'compute_extra': {}
    },      
    'data_pars': { 'n_sample' : n_sample,
        'cols_input_type' : cols_input_type_1,
        'cols_model_group': [ 'colnum_norm',
                              'colcat_bin',
                              # 'colcross_pair',
                            ]

        ### Filter data rows   ##################################################################
       ,'filter_pars': { 'ymax' : 2 ,'ymin' : -1 }
       }
    }

    ##### Filling Global parameters    ############################################################
    model_dict        = global_pars_update(model_dict, data_name, config_name )
    return model_dict


###################################################################################################
###################################################################################################
from source import run_train
from util_feature import load_function_uri
def  train_test(nsample=100) :
    """ 
      python example/fraud_model.py  train_test

    """
    nsample = 3*10**3
    
    model_dict_ref = config_template()
    ll = [
        #( 'VAE' , { 'contamination' :0.01, 'epochs' : 1, 'latent_dim': 5,
        #      # 'encoder_neurons' : [20, 10], 'decoder_neurons' : [10, 20]
        #      'encoder_neurons' : [8, 6], 'decoder_neurons' : [6, 8]
        #
        # }),

        # ( 'IForest' , { 'contamination' :0.01, 'n_estimators': 30, 'n_jobs': 4 } ),

        
        ( 'HBOS'   , { 'contamination' : 0.01, 'n_bins' : 10, 'alpha' : 0.1, 'tol' : 0.5  } ),   

        #( 'COPOD'   , { 'contamination' :0.01  } ),    ### Copula Based 2020

        #( 'CBLOF'   , { 'n_clusters': 10   } ),  

        #( 'LGBMClassifier' , { 'n_estimators': 10,} ),

        
        #( 'ABOD'   , { 'contamination' :0.01,  'n_neighbors' :5, 'method' : 'fast'  } ),   ### Very Slow      
        
        #( 'SOS'     , { 'contamination' :0.01, 'perplexity' :4.5, 'metric' : 'euclidean', n_jobs= 4 } ),  ### VERY SLOW
        
        ### VAE Serialization Error
        # ( 'SO_GAAL' , { 'contamination' :0.01, 'stop_epochs' : 1, 'lr_d' :0.01, 'lr_g' : 0.0001, 'decay' :1e-06, 'momentum' : 0.9,  } ),   ## VAE keras
        
    ]

    feat_name = "train_smalll"
    data_name = "/data1/"
    
    
    #dir_data3     = "C:/D/gitdev/fraud/mldev/ztmp/rpp_fraud/"    
    dir_data3     = root_repo  + "/ztmp/"    ###  a/adigcb301/ipsvols05/scoupon/test_code/fraud/mldev/ztmp    
    dir_input3_tr = dir_data3 + f"/input/features/202011/{feat_name}/"  
    dir_input3_te = dir_data3 + f"/input/features/202011/{feat_name}/"  

    for m, p in ll :
        model_dict = copy.deepcopy(model_dict_ref )  ### Full Copy
        model_dict['model_pars']['model_class'] = "model_outlier:" + m
        model_dict['model_pars']['model_pars']  = p

        
        config_name = "config_" + m
        model_dict  = global_pars_update(model_dict, data_name, config_name,
                                 dir_data    = dir_data3,
                                 dir_input_tr= dir_input3_tr,
                                 dir_input_te= dir_input3_te
                              )

        run_train.run_train(config_name       =  None, #'config1',  
                            config_path       =  None, # THIS_FILEPATH,
                            n_sample          =  nsample,
                            model_dict        =  model_dict
                            # use_mlmflow     =  False
                            )
        # sys.exit()

        
  

########## Preprocess #############################################################
### def preprocess(config='', nsample=1000):
from core_run import preprocess


########## Train #################################################################
## def train(config='titanic_classifier.py::titanic_lightgbm'):
from core_run import train



####### Inference ##################################################################
# def  predict(config='', nsample=10000)
from core_run import predict


####################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()
    










