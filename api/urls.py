from django.urls import path

from .views import DataCSVView, DataView

urlpatterns = [
    path("data/", DataView.as_view(), name="data-view"),
    path("csv/", DataCSVView.as_view(), name="data-csv-view"),
]
