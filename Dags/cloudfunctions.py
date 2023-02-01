from google.auth.transport.requests import Request
from google.oauth2 import id_token
import requests

def trigger_dag(data, context=None):
        # This script is intended to be used with Composer 1 environments
    # In Composer 2, the Airflow Webserver is not in the tenant project
    # so there is no tenant client ID
    # See https://cloud.google.com/composer/docs/composer-2/environment-architecture
    # for more details
    import google.auth
    import google.auth.transport.requests
    import requests
    import six.moves.urllib.parse

    # Authenticate with Google Cloud.
    # See: https://cloud.google.com/docs/authentication/getting-started
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    authed_session = google.auth.transport.requests.AuthorizedSession(credentials)

    # project_id = 'YOUR_PROJECT_ID'
    # location = 'us-central1'
    # composer_environment = 'YOUR_COMPOSER_ENVIRONMENT_NAME'

    environment_url = (
        "https://composer.googleapis.com/v1beta1/projects/{}/locations/{}"
        "/environments/{}"
    ).format('sadaindia-tvm-poc-de', 'us-central1', 'usecase-envrnm')
    composer_response = authed_session.request("GET", environment_url)
    environment_data = composer_response.json()
    composer_version = environment_data["config"]["softwareConfig"]["imageVersion"]
    if "composer-1" not in composer_version:
        version_error = ("This script is intended to be used with Composer 1 environments. "
                        "In Composer 2, the Airflow Webserver is not in the tenant project, "
                        "so there is no tenant client ID. "
                        "See https://cloud.google.com/composer/docs/composer-2/environment-architecture for more details.")
        raise (RuntimeError(version_error))
    airflow_uri = environment_data["config"]["airflowUri"]

    # The Composer environment response does not include the IAP client ID.
    # Make a second, unauthenticated HTTP request to the web server to get the
    # redirect URI.
    redirect_response = requests.get(airflow_uri, allow_redirects=False)
    redirect_location = redirect_response.headers["location"]

    # Extract the client_id query parameter from the redirect.
    parsed = six.moves.urllib.parse.urlparse(redirect_location)
    query_string = six.moves.urllib.parse.parse_qs(parsed.query)
    clientID=query_string["client_id"][0]


    IAM_SCOPE = 'https://www.googleapis.com/auth/iam'
    OAUTH_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
    # If you are using the stable API, set this value to False
    # For more info about Airflow APIs see https://cloud.google.com/composer/docs/access-airflow-api
    USE_EXPERIMENTAL_API = False
    """Makes a POST request to the Composer DAG Trigger API

    When called via Google Cloud Functions (GCF),
    data and context are Background function parameters.

    For more info, refer to
    https://cloud.google.com/functions/docs/writing/background#functions_background_parameters-python

    To call this function from a Python script, omit the ``context`` argument
    and pass in a non-null value for the ``data`` argument.

    This function is currently only compatible with Composer v1 environments.
    """

    # Fill in with your Composer info here
    # Navigate to your webserver's login page and get this from the URL
    # Or use the script found at
    # https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/composer/rest/get_client_id.py
    client_id = clientID
    # This should be part of your webserver's URL:
    # {tenant-project-id}.appspot.com
    webserver_id = 'gc1383166fcde49aap-tp'
    # The name of the DAG you wish to trigger
    dag_name = 'composer_sample_trigger_response_dag'

    if USE_EXPERIMENTAL_API:
        endpoint = f'api/experimental/dags/{dag_name}/dag_runs'
        json_data = {'conf': data, 'replace_microseconds': 'false'}
    else:
        endpoint = f'api/v1/dags/{dag_name}/dagRuns'
        json_data = {'conf': data}
    webserver_url = (
        'https://'
        + webserver_id
        + '.appspot.com/'
        + endpoint
    )
    # Make a POST request to IAP which then Triggers the DAG
    make_iap_request(
        webserver_url, client_id, method='POST', json=json_data)


# This code is copied from
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/iap/make_iap_request.py
# START COPIED IAP CODE
def make_iap_request(url, client_id, method='GET', **kwargs):
    """Makes a request to an application protected by Identity-Aware Proxy.
    Args:
      url: The Identity-Aware Proxy-protected URL to fetch.
      client_id: The client ID used by Identity-Aware Proxy.
      method: The request method to use
              ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE')
      **kwargs: Any of the parameters defined for the request function:
                https://github.com/requests/requests/blob/master/requests/api.py
                If no timeout is provided, it is set to 90 by default.
    Returns:
      The page body, or raises an exception if the page couldn't be retrieved.
    """
    # Set the default timeout, if missing
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 90

    # Obtain an OpenID Connect (OIDC) token from metadata server or using service
    # account.
    google_open_id_connect_token = id_token.fetch_id_token(Request(), client_id)

    # Fetch the Identity-Aware Proxy-protected URL, including an
    # Authorization header containing "Bearer " followed by a
    # Google-issued OpenID Connect token for the service account.
    resp = requests.request(
        method, url,
        headers={'Authorization': 'Bearer {}'.format(
            google_open_id_connect_token)}, **kwargs)
    if resp.status_code == 403:
        raise Exception('Service account does not have permission to '
                        'access the IAP-protected application.')
    elif resp.status_code != 200:
        raise Exception(
            'Bad response from application: {!r} / {!r} / {!r}'.format(
                resp.status_code, resp.headers, resp.text))
    else:
        return resp.text
# END COPIED IAP CODE