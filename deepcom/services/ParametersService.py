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

    def saveParameters(video_path: str, parameters: Dict):
        defaultParameters = ParametersService.getDefaultParameters()
        defaultParameters.update(parameters)
        parameters = defaultParameters

        if not ParametersService.validateParameters(parameters):
            raise Exception("Invalid processing parameters")

        preprocess = parameters.get("preprocess")

        model = ProcessingParametersModel(
            preprocess=preprocess, video_linked=video_path)
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
            parameters = model_to_dict(parameters, fields=[field.name for field in parameters._meta.fields])
        else:
            parameters = ParametersService.getDefaultParameters()
        
        return parameters
