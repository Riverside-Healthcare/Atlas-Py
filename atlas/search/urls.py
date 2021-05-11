from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/<str:search_string>", views.search, name="search"),
    path("template", views.template, name="template"),
]