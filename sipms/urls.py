from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sipms/", views.sipm_list, name="sipm_list"),
    path("sipms/<int:pk>/", views.sipm_detail, name="sipm_detail"),
    path("search/", views.quick_search, name="quick_search"),
]
