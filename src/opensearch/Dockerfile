# Declare a build argument for the version
ARG VERSION

# Use OpenSearch image as base
FROM opensearchproject/opensearch:${VERSION}

# Install prometheus plugin (https://github.com/aiven/prometheus-exporter-plugin-for-opensearch)
USER root
RUN /usr/share/opensearch/bin/opensearch-plugin install https://github.com/aiven/prometheus-exporter-plugin-for-opensearch/releases/download/${VERSION}.0/prometheus-exporter-${VERSION}.0.zip

# Switch back to opensearch user
USER opensearch