"""

https://docs.bentoml.org/en/latest/quickstart.html




https://github.com/jjmachan/resnet-bentoml

Project Stucture
train.py - The python script to train the model and save the trained model. The saved models will be stored in saved_models folder. Typically trains for 2mins on GPU and 30mins on my CPU. It automatically saves the checkpoints if you exit from training and you can resume training from the same checkpoint by specifying the checkpoint using -c (--checkpoint) argument.

get_data.sh - Script to download the training data from the PyTorch servers and extract it.

classificationService.py - Defines the Bento service that has to be run for serving the model. This file specifies handlers which are used to specify how the incoming data is to be handled, artifacts or containers that store different models and Services which defines the API endpoints for the various models you want to serve.

saveToBento.py - The script that creates, packs and saves the Bento Service. The script packs the models weights, model definition and the information on how to serve along with the dependencies and saves it into the disk. Each saved Bento Service is stand alone and containes everything needed to serve it. The saved services are also versioned for tracking the different models that you tested.



Usage
First of all, download the dataset by running the script sh get_data.sh.

Now, install all the dependencies by running pip install -r requirements.txt. With that all the dependencies like pytorch, torchvision, imageio and bentoml will be installed.

You can train the model using python train.py which will run by default for 25 epochs and save the model weights on the saved_models dir.

With the model all trained you can now add it to Bento using python saveToBento.py {pathtosaved_model} and now its saved and ready to serve. It will print out the path of the location where it is saved so note that down.

Now just run bentoml serve {pathtobento_file} and vola! Your service is running. Head over to localhost:5000 to test it out.


https://docs.bentoml.org/en/latest/frameworks.html


python source/run_bentoml.py




"""
import bentoml
import pandas as pd, json, sys, os
from bentoml import BentoService, api, artifacts, env
from bentoml.adapters import DataframeInput, JsonInput
from bentoml.frameworks.pytorch import PytorchModelArtifact
from bentoml.frameworks.lightgbm import LightGBMModelArtifact
from bentoml.frameworks.sklearn import SklearnModelArtifact
from bentoml.handlers import ImageHandler


#### Add path for python import
sys.path.append( os.path.dirname(os.path.abspath(__file__)) + "/")
# import util_feature


#### Root folder analysis
root = os.path.abspath(os.getcwd()).replace("\\", "/") + "/"
print(root)

from run_train import load_function_uri, model_dict_load




########  Service ##################################################################
from run_train import map_model, model_dict_load

def log(*s):
    print(s)


def load_model_dsa(dir_model='', model_uri="source/models/model_sklearn.py::LightGBM"):
    """
       Return the model loaded from disk
    :param dir_model:
    :param model_uri:
    :return:
    """
    sys.path.append( root)    #### Needed due to import source error

    model_dict  = None
    model_dict  = model_dict_load(model_dict, config_path= model_uri.split("::")[0],
                                  config_name= model_uri.split("::")[1], verbose=True)

    log(model_dict)

    model_pars, compute_pars = model_dict['model_pars'], model_dict['compute_pars']
    data_pars                = model_dict['data_pars']
    model_name, model_path   = model_pars['model_class'], model_dict['global_pars']['path_train_model']
    metric_list              = compute_pars['metric_list']

    modelx = map_model(model_name)
    modelx.reset()
    modelx.init(model_pars, compute_pars=compute_pars)
    modelx.load_model(dir_model)
    log(modelx)

    return modelx





path_model       = ""
service_model_id = "myid1"
model_frameowrk  = 'sklearn'
dir_bento        = root + "data/output/bento/"
dir_model        = root + "/data/output/titanic/titanic_lightgbm/model/"
model_uri        = root + "/titanic_classifier.py::titanic_lightgbm"



import os
from bentoml.exceptions import MissingDependencyException
from bentoml.service.artifacts import BentoServiceArtifact



