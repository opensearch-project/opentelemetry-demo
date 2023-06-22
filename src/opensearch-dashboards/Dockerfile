# Use OpenSearch image as base
FROM opensearchproject/opensearch-dashboards:2.7.0

# Install plugin (https://opensearch.org/docs/1.2/dashboards/install/plugins/)
USER root
RUN sudo /usr/share/opensearch-dashboards/bin/opensearch-dashboards-plugin install <plugin-url>

# Switch back to opensearch user
USER opensearch-dahsboards
