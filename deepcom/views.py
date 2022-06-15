from django.http import HttpResponse
from django.shortcuts import render





# Hello
def say_hello(request):
    return render(request, 'hello.html', {
        'name': 'Miguel',
    })








    


