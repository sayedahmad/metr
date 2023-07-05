from api.renderers.csv_renderer import CSVRenderer
from types import SimpleNamespace
import io
import pytest
from api.models import Measurement
from api.serializers import MeasurementSearializer
from freezegun import freeze_time
from datetime import datetime
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_create_measurement(unauthenticated_client,measurement_post_data):
        url = reverse("data-view")
        response = unauthenticated_client.post(url, measurement_post_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED


def test_create_measurement_invalid_data(unauthenticated_client):
        url = reverse("data-view")
        data = {}  # Invalid data without required fields

        response = unauthenticated_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_get_latest_measurements_csv(unauthenticated_client,measurement_post_data ):
        response = unauthenticated_client.post(reverse("data-view"), measurement_post_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        response = unauthenticated_client.get(reverse("data-csv-view"))
        assert response.status_code == status.HTTP_200_OK
        assert response.content != b""  # CSV content should not be empty
        assert response["Content-Type"] == "text/csv; charset=utf-8"
        assert response["Content-Disposition"].startswith("attachment; filename=")