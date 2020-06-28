from django.urls import path
from . import views

urlpatterns = [
    path('casos/', views.CasoList.as_view(), name='list_create_caso'),
    path('casos/<int:pk>/', views.CasoDetail.as_view(), name='read_update_delete_caso'),
]