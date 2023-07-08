from datetime import datetime

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Measurement, MeasurementType
from .renderers.csv_renderer import CSVRenderer
from .serializers import MeasurementSearializer

# Create your views here.


class DataView(generics.CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSearializer

    def post(self, request):
        if not request.data:
            return Response({"Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            measurement_data = request.data.get("data")
            device_data = request.data.get("device")
            device = {
                "device_id": device_data.get("identnr"),
                "device_type": device_data.get("type"),
                "status": device_data.get("status"),
                "version": device_data.get("version"),
                "access_number": device_data.get("accessnr"),
                "manufacturer": device_data.get("manufacturer"),
            }

            measurement = {
                "device": device,
                "dimension": measurement_data[1].get("dimension"),
                "newest_value": measurement_data[1].get("value"),
                "due_date_value": measurement_data[3].get("value"),
            }
            if "Error flags" in measurement_data[2].get("dimension"):
                measurement["status"] = MeasurementType.ERROR
            else:
                measurement["due_date"] = measurement_data[2].get("value")
                measurement["status"] = MeasurementType.MEASUREMENT

            serializer = self.get_serializer(data=measurement)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(
                {"HTTP 201 Created ": "Message received successfully"},
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            return Response(
                {"HTTP 400 Bad Request ": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class DataCSVView(generics.ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSearializer
    renderer_classes = [CSVRenderer]

    def get_queryset(self):
        current_month = datetime.now().month

        latest_measurements = (
            Measurement.objects.filter(created_at__month=current_month)
            .order_by("device", "-created_at")
            .distinct("device")
        )

        return latest_measurements
