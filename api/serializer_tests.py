import pytest
from django.core.exceptions import ValidationError
from freezegun import freeze_time
from datetime import datetime
from .serializers import DeviceSerializer, MeasurementSearializer
from .models import Device, Measurement

@freeze_time(datetime(2021, 9, 7, 10, 30))
def test_measurement_serializer_create(measurement_valid, device_valid):
      
        measurement = measurement_valid(device_valid)
        data = MeasurementSearializer(measurement).data
        serializer = MeasurementSearializer(data=data)
        assert serializer.is_valid()

        measurement = serializer.save()
        assert measurement.device.device_id == 83251076
        assert measurement.dimension == "Energy (kWh)"
        assert measurement.newest_value == 29690
        assert measurement.due_date_value == 16274
        assert str(measurement.due_date) == "2019-09-30 00:00:00+00:00"
        assert str(measurement.created_at) == "2021-09-07 10:30:00+00:00"

def test_measurement_serializer_create_invalid_data():
        measurement_data = {
            "device": {},  # Invalid data: missing required fields
            "dimension": "",
            "newest_value": None,
            "due_date_value": None,
            "due_date": None,
            "created_at": None,
        }

        serializer = MeasurementSearializer(data=measurement_data)
        is_valid = serializer.is_valid()

        assert not is_valid
        assert "device" in serializer.errors
        assert "dimension" in serializer.errors
        assert "newest_value" in serializer.errors
        assert "due_date_value" in serializer.errors
        assert "due_date" in serializer.errors
        assert "created_at" in serializer.errors