class dsaModelArtifact(BentoServiceArtifact):
    """
    Abstraction for saving/loading scikit learn models using sklearn.externals.joblib

    Args:
        name (str): Name for the artifact
        pickle_extension (str): The extension format for pickled file

    Raises:
        MissingDependencyException: sklean package is required for SklearnModelArtifact

    Example usage:

    >>> from sklearn import svm
    >>>
    >>> model_to_save = svm.SVC(gamma='scale')
    >>> # ... training model, etc.
    >>>
    >>> import bentoml
    >>> from bentoml.frameworks.sklearn import SklearnModelArtifact
    >>> from bentoml.adapters import DataframeInput
    >>>
    >>> @bentoml.env(infer_pip_packages=True)
    >>> @bentoml.artifacts([SklearnModelArtifact('model')])
    >>> class SklearnModelService(bentoml.BentoService):
    >>>
    >>>     @bentoml.api(input=DataframeInput(), batch=True)
    >>>     def predict(self, df):
    >>>         result = self.artifacts.model.predict(df)
    >>>         return result
    >>>
    >>> svc = SklearnModelService()
    >>>
    >>> # Pack directly with sklearn model object
    >>> svc.pack('model', model_to_save)
    """

    def __init__(self, name, pickle_extension=".pkl"):
        super(SklearnModelArtifact, self).__init__(name)

        self._pickle_extension = pickle_extension
        self._model = None

    def _model_file_path(self, base_path):
        return os.path.join(base_path, self.name + self._pickle_extension)

    def pack(self, sklearn_model, metadata=None):  # pylint:disable=arguments-differ
        self._model = sklearn_model
        return self

    def load(self, path):
        """
         
        """
        model_file_path = self._model_file_path(path)
        sklearn_model   = load_model_dsa(model_file_path, model_uri )
        return self.pack(sklearn_model)

    def get(self):
        return self._model

    def save(self, dst, stats=None):        
        self._model.save(model_path, stats)        


    def set_dependencies(self, env):
        env.add_pip_packages(['scikit-learn'])



if model_frameowrk == 'sklearn' :
    #A minimum prediction service exposing a Scikit-learn model
    @env(infer_pip_packages=False)
    @artifacts([SklearnModelArtifact(service_model_id)])
    class mybentoClass(BentoService):
        @api(input=DataframeInput(), batch=True)
        def predict(self, df: pd.DataFrame):
            #An inference API named `predict` with Dataframe input adapter, which codifies
            #how HTTP requests or CSV files are converted to a pandas Dataframe object as the
            #inference API function input

            return self.artifacts.model.predict(df)


    # Create  service instance
    service = mybentoClass()

    # Pack the newly trained model artifact
    mymodel = load_model_dsa(dir_model, model_uri )
    service.pack(service_model_id, mymodel.model )

     #  $BENTOML_HOME  ~/bentoml/repository/{service_name}/{service_version}
    saved_path = service.save()

    # Save the prediction service to disk for model serving
    #os.makedirs(dir_bento, exist_ok=True)
    #saved_path = service.save_to_dir(dir_bento + "/"  )

    """
       https://github.com/bentoml/BentoML/issues/1433
       cannot pickle module,
       cannot pickle DSA module file !!!!!!!!!!!!!!!!!!!!!!!!!!
       
       Need a Custom wrapper
       
       Or need a flask API
       
    
    
    """

    #### Serve the model on command line
    #### bentoml serve IrisClassifier:latest


    """
    BentoML stores all packaged model files under the ~/bentoml/repository/{service_name}/{service_version} 
    directory by default. The BentoML packaged model format contains all the code, files, and configs required to run and deploy the model.
    
    
    #### Serve the model
    bentoml serve IrisClassifier:latest
    
    
    curl -i --header "Content-Type: application/json" --request POST \
      --data '[[5.1, 3.5, 1.4, 0.2]]'   http://localhost:5000/predict
      
    import requests
    response = requests.post("http://127.0.0.1:5000/predict", json=[[5.1, 3.5, 1.4, 0.2]])
    print(response.text)
    
    
    """


