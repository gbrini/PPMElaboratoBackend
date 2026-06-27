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
| register | POST | X| | ||
| login | POST | X| | ||
| refresh token | POST | X| | ||
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
- All the endpoints that supports the pagination will return `25` items per page by default, but that number can be changed using the parameter `page_size`, the maximum value is `100`. On the result object tehre will be two different keys, next fot the following page, and previous.

- ### register
    Register a user, the assigned role is `standard`. The username must be unique.

    * **URL:** `/api/users/register/`
    * **Method:** `POST`
    * **Auth Required:** `No`
    * **Role:** `Anon`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `username` | `string` | **Yes** | Username |
    | `password` | `string` | **Yes** | Password |
    | `password2` | `string` | **Yes** | Password, must be the same as `password` |
    | `email` | `string` | **No** | email |
    | `first_name` | `string` | **No** | First name |
    | `last_name` | `string` | **No** | Last name |

    #### Request Example

    ```bash
    http POST "http://127.0.0.1:8000/api/users/register/" \
    username="" password="" password2=""
    ```

    #### Response Examples

    **Success (201 CREATED)**

    ```json
    {
        "username": "",
        "email": "",
        "first_name": "",
        "last_name": ""
    }
    ```

    **Error (400 Bad Request)**

    ```json
    {
        "password": [
            "Passwords fields didn't match."
        ]
    }
    ```

- ### login
    Get the access and refresh token

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
    | `username` | `string` | **Yes** | Username |
    | `password` | `string` | **Yes** | Password |

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
- ### refresh token
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
    | `refresh` | `string` | **Yes** | Refresh token |

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
    | `unit` | `string` | **No** | Optional paramter to retrieve the temperature in the desired measurement unit (`C` the default value or `F`). |
    | `page` | `int` | **No** | The page number. |
    | `page_size` | `int` | **No** | The page size. |

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

- ### weather_forecast_query_history
    Retrieve personal search logs

    * **URL:** `/api/weather/forecast/history`
    * **Method:** `GET`
    * **Auth Required:** `Required`
    * **Role:** `Admin`, `Premium`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `page` | `int` | **No** | The page number. |
    | `page_size` | `int` | **No** | The page size. |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    #### Request Example

    ```bash
    http GET "http://127.0.0.1:8000/api/weather/history" \
    "Authorization: Bearer YOUR_API_KEY"
    ```

    #### Response Examples

    **Success (200 OK)**

    ```json
    {
        "count": 50,
        "next": "http://127.0.0.1:8000/api/weather/forecast/history?page=2&page_size=2",
        "previous": null,
        "results": [
            {
                "id": 50,
                "search_params": {
                    "location": "Tokyo",
                    "date": "2026-06-10",
                    "date_range": null,
                    "time": "17:00:00"
                },
                "timestamp": "2026-06-10T17:08:38.000994+02:00",
                "result_count": null,
                "user": 1
            },
            {
                "id": 49,
                "search_params": {
                    "location": "Tokyo",
                    "date": "2026-06-10",
                    "date_range": null,
                    "time": "17:00:00"
                },
                "timestamp": "2026-06-10T17:08:37.670434+02:00",
                "result_count": null,
                "user": 1
            }
        ]
    }
    ```

    **Error (400 Bad Request)**

    ```json
    {
        "detail": "Invalid page."
    }
    ```

- ### weather_forecast_query_history_detail
    Retrieve personal search log by id

    * **URL:** `/api/weather/forecast/history/{pk}`
    * **Method:** `GET`
    * **Auth Required:** `Required`
    * **Role:** `Admin`, `Premium`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `pk` | `int` | **Yes** | The log id. |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    #### Request Example

    ```bash
    http GET "http://127.0.0.1:8000/api/weather/history/3" \
    "Authorization: Bearer YOUR_API_KEY"
    ```

    #### Response Examples

    **Success (200 OK)**

    ```json
    {
        "id": 3,
        "search_params": {
            "location": "Tokyo"
        },
        "timestamp": "2026-06-02T09:56:03.830608+02:00",
        "result_count": null,
        "user": 1
    }
    ```

    **Error (400 Bad Request)**

    ```json
    {
        "detail": "No UserSearchHistory matches the given query."
    }
    ```

- ### weather_forecast_tracking
    Get the tracking of the request limit, grouped by day. There are shown only days with at least `1` request. On the object with the date of the requesting day, will be added `throttle_rate`, displaying the user's throttle rate.

    * **URL:** `/api/weather/forecast/tracking/`
    * **Method:** `GET`
    * **Auth Required:** `Yes`
    * **Role:** `Admin`, `Premium`, `Standard`

    #### Path Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |
    | `today` | `string` | **No** | `true` or `false` default `false` |

    #### Query Parameters

    | Parameter | Type | Required | Description |
    | :--- | :--- | :--- | :--- |

    #### Request Example

    ```bash
    http GET "http://127.0.0.1:8000/api/weather/forecast/tracking?today=true" \
    username="" password=""
    ```

    #### Response Examples

    **Success (200 OK)**

    ```json
    [
        {
            "date": "2026-06-27",
            "count": 1,
            "throttle_rate": "100/day"
        }
    ]
    ```

    **Error (400 Bad Request)**

    ```json
    
    ```

## Tests

```bash
python manage.py test
```











## License
This project is available for use under the MIT License.

[1]: https://localhost