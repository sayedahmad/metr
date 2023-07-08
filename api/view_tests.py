from datetime import datetime

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status


@pytest.mark.django_db
def test_create_measurement(unauthenticated_client, measurement_post_data):
    url = reverse("data-view")
    response = unauthenticated_client.post(url, measurement_post_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


def test_create_measurement_invalid_data(unauthenticated_client):
    url = reverse("data-view")
    data = {}  # Invalid data without required fields

    response = unauthenticated_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_latest_measurements_csv(
    unauthenticated_client, measurement_valid, device_valid
):
    past_month = measurement_valid(
        device_valid(device_id=12345),
        created_date=timezone.datetime(2021, 8, 7, 10, 30),
    )
    current_month = measurement_valid(device_valid, created_date=datetime.now())
    response = unauthenticated_client.get(reverse("data-csv-view"))
    assert response.status_code == status.HTTP_200_OK
    assert response.content != b""  # CSV content should not be empty
    assert response["Content-Type"] == "text/csv; charset=utf-8"
    assert response["Content-Disposition"].startswith("attachment; filename=")
    assert str(past_month.device.device_id) not in response.content.decode("utf8")
    assert str(current_month.device.device_id) in response.content.decode("utf8")
