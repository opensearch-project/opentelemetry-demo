# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0

import os
import json
import configparser
import time
import logging
from opensearchpy import OpenSearch, RequestsHttpConnection, OpenSearchException
import requests
from requests.auth import HTTPBasicAuth
import os

# headers
DASHBOARDS_HEADERS = {'Content-Type': 'application/json', 'osd-xsrf': 'true'}
RESTAPI_HEADERS = {'Content-Type': 'application/json'}

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

# load all integration configuration data
app_data = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())
app_data.read('data.ini')

# verify connection to opensearch - when successful create the transport client
def test_connection(opensearch_host, auth):
    max_retries = 100  # Maximum number of retries
    retry_interval = 20  # Wait for 20 seconds between retries

    for i in range(max_retries):
        try:
            response = requests.get(
                url=f'https://{opensearch_host}:9200/',
                auth=auth,
                headers=RESTAPI_HEADERS,
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

# create data streams
def create_data_streams(auth,items,domain):
        data_streams = items[domain].split(',')
        for ds in data_streams:
            try:
                response = requests.put(
                    url=f'https://{opensearch_host}:9200/_data_stream/{ds}',
                    auth=auth,
                    headers=RESTAPI_HEADERS,
                    verify=False  # Disable SSL verification
                )
                response.raise_for_status()  # Raise an exception if the request failed
                logger.info(f'Successfully created data stream: {ds}')
            except requests.HTTPError as e:
                logger.error(f'Failed to create data stream: {ds}, error: {str(e)}')

# load dashboards in the display folder
def load_dashboards(auth, items):
    for key,value in items.items():
        try:
            response = requests.post(
                url=f'http://{opensearch_dashboard}:5601/api/saved_objects/_import?overwrite=true',
                auth=auth,
                files={'file': (f'{key}.ndjson', value)},
                headers={'osd-xsrf': 'true'},
                verify=False  # Disable SSL verification
            )
            response.raise_for_status()  # Raise an exception if the request failed
            logger.info(f'Successfully loaded dashboard: {key}')
            print(f'Successfully loaded: {key}')
        except requests.HTTPError as e:
            logger.error(f'Failed to load dashboard: {key}, error: {str(e)}')

# create the data_streams based on the list given in the data-stream.json file
def create_datasources(auth,items):
    try:
        response = requests.get(
            url=f'https://{opensearch_host}:9200/_plugins/_query/_datasources',
            auth=auth,
            verify=False,  # Disable SSL verification
            headers=RESTAPI_HEADERS
        )
        response.raise_for_status()  # Raise an exception if the request failed
        current_datasources = response.json()  # convert response to json
    except requests.HTTPError as e:
        logger.error(f'Failed to fetch datasources, error: {str(e)}')

    for key,value in items.items():
        datasource = json.loads(items[key])
        # check if datasource already exists
        if any(d['name'] == datasource['name'] for d in current_datasources):
            logger.info(f'Datasource already exists: {key}')
            continue  # Skip to the next datasource if this one already exists

        try:
            response = requests.post(
                url=f'https://{opensearch_host}:9200/_plugins/_query/_datasources',
                auth=auth,
                json=datasource,
                verify=False,  # Disable SSL verification
                headers=RESTAPI_HEADERS
            )
            response.raise_for_status()  # Raise an exception if the request failed
            logger.info(f'Successfully created datasource: {key}')
        except requests.HTTPError as e:
            logger.error(f'Failed to create datasource: {key}, error: {str(e)}')

# log distribution details
def get_dist_version(auth):
    logger.debug('start get_dist_version')
    res = requests.get(f'https://{opensearch_host}:9200/',
     auth=auth,
     verify=False,  # Disable SSL verification
    )
    logger.info(res.text)

    version = json.loads(res.text)['version']
    domain_version = version['number']
    lucene_version = version['lucene_version']
    dist_name = version.get('distribution', 'elasticsearch')
    return dist_name, domain_version

# Generic upsert api using general endpoint
def upsert_obj(auth, items, api):
    for key in items:
        payload = json.loads(items[key])
        res = requests.put(
            url=f'https://{opensearch_host}:9200/{api}/{key}',
            auth=auth,
            json=payload,
            verify=False,  # Disable SSL verification
            headers=RESTAPI_HEADERS
        )
        if res.status_code == 200:
            logger.debug(output_message(key, res))
        else:
            logger.error(output_message(key, res))

# format response message
def output_message(key, res):
    return f'{key}: status={res.status_code}, message={res.text}'

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # attempt connection to cluster
    client = test_connection(opensearch_host,auth)
    # print distribution details
    dist_name, domain_version = get_dist_version(auth)
    logger.info(f'dist_name: {dist_name}, domain_version: {domain_version}')

    # load composable index template
    logger.info('Create/Update component index templates')
    upsert_obj(auth, app_data['component-templates'],
               api='_component_template')
    # load index template
    logger.info('Create/Update index templates')
    upsert_obj(auth, app_data['index-templates'],
               api='_index_template')
    # load data stream
    logger.info('Create/Update index templates')
    upsert_obj(auth, app_data['index-templates'],
               api='_index_template')
    # load data-streams
    logger.info('Create datastreams ')
    create_data_streams(auth, app_data['datastreams'],
               domain='observability')

    # load data-source
    logger.info('Create data-source ')
    create_datasources(auth, app_data['datasources'])

    # load dashboards
    logger.info('Create dashboards ')
    load_dashboards(auth, app_data['dashboards'])

    logger.info('Finished loading assets ')
