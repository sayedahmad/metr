import csv
import datetime
from io import StringIO

from rest_framework.renderers import BaseRenderer

from ..models import MeasurementType


class CSVRenderer(BaseRenderer):
    """
    CSV renderer for generating CSV content from data.

    Renders data as CSV format with specified headers and measurements.
    """

    media_type = "text/csv"
    format = "csv"
    charset = "utf-8"
    DATE_FORMATS = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
    ]

    def render(self, data, media_type=None, renderer_context=None):
        view = renderer_context["view"]
        view.response.headers[
            "Content-Disposition"
        ] = f"attachment; filename={self.generate_csv_name()}"
        if not data or not isinstance(data, list):
            return ""  # Return empty string if data is None or not a list

        return self.generate_measurement_csv(data)

    def generate_measurement_csv(self, data):
        """
        Generates the CSV content from the measurement data.

        Args:
            data (list): List of measurements data.

        Returns:
            str: CSV content as a string.
        """
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

        for measurement in data:
            measurement_date = self.convert_to_datetime(measurement["created_at"])
            measurement_due_date = (
                self.convert_to_datetime(measurement["due_date"])
                if measurement["due_date"]
                else None
            )
            status_text = MeasurementType(measurement["status"]).name.lower()
            writer.writerow(
                [
                    measurement_date.strftime(self.DATE_FORMATS[1])
                    if measurement_date
                    else None,
                    measurement["device"]["device_id"],
                    measurement["device"]["manufacturer"],
                    measurement["device"]["device_type"],
                    measurement["device"]["version"],
                    measurement["dimension"],
                    measurement["newest_value"],
                    measurement["due_date_value"],
                    measurement_due_date.strftime(self.DATE_FORMATS[1])
                    if measurement_due_date
                    else None,
                    status_text,
                ]
            )
        csv_content = csv_buffer.getvalue()
        csv_buffer.close()
        return csv_content

    def generate_csv_name(self):
        """
        Generates the name for the CSV file.

        Returns:
            str: Name of the CSV file.
        """
        return f"{datetime.datetime.now().date()}_report.csv"

    def convert_to_datetime(self, date_string):
        """
        Converts the given date string to a datetime object.

        Args:
            date_string (str): Date string to be converted.

        Returns:
            datetime.datetime: Converted datetime object.

        Raises:
            ValueError: If the date format is invalid.
        """
        for date_formate in self.DATE_FORMATS:
            try:
                return datetime.datetime.strptime(date_string, date_formate)
            except ValueError:
                continue

        raise ValueError("Invalid date format")
