from rest_framework.renderers import BaseRenderer
import csv
import datetime
from io import StringIO


class CSVRenderer(BaseRenderer):
    media_type = "text/csv"
    format = "csv"
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):
        view = renderer_context["view"]
        view.response.headers[
            "Content-Disposition"
        ] = f"attachment; filename={self.generate_csv_name()}"
        if not data or not isinstance(data, list):
            return ""  # Return empty string if data is None or not a list

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

        for measurement in data:
            measurement_date = self.convert_to_datetime(measurement["created_at"])
            measurement_due_date = self.convert_to_datetime(measurement["due_date"])
            writer.writerow(
                [
                    measurement_date.strftime("%Y-%m-%d %H:%M:%S"),
                    measurement["device"]["device_id"],
                    measurement["device"]["manufacturer"],
                    measurement["device"]["device_type"],
                    measurement["device"]["version"],
                    measurement["dimension"],
                    measurement["newest_value"],
                    measurement["due_date_value"],
                    measurement_due_date.strftime("%Y-%m-%d %H:%M:%S"),
                ]
            )

        csv_content = csv_buffer.getvalue()
        csv_buffer.close()
        return csv_content

    def generate_csv_name(self):
        return f"{datetime.datetime.now().date()}_report.csv"

    def convert_to_datetime(self, date_string):
        try:
            # Attempt to parse the date using different formats
            datetime_obj = datetime.datetime.strptime(
                date_string, "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        except ValueError:
            try:
                datetime_obj = datetime.datetime.strptime(
                    date_string, "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                try:
                    datetime_obj = datetime.datetime.strptime(
                        date_string, "%Y-%m-%dT%H:%M:%S.%f"
                    )
                except ValueError:
                    try:
                        datetime_obj = datetime.datetime.strptime(
                            date_string, "%Y-%m-%dT%H:%M:%SZ"
                        )
                    except:
                        raise ValueError("Invalid date format")

        return datetime_obj
