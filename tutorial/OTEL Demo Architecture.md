# OTEL Astronomy Demo Application

The following diagram presents the OTEL Astronomy shop services architecture:

![](img/DemoServices.png)

### Trace Collectors
Monitoring data flow through the OpenTelemetry Collector is crucial for several reasons. Gaining a macro-level perspective on incoming data, such as sample counts and cardinality, is essential for comprehending the collector’s internal dynamics. However, when delving into the details, the interconnections can become complex. The Collector Data Flow Dashboard aims to demonstrate the capabilities of the OpenTelemetry demo application, offering a solid foundation for users to build upon. Collector Data Flow Dashboard provides valuable guidance on which metrics to monitor. Users can tailor their own dashboard variations by adding necessary metrics specific to their use cases, such as memory_delimiter processor or other data flow indicators. This demo dashboard serves as a starting point, enabling users to explore diverse usage scenarios and adapt the tool to their unique monitoring needs.

Data Flow Overview
The diagram below provides an overview of the system components, showcasing the configuration derived from the OpenTelemetry Collector (otelcol) configuration file utilized by the OpenTelemetry demo application. Additionally, it highlights the observability data (traces and metrics) flow within the system.

## Reference
- https://opentelemetry.io/docs/demo/architecture/
- https://opentelemetry.io/docs/demo/collector-data-flow-dashboard/
- https://opentelemetry.io/docs/demo/services/