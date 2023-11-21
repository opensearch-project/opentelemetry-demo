#!/bin/bash

# Environment variables for authentication
OPENSEARCH_USERNAME="your_username"
OPENSEARCH_PASSWORD="your_password"

# The endpoint URL for creating the datasource
ENDPOINT="https://localhost:9200/_plugins/_query/_datasources"

# The JSON payload
PAYLOAD='{
    "name": "my_prometheus",
    "connector": "prometheus",
    "properties": {
        "prometheus.uri": "http://localhost:9090"
    }
}'

# Execute the curl command
curl -k -X POST "$ENDPOINT" \
     -u "$OPENSEARCH_USERNAME:$OPENSEARCH_PASSWORD" \
     -H "Content-Type: application/json" \
     -d "$PAYLOAD"

# Check if the curl command was successful
if [ $? -eq 0 ]; then
    echo "Datasource created successfully."
else
    echo "Failed to create datasource."
fi
