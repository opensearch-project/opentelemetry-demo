
![](https://raw.githubusercontent.com/opensearch-project/.github/main/profile/banner.jpg)
# OpenSearch Observability OTEL Demo

Welcome to the [OpenSearch](https://opensearch.org/docs/latest) OpenTelemetry [Demo](https://opentelemetry.io/docs/demo/) documentation, which covers how to install and run the demo, and some scenarios you can use to view OpenTelemetry in action.

## Purpose
The purpose of this demo is to demonstrate the different capabilities of OpenSearch Observability to investigate and reflect your system.

![](../../../.github/img/DemoFlow.png)

### Services
[OTEL DEMO](https://opentelemetry.io/docs/demo/services/) Describes the list of services that are composing the Astronomy Shop.

The main services that are open to user interactions:

- [Dashboards](https://observability.playground.opensearch.org/)

- [Demo Proxy](https://observability.playground.demo-proxy.opensearch.org/)

- [Demo loader](https://observability.playground.demo-loader.opensearch.org/)

- [Demo feature-flag](https://observability.playground.demo-feature-flag.opensearch.org/)

### Screenshots
![](https://opentelemetry.io/docs/demo/screenshots/frontend-1.png)

_**The shopping App**_
![](https://opentelemetry.io/docs/demo/screenshots/frontend-2.png)

_**The feature flag**_
![](https://opentelemetry.io/docs/demo/screenshots/feature-flag-ui.png)

_**The load generator**_
![](https://opentelemetry.io/docs/demo/screenshots/load-generator-ui.png)

---
### Ingestion
The ingestion capabilities for OpenSearch is to be able to support multiple pipelines:
- [Data-Prepper](https://github.com/opensearch-project/data-prepper/) is an OpenSearch ingestion project that allows ingestion of OTEL standard signals using Otel-Collector
- [Jaeger](https://opensearch.org/docs/latest/observing-your-data/trace/trace-analytics-jaeger/) is an ingestion framework which has a build in capability for pushing OTEL signals into OpenSearch
- [Fluent-Bit](https://docs.fluentbit.io/manual/pipeline/outputs/opensearch) is an ingestion framework which has a build in capability for pushing OTEL signals into OpenSearch

### Integrations -
The integration service is a list of pre-canned assets that are loaded in a combined manner to allow users the ability for simple and automatic way to discover and review their services topology.

These (demo-sample) integrations contain the following assets:
- components & index template mapping
- datasources
- data-stream & indices
- queries
- dashboards
   
