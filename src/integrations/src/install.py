import os
import json
import time
import logging
from opensearchpy import OpenSearch, RequestsHttpConnection, OpenSearchException
import requests
from requests.auth import HTTPBasicAuth
import os

# load env variables
opensearch_host = os.getenv('OPENSEARCH1_HOST', 'opensearch-node1')
opensearch_dashboard = os.environ.get('OPENSEARCH_DASHBOARD_HOST', 'opensearch-dashboards')

# For testing only. Don't store credentials in code.
auth = ('admin', 'admin')

# Configure logging to file
logging.basicConfig(
    filename='application.log',  # The file where the logs should be written to
    filemode='a',  # Append mode, use 'w' for overwriting each time the script is run
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# verify connection to opensearch - when successful create the transport client
def test_connection(opensearch_host, auth):
    max_retries = 100  # Maximum number of retries
    retry_interval = 20  # Wait for 20 seconds between retries

    for i in range(max_retries):
        try:
            response = requests.get(
                url=f'https://{opensearch_host}:9200/',
                auth=HTTPBasicAuth('admin', 'admin'),
                headers={'Content-Type': 'application/json'},
                verify=False  # Disable SSL verification
            )
            response.raise_for_status()  # Raise an exception if the request failed
            logging.info('Successfully connected to OpenSearch')
            # Exit the function if connection is successful, return client
            return create_client(opensearch_host, auth)
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            logging.error(f'Failed to connect to OpenSearch, error: {str(e)}')

        logging.info(f'Attempt {i + 1} failed, waiting for {retry_interval} seconds before retrying...')
        time.sleep(retry_interval)

    logging.error(f'Failed to connect to OpenSearch after {max_retries} attempts')
    exit(1)  # Exit the program with an error code

# Create the client with SSL/TLS enabled, but hostname verification disabled.
def create_client(opensearch_host, auth):
    return OpenSearch(
        hosts = [{'host': opensearch_host, 'port': 9200}],
        http_compress = True,  # enables gzip compression for request bodies
        http_auth = auth,
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
        timeout=20,
        max_retries=50,  # Increasing max_retries from 3 (default) to 50
        retry_on_timeout=True
    )

# create mapping components to compose the different observability categories
def create_mapping_components(client):
   mapping_dir = '../mapping-components/'
   for filename in os.listdir(mapping_dir):
        if filename.endswith('.mapping'):
            with open(os.path.join(mapping_dir, filename), 'r') as f:
                mapping = json.load(f)

                template_name = os.path.splitext(filename)[0]  # Remove the .mapping extension
                logger.info(f'About to load  template: {template_name}')
                # Create the component template
                try:
                    response = requests.put(
                        url=f'https://{opensearch_host}:9200/_component_template/{template_name}_template',
                        auth=HTTPBasicAuth('admin', 'admin'),
                        json=mapping,
                        verify=False,  # Disable SSL verification
                        headers={'Content-Type': 'application/json'}
                    )
                    response.raise_for_status()  # Raise an exception if the request failed
                    logger.info(f'Successfully created component template: {template_name}')
                except requests.HTTPError as e:
                    logger.error(f'Failed to create component template: {template_name}, error: {str(e)}')

# Create the templates from the mapping content
def create_mapping_templates(client):
    mapping_dir = '../mapping-templates/'
    for filename in os.listdir(mapping_dir):
        if filename.endswith('.mapping'):
            with open(os.path.join(mapping_dir, filename), 'r') as f:
                mapping = json.load(f)

                template_name = os.path.splitext(filename)[0]  # Remove the .mapping extension
                logger.info(f'About to created index template: {template_name}')

                # Create the template
                try:
                    client.indices.put_index_template(name=template_name, body=mapping)
                    logger.info(f'Successfully created index template: {template_name}')
                except OpenSearchException as e:
                    logger.error(f'Failed to create index template: {template_name}, error: {str(e)}')

# create data streams
def create_data_streams():
    with open('../indices/data-stream.json', 'r') as f:
        data = json.load(f)
        data_streams = data.get('data-stream', [])

        for ds in data_streams:
            try:
                response = requests.put(
                    url=f'https://{opensearch_host}:9200/_data_stream/{ds}',
                    auth=HTTPBasicAuth('admin', 'admin'),
                    headers={'Content-Type': 'application/json'},
                    verify=False  # Disable SSL verification
                )
                response.raise_for_status()  # Raise an exception if the request failed
                logger.info(f'Successfully created data stream: {ds}')
            except requests.HTTPError as e:
                logger.error(f'Failed to create data stream: {ds}, error: {str(e)}')

# load dashboards in the display folder
def load_dashboards():
    dashboard_dir = '../display/'
    for filename in os.listdir(dashboard_dir):
        if filename.endswith('.ndjson'):
            with open(os.path.join(dashboard_dir, filename), 'r') as f:
                dashboard_data = f.read()
                dashboard_name = os.path.splitext(filename)[0]  # Remove the .json extension
                logger.info(f'About to load dashboard: {dashboard_name}')

                # Load the dashboard
                try:
                    response = requests.post(
                        url=f'http://{opensearch_dashboard}:5601/api/saved_objects/_import?overwrite=true',
                        auth=HTTPBasicAuth('admin', 'admin'),
                        files={'file': (f'{dashboard_name}.ndjson', dashboard_data)},
                        headers={'osd-xsrf': 'true'},
                        verify=False  # Disable SSL verification
                    )
                    response.raise_for_status()  # Raise an exception if the request failed
                    logger.info(f'Successfully loaded dashboard: {dashboard_name}')
                    print(f'Successfully loaded: {dashboard_name}')
                except requests.HTTPError as e:
                    logger.error(f'Failed to load dashboard: {dashboard_name}, error: {str(e)}')

# create the data_streams based on the list given in the data-stream.json file
def create_datasources():
    datasource_dir = '../datasource/'
    # get current list of data sources
    try:
        response = requests.get(
            url=f'https://{opensearch_host}:9200/_plugins/_query/_datasources',
            auth=HTTPBasicAuth('admin', 'admin'),
            verify=False,  # Disable SSL verification
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()  # Raise an exception if the request failed
        current_datasources = response.json()  # convert response to json
    except requests.HTTPError as e:
        logger.error(f'Failed to fetch datasources, error: {str(e)}')

    for filename in os.listdir(datasource_dir):
        if filename.endswith('.json'):
            with open(os.path.join(datasource_dir, filename), 'r') as f:
                datasource = json.load(f)
                # check if datasource already exists
                if any(d['name'] == datasource['name'] for d in current_datasources):
                    logger.info(f'Datasource already exists: {filename}')
                    continue  # Skip to the next datasource if this one already exists

                try:
                    response = requests.post(
                        url=f'https://{opensearch_host}:9200/_plugins/_query/_datasources',
                        auth=HTTPBasicAuth('admin', 'admin'),
                        json=datasource,
                        verify=False,  # Disable SSL verification
                        headers={'Content-Type': 'application/json'}
                    )
                    response.raise_for_status()  # Raise an exception if the request failed
                    logger.info(f'Successfully created datasource: {filename}')
                except requests.HTTPError as e:
                    logger.error(f'Failed to create datasource: {filename}, error: {str(e)}')



if __name__ == '__main__':
    # import all assets
    client = test_connection(opensearch_host,auth)
    create_mapping_components(client)
    create_mapping_templates(client)
    create_data_streams()
    load_dashboards()
    create_datasources()