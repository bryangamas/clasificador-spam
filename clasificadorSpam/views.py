from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect #, get_object_or_404
from .logica import entrenar_clasificador 
from .logica import Clasificador, MNB_PROB
import numpy as np

def index(request):
    return render(request, 'inicio.html')

def entrenar(request):
   entrenar_clasificador()
   return redirect('formulario')
   #return HttpResponse("You're looking at question %s." % Clasificador.PI_SPAM)

def formulario(request):
    return render(request, 'formulario.html')

def results(request):
   mensaje = request.GET.get('mensaje', '')
   (spam, ham) = MNB_PROB(mensaje)
   context = {
      'spam': spam,
      'ham': ham,
      'mensaje': mensaje
   }
   return render(request, 'formulario.html', context)

def aleatorio(request):
   tipo = request.GET.get('tipo', '')
   df = Clasificador.DATASET_ORIGINAL
   df_acotado = df[df['etiqueta']==tipo]
   mensaje_elegido = df[df['mensaje']==np.random.choice(df_acotado['mensaje'])]
   context = {
      'mensaje': np.array(mensaje_elegido.mensaje)[0],
      'etiqueta': np.array(mensaje_elegido.etiqueta)[0]
   }
   return JsonResponse(context)
   
   # return HttpResponse("You're voting on question %s.")