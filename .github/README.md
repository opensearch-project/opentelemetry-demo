# <img src="https://opentelemetry.io/img/logos/opentelemetry-logo-nav.png" alt="OTel logo" width="32"> + <img src="https://avatars.githubusercontent.com/u/80134844?s=240&v=4" alt="OTel logo" width="35"> OpenTelemetry Demo with OpenSearch 

The following guide describes how to setup the OpenTelemetry demo with OpenSearch Observability using [Docker compose](#docker-compose) or [Kubernetes](#kubernetes).

## Docker compose

### Prerequisites

- Docker
- Docker Compose v2.0.0+
- 4 GB of RAM for the application

### Running this demo

```bash
git clone https://github.com/opensearch-project/opentelemetry-demo.git
cd opentelemetry-demo
docker compose up -d
```

### Services

Once the images are built and containers are started you can access:

- Webstore-Proxy (Via Nginx Proxy): http://nginx:90/ (`nginx` DNS name needs to be added )
    - [Defined here](https://github.com/opensearch-project/opentelemetry-demo/blob/079750428f1bddf16c029f30f478396e45559fec/.env#L58) 
- Webstore: http://frontend:8080/ (`frontend` DNS name needs to be added )
    - [Defined here](https://github.com/opensearch-project/opentelemetry-demo/blob/079750428f1bddf16c029f30f478396e45559fec/.env#L63) 
- Dashboards: http://dashboards:5601/ (`dashboards` DNS name needs to be added )
- Feature Flags UI: http://featureflag:8081/ (`featureflag` DNS name needs to be added )
    - [Defined here](https://github.com/opensearch-project/opentelemetry-demo/blob/079750428f1bddf16c029f30f478396e45559fec/.env#LL47C31-L47C31)
- Load Generator UI: http://loadgenerator:8089/ (`loadgenerator` DNS name needs to be added)
    - [Defined here](https://github.com/opensearch-project/opentelemetry-demo/blob/079750428f1bddf16c029f30f478396e45559fec/.env#L66)

OpenSearch has [documented](https://opensearch.org/docs/latest/observing-your-data/trace/trace-analytics-jaeger/#setting-up-opensearch-to-use-jaeger-data) the usage of the Observability plugin with jaeger as a trace signal source.

The next instructions are similar and use the same docker compose file.
1. Start the demo with the following command from the repository's root directory:
   ```
   docker compose up -d
   ```
**Note:** The docker compose `--no-build` flag is used to fetch released docker images from [ghcr](http://ghcr.io/open-telemetry/demo) instead of building from source.
Removing the `--no-build` command line option will rebuild all images from source. It may take more than 20 minutes to build if the flag is omitted.

### Explore and analyze the data With OpenSearch Observability
Review revised OpenSearch [Observability Architecture](architecture.md)

### Start learning OpenSearch Observability using our tutorial
[Getting started Tutorial](../tutorial/README.md)

#### Service map
![Service map](https://docs.aws.amazon.com/images/opensearch-service/latest/developerguide/images/ta-dashboards-services.png)

#### Traces
![Traces](https://opensearch.org/docs/2.6/images/ta-trace.png)

#### Correlation
![Correlation](https://opensearch.org/docs/latest/images/observability-trace.png)

#### Logs
![Logs](https://opensearch.org/docs/latest/images/trace_log_correlation.gif)
