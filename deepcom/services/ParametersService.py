from typing import Dict
from deepcom.apps import DeepcomConfig
from deepcom.models import ProcessingParametersModel

from django.forms.models import model_to_dict


class ParametersService:

    def __init__():
        pass

    def getDefaultParameters():
        return DeepcomConfig.default_processing_parameters

    def validateParameters(parameters):
        # TODO
        return True

    def updateParameters(video_path: str, parameters: Dict):
        if not ParametersService.validateParameters(parameters):
            raise Exception("Invalid processing parameters")

        parameters = ParametersService.fillParameters(parameters)
        preprocess = parameters.get("preprocess")
        process = parameters.get("process")

        ProcessingParametersModel.objects.filter(video_linked=video_path).update(
            preprocess=preprocess,
            process=process
        )

    def saveParameters(video_path: str, parameters: Dict):
        defaultParameters = ParametersService.getDefaultParameters()
        defaultParameters.update(parameters)
        parameters = defaultParameters

        if not ParametersService.validateParameters(parameters):
            raise Exception("Invalid processing parameters")

        parameters = ParametersService.fillParameters(parameters)
        preprocess = parameters.get("preprocess")
        process = parameters.get("process")

        model = ProcessingParametersModel(
            preprocess=preprocess,
            process=process,
            video_linked=video_path)
        model.save()

    def parametersExistsInDB(video_path: str):
        documents = ProcessingParametersModel.objects.filter(
            video_linked=video_path)
        return len(documents) > 0

    def getParametersInDB(video_path: str):
        return ProcessingParametersModel.objects.get(video_linked=video_path)

    def getParametersForVideo(video_path: str):

        if (ParametersService.parametersExistsInDB(video_path)):
            parameters = ParametersService.getParametersInDB(video_path)
            parameters = model_to_dict(
                parameters, fields=[field.name for field in parameters._meta.fields])
        else:
            parameters = ParametersService.getDefaultParameters()

        return parameters

    def fillParameters(partial_parameters):
        if partial_parameters is None:
            return ParametersService.getDefaultParameters()

        # Preprocess
        preprocess = partial_parameters.get("preprocess")
        if preprocess is None:                      
            preprocess = DeepcomConfig.default_preprocess_parameters
        
        # Tophat
        if preprocess.get("top_hat") is None:
            preprocess["top_hat"] = DeepcomConfig.default_top_hat_parameters



        # Process 
        process = partial_parameters.get("process")
        if process is None:           
            process = DeepcomConfig.default_process_parameters

        # Threshold
        if process.get("threshold") is None:
            process['threshold'] = DeepcomConfig.default_threshold_parameters        



        return {
          "preprocess": preprocess,
          "process": process,
        }


    def formatParameters(params):
      """
        Formats parameters so they can be accepted by deepviewcore
      """
      if not ParametersService.validateParameters(params):
          raise Exception("Invalid parameters")

      preprocess = params["preprocess"]          
      width = preprocess["top_hat"]["kernelWidth"]          
      height = preprocess["top_hat"]["kernelHeight"]          

      preprocess["top_hat"] = {
        "filterSize": (width, height)
      }
      
      params["preprocess"] = preprocess

      return params
