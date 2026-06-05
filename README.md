# Weather API - Guido Brini

The Weather API, as the name suggests, is a REST API project developed using the Django REST Framework for UNIFI’s PPM courses.

This API defines three user roles, as well as allowing access by unregistered users.

The table below sets out all the features and the availability of the roles.

| API description | Method| Anon | Standard | Premium | Admin |
|:---|:---|:---:|:---:|:---:|:---:|
| weather_forecast | GET | X| X| X|X|
| weather_forecast | POST | | | |X|
| weather_forecast_detail | DELETE | | | |X|
| weather_forecast_detail | PUT | | | |X|
| weather_forecast_query_history | GET | | |X |X|
| weather_forecast_query_history_detail | GET | | |X |X|
| weather_forecast_tracking | GET | | |X |X|
| Rate Limit     |        |5/day |   5/day    |5/day    | Unlimited    |

## Local installation
```bash
#First of all clone the repo in you desidered folder  
git clone https://github.com/user/repo.git
cd project-folder

#Create and activate the virtual environment
python -m venv .venv
source .venv/bin/activate

#Install the requirements
pip install -r requirements.txt
```

## Start the application
```bash
#Inside the project folder
python manage.py runserver
```

## Demo accounts
For this API there are already set up 3 different users:

| ROLE | Username | Password |
|:---|:---|:---:|
| Admin | aaa | aaa |
| Premium | aaa | aaa |
| Standard | aaa | aaa |

## Endpoint documentation

- ### weather_forecast
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

- ### weather_forecast
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

## Tests












[1]: https://localhost