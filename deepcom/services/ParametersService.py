from typing import Dict
from deepcom.apps import DeepcomConfig
from deepcom.models import ProcessingParametersModel


class ParametersService:

    def __init__():
        pass

    def getDefaultParameters():
        return DeepcomConfig.default_processing_parameters


    def validateParameters(parameters):
      # TODO
      return True

    def saveParameters(video_path: str, parameters: Dict):
        parameters = {}
        parameters.update(ParametersService.getDefaultParameters())
        if not ParametersService.validateParameters(parameters):
          raise Exception("Invalid processing parameters")
        
        preprocess = parameters.get("preprocess")

        model = ProcessingParametersModel(preprocess=preprocess, video_linked=video_path)
        model.save()
        

