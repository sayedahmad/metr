import io
from datetime import datetime
from types import SimpleNamespace

import pytest
from freezegun import freeze_time

from api.renderers.csv_renderer import CSVRenderer
from api.serializers import MeasurementSearializer


@pytest.mark.django_db
@freeze_time(datetime(2021, 9, 7, 10, 30))
def test_csv_renderer(measurement_valid, device_valid, csv_sample):
    measurement = measurement_valid(device_valid, created_date=datetime.now())
    renderer = CSVRenderer()
    view = SimpleNamespace(
        request={},
        response=SimpleNamespace(status_code=None, headers={}),
        action="get",
        format="csv",
    )
    renderer_context = {
        "view": view,
        "request": SimpleNamespace(get_full_path=lambda: "http//:example.com"),
    }

    assert (
        renderer.render(
            [MeasurementSearializer(measurement).data],
            renderer_context=renderer_context,
        )
        == csv_sample
    )


@pytest.mark.django_db
@freeze_time(datetime(2021, 9, 7, 10, 30))
def test_file_name():
    renderer = CSVRenderer()
    assert renderer.generate_csv_name() == "2021-09-07_report.csv"


@pytest.mark.django_db
@freeze_time(datetime(2021, 9, 7, 10, 30))
def test_generate_measurement_csv(measurement_valid, device_valid, csv_sample):
    measurement = measurement_valid(device_valid, created_date=datetime.now())
    renderer = CSVRenderer()
    assert (
        renderer.generate_measurement_csv([MeasurementSearializer(measurement).data])
        == csv_sample
    )


@pytest.mark.django_db
@freeze_time(datetime(2021, 9, 7, 10, 30))
def test_convert_to_datetime():
    renderer = CSVRenderer()
    assert renderer.convert_to_datetime("2021-09-07T10:30:0.000000Z") == datetime.now()
    assert renderer.convert_to_datetime("2021-09-07 10:30:00") == datetime.now()
    assert renderer.convert_to_datetime("2021-09-07 10:30:0") == datetime.now()
    assert renderer.convert_to_datetime("2021-09-07T10:30:00Z") == datetime.now()
