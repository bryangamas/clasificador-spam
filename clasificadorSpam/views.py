from django.http import HttpResponse
from django.shortcuts import render, redirect #, get_object_or_404
from .logica import entrenar_clasificador 
from .logica import Clasificador

def index(request):
    return render(request, 'inicio.html')

def entrenar(request):
   entrenar_clasificador()
   return redirect('formulario')
   #return HttpResponse("You're looking at question %s." % Clasificador.PI_SPAM)

def formulario(request):
    return render(request, 'formulario.html')

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)