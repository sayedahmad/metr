from django.urls import path, include
from .views import DataView, DataCSVView

urlpatterns = [
    path("data/", DataView.as_view(), name="data-view"),
    path("csv/", DataCSVView.as_view(), name="data-csv-view"),
]
