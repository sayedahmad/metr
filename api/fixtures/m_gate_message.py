import pytest


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
