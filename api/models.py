from django.db import models
from django.utils import timezone

# Create your models here.

# class DeviceManufacturer(models.Model):
#     name = models.CharField(max_length=100)


class MeasurementType(models.IntegerChoices):
    MEASUREMENT = 1
    ERROR = 2


class Device(models.Model):
    device_id = models.BigIntegerField(blank=True, null=True)
    device_type = models.IntegerField()
    status = models.IntegerField()
    version = models.IntegerField()
    access_number = models.IntegerField()
    manufacturer = models.IntegerField()


class Measurement(models.Model):
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="device_measurements"
    )
    dimension = models.CharField(max_length=100)
    newest_value = models.IntegerField()
    due_date_value = models.IntegerField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=MeasurementType.choices)
    created_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)