#############################################################################################################
#############################################################################################################
if model_frameowrk == 'sklearn2' :
    class FraudDetectionAndIdentityService(BentoService):
        @api(input=JsonInput(), batch=True)
        def fraud_detect(self, json_list):
            # user-defined callback function that process inference requests
            pass

        @api(input=DataframeInput(input_json_orient='records'), batch=True)
        def identity(self, df):
            # user-defined callback function that process inference requests
            pass



if model_frameowrk == 'lightgbm' :
    @bentoml.env(pip_dependencies=['torch', 'torchvision'])
    @bentoml.artifacts([LightGBMModelArtifact('model')])
    @bentoml.env(infer_pip_packages=True)
    class LgbModelService(bentoml.BentoService):
        @bentoml.api(input=DataframeInput(), batch=True)
        def predict(self, df):
            return self.artifacts.model.predict(df)

    svc = LgbModelService()
    svc.pack('model', model)




if model_frameowrk == 'pytorch' :
    from PIL import Image
    import torch
    from torchvision import transforms

    classes = ['ant', 'bee']
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    cpu = torch.device('cpu')


    @bentoml.env(pip_dependencies=['torch', 'torchvision'])
    @bentoml.artifacts([PytorchModelArtifact('mymodel_id')])
    class AntOrBeeClassifier(bentoml.BentoService):

        @bentoml.api(ImageHandler)
        def predict(self, img):
            img = Image.fromarray(img)
            img = transform(img)

            self.artifacts.model.eval()
            outputs = self.artifacts.model(img.unsqueeze(0))
            _, idxs = outputs.topk(1)
            idx = idxs.squeeze().item()
            return classes[idx]




################# Save to Bento Space ###################################
def bento_save():
    import argparse

    import torch.nn as nn
    from torchvision import models

    import utils
    #from classificationService import AntOrBeeClassifier

    def saveToBento(checkpoint):
        model_state_dict, _, _, _, _ = utils.load_model(checkpoint)

        # Define the model
        model_ft =  models.resnet18(pretrained=False)
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs, 2)

        # Load saved model
        model_ft.load_state_dict(model_state_dict)

        # Add model to Bento ML
        bento_svc = AntOrBeeClassifier()
        bento_svc.pack('mymodel_id', model_ft)

        # Save Bento Service
        saved_path = bento_svc.save()
        print('Bento Service Saved in ', saved_path)

    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('checkpoint', help='Checkpoint to load the model')
        args = parser.parse_args()

        saveToBento(args.checkpoint)









"""





# iris_classifier.py
import pandas as pd

from bentoml import env, artifacts, api, BentoService
from bentoml.adapters import DataframeInput
from bentoml.frameworks.sklearn import SklearnModelArtifact

@env(infer_pip_packages=True)
@artifacts([SklearnModelArtifact('model')])
class IrisClassifier(BentoService):

    #A minimum prediction service exposing a Scikit-learn model


    @api(input=DataframeInput(), batch=True)
    def predict(self, df: pd.DataFrame):
 
        An inference API named `predict` with Dataframe input adapter, which codifies
        how HTTP requests or CSV files are converted to a pandas Dataframe object as the
        inference API function input
 
        return self.artifacts.model.predict(df)


    else:
        model_state_dict, criterion, optimizer_ft, exp_lr_scheduler, epoch = utils.load_model(checkpoint)
        model_ft.load_state_dict(model_state_dict)
        model_ft = model_ft.to(device)
    try:
        model_ft = train_model(dataloaders, dataset_sizes, model_ft, criterion,
            optimizer_ft, exp_lr_scheduler, start_epoch=epoch, end_epoch=25)

        saveToBento = input("Save model to Bento ML (yes/no): ")

        if saveToBento.lower() == "yes":
            # Add it to BentoML
            bento_svc = AntOrBeeClassifier()
            bento_svc.pack('model', model_ft)

            # Save your Bento Service
            saved_path = bento_svc.save()
            print('Bento Service saved in ', saved_path)
    except KeyboardInterrupt:
        pass
    finally:
"""


