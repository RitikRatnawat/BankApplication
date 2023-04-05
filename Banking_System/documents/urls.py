from django.urls import path
from . import views

urlpatterns = [
    path("document/", views.UploadView.as_view())
]
