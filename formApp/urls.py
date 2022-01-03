from django.urls import path
from . import views

app_name = "problemapp"
urlpatterns = [
    path("", views.addProblem, name="theForm")
]
