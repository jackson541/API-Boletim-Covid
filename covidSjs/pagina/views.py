from django.shortcuts import render
from django.views import View

from .models import casos as Casos

# Create your views here.

class index(View):
    def get(self, request):
        casos = Casos.objects.latest('data')
        return render(request, 'index.html', {'casos': casos})
