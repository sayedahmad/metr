from rest_framework import serializers

from .models import Device, Measurement


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "device_id",
            "device_type",
            "status",
            "version",
            "access_number",
            "manufacturer",
        ]


class MeasurementSearializer(serializers.ModelSerializer):
    device = DeviceSerializer()

    class Meta:
        model = Measurement
        fields = [
            "device",
            "dimension",
            "newest_value",
            "due_date_value",
            "due_date",
            "status",
            "created_at",
        ]

    def create(self, validated_data):
        device_data = validated_data.pop("device")
        device, _ = Device.objects.get_or_create(
            device_id=device_data.get("device_id"), defaults=device_data
        )
        measurement = Measurement.objects.create(device=device, **validated_data)
        return measurement
