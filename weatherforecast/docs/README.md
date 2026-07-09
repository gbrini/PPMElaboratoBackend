# API Collection - Insomnia Usage

The project includes an Insomnia API collection that can be used to test the REST API endpoints.

## Importing the collection

To use the collection, import the `api_collection.yaml` file into the Insomnia application.

The collection also includes an environment containing two variables:

* `local_url`: the local development server URL
* `deployed_url`: the online deployed API URL

By default, all requests use the local environment URL. To test the deployed API, change the environment variable used in the request URL from the local value to the deployed value.

## Authentication

The collection includes authentication requests for obtaining JWT access and refresh tokens.

I have added an `After-response` script to both the login and the refresh token endpoints, so that the environment variables relating to the access and the refresh token are only updated when the status code of that particular requests is 200. These two variables are also used by all over the collection, so there will be no need to manually update the access token.

The included SQLite database already contains demo accounts and sample weather data, allowing the API workflow to be tested immediately.

The collection supports all the endpoints that have been developed. For testing purposes, the database is populated with these six cities (Berlin, Tokyo, New York, London, Paris, Florence, Milan and Rome), and daily weather forecasts are available for all of them from 9 July (00:00) until 16 July (23:00).
Please note that all data is available in the admin panel, where access is restricted to the `admin_demo` user only.
