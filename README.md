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

## Demo accounts
For this API there are already set up 3 different users:

| ROLE | Username | Password |
|:---|:---|:---:|
| Admin | aaa | aaa |
| Premium | aaa | aaa |
| Standard | aaa | aaa |