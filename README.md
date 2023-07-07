
# Metr Data CSV Exporter

The Metr Data CSV Exporter is a Django-based application that allows you to gather OMS-Data from multiple sources and build a CSV exporter. The exporter provides two endpoints: one for receiving messages from devices through the m-gate gateway and another for clients to download a CSV file containing the latest message of the current month for each device.

## Challenge Details

The goal of this challenge is to build two endpoints using Django and Django Rest Framework. The m-gate gateway installed in the buildings sends messages from devices to the first endpoint. The gateway processes the messages and sends them to the backend. The second endpoint allows clients to download a CSV file with the latest message of the current month for each device.

## Directory Structure

The project follows the directory structure outlined below. The backend directory serves as the main project directory, containing the settings files. The api directory represents the Django application, where the primary logic of the project is implemented.

```plaintext
metr/
├── backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── test_settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── fixtures/
│   ├── renderers/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── conftest.py
│   ├── models.py
│   ├── serializers_tests.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views_tests.py
│   ├── views.py
├── .gitignore.py
├── manage.py
├── pytest.ini
└── README.md
├── requirements.txt
```
## Installation and Setup

1. Clone the repository:

   ```shell
   git clone https://github.com/sayedahmad/metr.git
   ```

2. Navigate to the project directory:

   ```shell
   cd metr
   ```

3. Create a virtual environment:

   ```shell
   python3 -m venv venv
   ```

4. Activate the virtual environment:

   - Windows:

     ```shell
     venv\Scripts\activate
     ```

   - macOS/Linux:

     ```shell
     source venv/bin/activate
     ```

5. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

6. Install PostgreSQL with the following database:
    - Ubuntu:
        ```shell
        sudo apt update
        sudo apt install postgresql
        ```
    - Create the following database and user in PostgreSQL:
        ```shell
        NAME: metr,
        USER: admin,
        PASSWORD: secret,
        ```
7. Run database migrations:

   ```shell
   python manage.py migrate
   ```

7. Start the development server:

   ```shell
   python manage.py runserver
   ```

8. Access the application at `http://localhost:8000/`.

## Endpoints

### Receive Device Messages

- **Endpoint:** `api/data/`
- **Method:** `POST`
- **Parameters:**

  - `data` (object): A single message sent by the m-gate gateway.

    Example:
    ```json
    {
      "data": [
        {
          "value": "2020-06-26T06:49:00.000000",
          "tariff": 0,
          "subunit": 0,
          "dimension": "Time Point (time & date)",
          "storagenr": 0
        },
        {
          "value": 29690,
          "tariff": 0,
          "subunit": 0,
          "dimension": "Energy (kWh)",
          "storagenr": 0
        },
        {
          "value": "2019-09-30T00:00:00.000000",
          "tariff": 0,
          "subunit": 0,
          "dimension": "Time Point (date)",
          "storagenr": 1
        },
        {
          "value": 16274,
          "tariff": 0,
          "subunit": 0,
          "dimension": "Energy (kWh)",
          "storagenr": 1
        }
      ],
      "device": {
        "type": 4,
        "status": 0,
        "identnr": 83251076,
        "version": 0,
        "accessnr": 156,
        "manufacturer": 5317
      }
    }
    ```

- **Response:**
  - `HTTP 201 Created`: Message received successfully.
  - `HTTP 400 Bad Request`: exception message.

### Download Latest Measurements (CSV)

- **Endpoint:** `/csv/`
- **Method:** `GET`
- **Response:** CSV file containing the latest message of the current month for each device.

## CSV Columns

The CSV file contains the following columns:

- Date and time of the message (in a human-readable format)
- Device ID
- Device manufacturer
- Device type
- Device version
- Measurement dimension
- Value of the newest measurement
- Value of the measurement at the due date
- Due date (in a human-readable format)
- Status

 ## Running Tests
 The Metr Data CSV Exporter project includes comprehensive unit tests for models, serializers, views, and renderers. These tests ensure the correctness and functionality of the application. To run the tests, follow the instructions below:



 - ```shell
   pytest
