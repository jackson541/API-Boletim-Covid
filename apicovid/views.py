from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication

from .models import *
from .serializers import *


class CasoList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer


class CasoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Caso.objects.all()
    serializer_class = CasoSerializer



