import csv
import datetime
from io import StringIO

import pytest

from ..models import Measurement, MeasurementType


@pytest.fixture(scope="function")
def measurement_valid(device_valid):
    measurements = []

    def _create_measurement(device=None, created_date=datetime.datetime.now()):
        if callable(device):
            device = device()
        measurement = Measurement.objects.create(
            device=device,
            dimension="Energy (kWh)",
            newest_value=29690,
            due_date_value=16274,
            due_date="2019-09-30T00:00:00.000000",
            status=MeasurementType.MEASUREMENT,
            created_at=created_date,
        )
        measurements.append(measurement)
        return measurement

    yield _create_measurement
    for measurement in measurements:
        measurement.delete()


@pytest.fixture(scope="function")
def csv_sample():
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(
        [
            "Date",
            "Device ID",
            "Device Manufacturer",
            "Device Type",
            "Device Version",
            "Measurement Dimension",
            "Newest Value",
            "Due Date Value",
            "Due Date",
            "Status",
        ]
    )
    writer.writerow(
        [
            "2021-09-07 10:30:00",
            "83251076",
            "5317",
            "4",
            "0",
            "Energy (kWh)",
            29690,
            16274,
            "2019-09-30 00:00:00",
            "measurement",
        ]
    )
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()
    return csv_content
