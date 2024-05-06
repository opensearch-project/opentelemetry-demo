# Getting Started
Getting started with the OTEL demo including running the OpenSearch Server and Dashboard.

`docker-compose up -d` starts all the services and initiates the load-generator activity for synthetically creating user activity on the demo web store.

The following web-pages can be directly access to review the load generator
 - http://localhost:8089/

 - Here the synthetic testing process can be started 

![](./img/load-generator.png)

The following web-pages can be directly access to actually simulate store purchase
- http://localhost:8080/ (front-end) OR  http://localhost:90 (nginx-forntend proxy) 
- Here the actual shop demo can be used (simulated demo shop ...) 

![](./img/demo-app.png)


---

## Logging In Dashboard

Once all services are up and running - log-in to the Dashboard and enter the next credentials

**User: `admin`  | Password:  `my_%New%_passW0rd!@#`** 

- http://localhost:5601/
- OpenSearch Dashboard login

![dashboard-login.png](img%2Fdashboard-login.png)

## Store URLs in session storage
Enable Store URLs in session storage for allowing to view and edit Vega based visualizations 
- Once logged in, go to [Advanced Setting](http://localhost:5601/app/management/opensearch-dashboards/settings)
![store-url-in-session.png](img%2Fstore-url-in-session.png)

## Loading the OTEL Schema Manually
To install the OTEL schema manually using the [Simple Schema for Observability](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema/observability) load the schema creation command 
- Go to the [Dev Console](http://localhost:5601/app/dev_tools#/console) and import the next [sense file](../assets/sense.json)

![import-dev-console-sense-notebook.png](img%2Fimport-dev-console-sense-notebook.png)
![dev-tool-schema-notebook.png](img%2Fdev-tool-schema-notebook.png)


## Installing OTEL Services Demo 

Install OpenTelemetry Integration - navigate to the Integration sections and select the OTEL-Demo Integration
- Go to the [available integrations ](http://localhost:5601/app/integrations#/available) dialog
- Select the [OTEL-Demo Integration](http://localhost:5601/app/integrations#/available/otel-services)  
![integration-otel-services-selection.png](img%2Fintegration-otel-services-selection.png)
![integration-otel-services-info.png](img%2Fintegration-otel-services-info.png)

- Run the set-up integration and choose the `otel-*` index name as the integration data source

![integration-otel-services-setup.png](img%2Fintegration-otel-services-setup.png)

 - View all the Generated Dashboards:

![integration-otel-services-dashboards.png](img%2Fintegration-otel-services-dashboards.png)

## Ingestion Rate Dashboard
This dashboard show the 3 signals ingestion rate as they are shipped via data-prepper into OpenSearch indices

![otel-ingestion-rate-dashboard.png](img%2Fotel-ingestion-rate-dashboard.png)

## Services High Level Dashboards View
This dashboard show the 3 signals ingestion rate as they are shipped via data-prepper into OpenSearch indices
![services-general-dashboard.png](img%2Fservices-general-dashboard.png)

## Single Service Details Dashboards View
This dashboard show the specific service details including associated high level view of the metrics collected for the service 
![specific-service-dashboard.png](img%2Fspecific-service-dashboard.png)

## Service Metrics View

### Service Metrics system projection Dashboards 
This dashboard show the specific service details in particular the system related metrics collected for the service

![amp-services-system-metrics-details.png](img%2Famp-services-system-metrics-details.png)

### Service Metrics network projection Dashboards 
This dashboard show the specific service details in particular the network related metrics collected for the service

![amp-services-network-metrics-details.png](img%2Famp-services-network-metrics-details.png)

## Metrics Analytics

### Setting Up Prometheus `datasource`
- First [setup](http://localhost:5601/app/datasources#/new) the Prometheus datasource we wanted to connect with 
![configure-prometheus-datasource.png](img%2Fconfigure-prometheus-datasource.png)

### Query Prometheus OTEL metrics
- [Select the OTEL metrics](http://localhost:5601/app/observability-metrics#/) (Prometheus / OpenSearch) we want to display 
![metrics-analytics-prometheus.png](img%2Fmetrics-analytics-prometheus.png)
![metrics-analytics-prometheus-select-metrics.png](img%2Fmetrics-analytics-prometheus-select-metrics.png)

### Query OpenSearch OTEL metrics
- Select the `ss4o_metrics-*-*` based index to view the OTEL metrics stored in OpenSearch:
![metrics-analytics-opensearch-otel-metrics.png](img%2Fmetrics-analytics-opensearch-otel-metrics.png)
![metrics-analytics-opensearch-otel-metrics-select-metrics.png](img%2Fmetrics-analytics-opensearch-otel-metrics-select-metrics.png)

## Discover - Log Exploration
- [Discover](http://localhost:5601/app/data-explorer/discover) the OTEL logs stored inside OpenSearch
![logs-discovery-otel.png](img%2Flogs-discovery-otel.png)
