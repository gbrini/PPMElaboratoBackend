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

After logging in, use the returned access token in authenticated requests through the Authorization header:

```
Authorization: Bearer <ACCESS_TOKEN>
```

The included SQLite database already contains demo accounts and sample weather data, allowing the API workflow to be tested immediately.
