from django.shortcuts import render
from rest_framework import generics

from .models import *
from .serializers import *


class CasoList(generics.ListCreateAPIView):
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer


class CasoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer



