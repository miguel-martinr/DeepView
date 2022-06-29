from django.http import HttpRequest


def get_contours(request: HttpRequest):
  contours = []

  response = {
    "sucess": True,
    "contours": contours
  }


  return response