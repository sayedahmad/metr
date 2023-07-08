import pytest

from ..models import Device


@pytest.fixture(scope="function")
def device_valid():
    devices = []

    def _make_protocol(device_id=83251076):
        device = Device.objects.create(
            device_id=device_id,
            device_type=4,
            status=0,
            version=0,
            access_number=156,
            manufacturer=5317,
        )
        devices.append(device)
        return device

    yield _make_protocol
    for device in devices:
        device.delete()
