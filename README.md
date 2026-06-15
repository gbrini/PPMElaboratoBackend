# Weather API - Guido Brini

**Chosen Project Type:** REST API  
**Framework Used:** Django REST Framework (DRF)

The Weather API is a REST API project developed using the Django REST Framework for UNIFI’s PPM course. The purpose of this application is to manage and serve weather forecast data, tracking user query history and implementing role-based access control along with strict rate-limiting.

---

## Implemented Features by User Role

This API defines three distinct user roles, alongside allowing limited access for unregistered (anonymous) users. 

* **Anonymous (Anon):** Can log in, refresh JWT tokens, and check current weather forecasts (up to 5 requests per day).
* **Standard User:** Can check weather forecasts (up to 5 requests per day).
* **Premium User:** Can check weather forecasts (up to 5 requests per day), view their own query history, and track custom weather data.
* **Admin:** Full CRUD capabilities on weather data, access to all tracking/history logs, and enjoys unlimited API requests.

### Role & Feature Matrix

| API description | Method| Anon | Standard | Premium | Admin |
|:---|:---|:---:|:---:|:---:|:---:|
| login | POST | X| | ||
| refresh | POST | X| | ||
| weather_forecast | GET | X| X| X|X|
| weather_forecast | POST | | | |X|
| weather_forecast_detail | DELETE | | | |X|
| weather_forecast_detail | PUT | | | |X|
| weather_forecast_query_history | GET | | |X |X|
| weather_forecast_query_history_detail | GET | | |X |X|
| weather_forecast_tracking | GET | | |X |X|
| Rate Limit     |        |5/day |   50/day    |100/day    | Unlimited    |

---

## Online Deployment
The APIs are live and available at the following production URL: [URL Here]

---

## Local Installation

Follow these steps to get the project running locally:

```bash
# 1. Clone the repository into your desired folder
git clone https://github.com/user/repo.git
cd project-folder

# 2. Create and activate the virtual environment
python -m venv .venv

# If using Linux/macOS
source .venv/bin/activate

# If using Windows (PowerShell)
.venv\Scripts\Activate.ps1
# If using Windows (CMD)
.venv\Scripts\activate.bat 

# 3. Install the requirements
pip install -r requirements.txt
```

## Start the application
```bash
# Navigate to the Django project directory
cd weatherforecast

# Apply database migrations
python manage.py migrate

# Start the local development server
python manage.py runserver
```

## Demo accounts
For this API there are already set up 3 different users:

| ROLE | Username | Password |
|:---|:---|:---:|
| Admin | aaa | aaa |
| Premium | aaa | aaa |
| Standard | aaa | aaa |

## Database
The included SQLite database file is located at **weatherforecast/db.sqlite3**. This file is pre-populated and contains all the necessary demo data, tables, and roles required to test the REST APIs immediately.

## Endpoint documentation
- ### login
    Get the access token

    * **URL:** `/users/login/`
    * **Method:** `POST`
    * **Auth Required:** `No`
    * **Role:** `Anon`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `data` | `object` | **Yes** | Username and password. |

    #### Request Example

    ```bash
    curl -X POST "http://127.0.0.1:8000/users/login/" \
    -H "Accept: application/json"
    -d '{ "username": "",  "password": "" }'
    ```

    #### Response Examples

    **Success (200 OK)**

    ```json
    {
        "refresh": "",
        "access": ""
    }
    ```

    **Error (400 Bad Request)**

    ```json
   {
        "username": [
            "This field is required."
        ],
        "password": [
            "This field is required."
        ]
    }
    ```
- ### refresh
    Refresh the access token

    * **URL:** `/users/refresh/`
    * **Method:** `POST`
    * **Auth Required:** `No`
    * **Role:** `Anon`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `data` | `object` | **Yes** | Refresh token |

    #### Request Example

    ```bash
    curl -X POST "http://127.0.0.1:8000/users/refresh/" \
    -H "Accept: application/json"
    -d '{ "refresh": "" }'
    ```

    #### Response Examples

    **Success (200 OK)**

    ```json
    {
        "access": ""
    }
    ```

    **Error (400 Bad Request)**

    ```json
    {
        "refresh": [
            "This field may not be blank."
        ]
    }
    ```

- ### weather_forecast (GET)
    Retrieves the forecast information

    * **URL:** `/weather/forecast/`
    * **Method:** `GET`
    * **Auth Required:** `Optional`
    * **Role:** `Any + Anon`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `location` | `string` | **Yes** | The location name of the city you want to query. |

    #### Request Example

    ```bash
    curl -X GET "http://127.0.0.1:8000/weather/forecast/?location=Tokyo" \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Accept: application/json"

    curl -X GET "http://127.0.0.1:8000/weather/forecast/?location=Tokyo" \
    -H "Accept: application/json"
    ```

    #### Response Examples

    **Success (200 OK)**

    ```json
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
            "id": 93,
            "location": "Tokyo",
            "temperature": 15.0,
            "condition": "Sunny",
            "forecast_date": "2026-06-01T18:02:19+02:00"
            }
        ]
    }
    ```

    **Error (400 Bad Request)**

    ```json
    {
        "location": [
            "This field is required."
        ]
    }
    ```

- ### weather_forecast (POST)
    Add a forecast object

    * **URL:** `/weather/forecast/`
    * **Method:** `POST`
    * **Auth Required:** `Required`
    * **Role:** `Admin`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `data` | `object` | **Yes** | The forecast object. |

    #### Request Example

    ```bash
    curl -X POST "http://127.0.0.1:8000/weather/forecast/" \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Accept: application/json"
    -d '{ "location": "Tokyo",  "forecast_date": "2026-05-31T15:54", "temperature": 28, "condition": "Rain" }'
    ```

    #### Response Examples

    **Success (201 CREATED)**

    ```json
    {
        "id": 94,
        "location": "Tokyo",
        "temperature": 28.0,
        "condition": "Rain",
        "forecast_date": "2026-05-31T15:54:00+02:00"
    }
    ```

    **Error (400 Bad Request)**

    ```json
    {
        "location": [
            "This field is required."
        ]
    }
    ```

- ### weather_forecast_detail (DELETE)
    DELETE a forecast object

    * **URL:** `/weather/forecast/`
    * **Method:** `DELETE`
    * **Auth Required:** `Required`
    * **Role:** `Admin`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `pk` | `int` | **Yes** | The forecast object id. |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    #### Request Example

    ```bash
    curl -X DELETE "http://127.0.0.1:8000/weather/forecast/6" \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Accept: application/json"
    ```

    #### Response Examples

    **Success (204 NO CONTENT)**

    ```json
    
    ```

    **Error (404 NOT FOUND)**

    ```json
    {
        "detail": "No WeatherQuery matches the given query."
    }
    ```

- ### weather_forecast_detail (PUT)
    Modify a forecast object

    * **URL:** `/weather/forecast/`
    * **Method:** `PUT`
    * **Auth Required:** `Required`
    * **Role:** `Admin`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `pk` | `int` | **Yes** | The forecast object id. |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `data` | `object` | **Yes** | The forecast object. |

    #### Request Example

    ```bash
    curl -X PUT "http://127.0.0.1:8000/weather/forecast/6" \
    -H "Authorization: Bearer YOUR_API_KEY" \
    -H "Accept: application/json"
    -d '{ "location": "Tokyo",  "forecast_date": "2026-05-31T15:54", "temperature": 28, "condition": "Rain" }'
    ```

    #### Response Examples

    **Success (200 OK)**

    ```json
    {
        "id": 94,
        "location": "Tokyo",
        "temperature": 28.0,
        "condition": "Rain",
        "forecast_date": "2026-05-31T15:54:00+02:00"
    }
    ```

    **Error (400 Bad Request)**

    ```json
    {
        "location": [
            "This field is required."
        ]
    }
    ```

## Tests

```bash
python manage.py test
```











## License
This project is available for use under the MIT License.

[1]: https://localhost