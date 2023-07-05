import pytest
import datetime
from io import StringIO
import csv


from ..models import Measurement, MeasurementType


@pytest.fixture(scope="function")
def measurement_valid(device_valid):
    measurements = []

    def _make_protocol(device_valid):
        measurement = Measurement.objects.create(
            device=device_valid(),
            dimension="Energy (kWh)",
            newest_value=29690,
            due_date_value=16274,
            due_date="2019-09-30T00:00:00.000000",
            status = MeasurementType.MEASUREMENT,
            created_at=datetime.datetime.now(),
        )
        measurements.append(measurement)
        return measurement

    yield _make_protocol
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
        ]
    )
    csv_content = csv_buffer.getvalue()
    csv_buffer.close()
    return csv_content

@pytest.fixture(scope="function")
def measurement_post_data():
    return {
            "device": {
                "identnr": 123456,
                "type": 1,
                "status": 0,
                "version": 1,
                "accessnr": 99,
                "manufacturer": 9876,
            },
            "data": [
                {
                    "value": "2020-06-26T06:49:00.000000",
                    "tariff": 0,
                    "subunit": 0,
                    "dimension": "Time Point (time & date)",
                    "storagenr": 0,
                },
                {
                    "value": 29690,
                    "tariff": 0,
                    "subunit": 0,
                    "dimension": "Energy (kWh)",
                    "storagenr": 0,
                },
                {
                    "value": "2019-09-30T00:00:00.000000",
                    "tariff": 0,
                    "subunit": 0,
                    "dimension": "Time Point (date)",
                    "storagenr": 1,
                },
                {
                    "value": 16274,
                    "tariff": 0,
                    "subunit": 0,
                    "dimension": "Energy (kWh)",
                    "storagenr": 1,
                },
            ],
        }