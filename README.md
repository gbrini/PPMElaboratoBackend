# Weather API - Guido Brini

**Chosen Project Type:** REST API  
**Framework Used:** Django REST Framework (DRF)

The Weather API is a REST API project developed using the Django REST Framework for UNIFI’s PPM course. The purpose of this application is to manage and serve weather forecast data, tracking user query history and implementing role-based access control along with strict rate-limiting.

---

## Implemented Features by User Role

This API defines three distinct user roles, alongside allowing limited access for unregistered (anonymous) users. 

* **Anonymous (Anon):** Can log in, refresh JWT tokens, and check current weather forecasts (up to 5 requests per day).
* **Standard User:** Can check weather forecasts (up to 50 requests per day).
* **Premium User:** Can check weather forecasts (up to 100 requests per day), view their own query history, and track custom weather data.
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
- All the endpoint listed down below can be tested using Httpie (installed from requirements.txt)
- All the endpoints that supports the pagination will return `25` items per page by default, but that number can be changed using the parameter `page_size`, the maximum value is `100`.

- ### login
    Get the access token

    * **URL:** `/api/users/login/`
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
    http POST "http://127.0.0.1:8000/api/users/login/" \
    username="" password=""
    ```

    #### Response Examples

    **Success (200 OK)**

    ```json
    {
        "refresh": "refresh_token",
        "access": "access_token"
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

    * **URL:** `/api/users/refresh/`
    * **Method:** `POST`
    * **Auth Required:** `No`
    * **Role:** `Anon`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `refresh` | `object` | **Yes** | Refresh token |

    #### Request Example

    ```bash
    http POST "http://127.0.0.1:8000/api/users/refresh/" \
    refresh=""
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

    * **URL:** `/api/weather/forecast/`
    * **Method:** `GET`
    * **Auth Required:** `Optional`
    * **Role:** `Any + Anon`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `location` | `string` | **Yes** | The location name of the city you want to query. |
    | `date` | `string` | **No** | The date you want to query, in the format yyyy-mm-dd. |
    | `date_range_before` | `string` | **No** | The date range you want to query, in the format yyyy-mm-dd. |
    | `date_range_after` | `string` | **No** | The date range you want to query, in the format yyyy-mm-dd. |
    | `hour_min` | `string` | **No** | The hour range you want to query (Both 09 and 9 are valid). |
    | `hour_max` | `string` | **No** | The hour range you want to query (Both 09 and 9 are valid). |
    | `page_size` | `string` | **No** | The page size. |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    These are the assumptions for these filters:
    - If neither date or date range is provided then the default date is the request day.
    - If both date and at least one date range filter is provided, the the range will be discarded.
    - Both bour_min and hour_max are constrained between 0 and 23, hour_max has to be greater or equal then hour_min.

    Api behaviour:
    - If the hour_range is not provided will return all the data that matches the other filter starting from the midnight of the initial date
    - Queryng as **admin** or **advanced user** will grant that the query with the filters will be saved in the history, so it might be retrieved with the appropriate API call.
    - This endpoint handles the pagination. In fact in the object response count will provide the number of the total elements retrieved, next and previous instead will provide the link for the pages keeping the filters. Queryng a page that doesn't exist will return raise a 404 error.

    #### Request Examples

    ```bash
    http GET "http://127.0.0.1:8000/api/weather/forecast/?location=Tokyo" \
    "Authorization: Bearer YOUR_API_KEY" \

    http GET "http://127.0.0.1:8000/api/weather/forecast/?location=Tokyo"
    
    http GET "http://127.0.0.1:8000/api/weather/forecast/?location=Tokyo&page=2"

    http GET "http://127.0.0.1:8000/api/weather/forecast/?location=Tokyo&date=2026-06-20"

    http GET "http://127.0.0.1:8000/api/weather/forecast/?location=Tokyo&date_range_before=2026-06-30&date_range_after=2026-06-20"

    http GET "http://127.0.0.1:8000/api/weather/forecast/?location=Tokyo&date=2026-06-30&hour_min=12&hour_max=15"
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

    API reasoning:
    - Every forecast date will be saved putting the seconds at 0

    * **URL:** `/api/weather/forecast/`
    * **Method:** `POST`
    * **Auth Required:** `Required`
    * **Role:** `Admin`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `location` | `string` | **Yes** | The forecast location. |
    | `forecast_date` | `string` | **Yes** | The forecast date, by the format YYYY-MM-DDTHH:mm:ss |
    | `temperature` | `float` | **Yes** | The temperature in Celsius. (e.g., `28.5`) |
    | `condition` | `string` | **Yes** | The forecast decription. |

    #### Request Example

    ```bash
    http POST "http://127.0.0.1:8000/api/weather/forecast/" \
    "Authorization: Bearer YOUR_API_KEY" \
    location="Tokyo" forecast_date="2026-06-16T18:56" temperature=28 condition="Rain"
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

    * **URL:** `/api/weather/forecast/`
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
    http DELETE "http://127.0.0.1:8000/api/weather/forecast/6" \
    "Authorization: Bearer YOUR_API_KEY" \
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

    * **URL:** `/api/weather/forecast/`
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
    http PUT "http://127.0.0.1:8000/api/weather/forecast/6" \
    "Authorization: Bearer YOUR_API_KEY" \
    location="Tokyo" forecast_date="2026-05-31T15:54" temperature=28 condition="Rain"
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