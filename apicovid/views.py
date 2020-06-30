from django.shortcuts import render
from rest_framework import generics

from .models import *
from .serializers import *

class CidadeList(generics.ListCreateAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer

class CidadeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cidade.objects.all()
    serializer_class = CidadeSerializer

class CasoList(generics.ListCreateAPIView):
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer


class CasoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer



