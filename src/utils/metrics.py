from prometheus_client import Counter, Histogram, start_http_server, REGISTRY

def unregister_metric(name):
    """
    Prevents 'Duplicated timeseries' error when reloading the module.
    """
    for collector in list(REGISTRY._collector_to_names):
        if name in REGISTRY._collector_to_names[collector]:
            REGISTRY.unregister(collector)
            break

# Unregister existing metrics to allow reload
unregister_metric('research_agent_search_queries_total')
unregister_metric('research_agent_llm_tokens_total')
unregister_metric('research_agent_request_latency_seconds')

# Metrics
SEARCH_QUERIES = Counter('research_agent_search_queries_total', 'Total search queries executed')
LLM_TOKENS = Counter('research_agent_llm_tokens_total', 'Total LLM tokens used (estimated)')
REQUEST_LATENCY = Histogram('research_agent_request_latency_seconds', 'Request latency in seconds')

def start_metrics_server(port=8000):
    """
    Starts the Prometheus metrics server.
    """
    try:
        start_http_server(port)
        print(f"Metrics server executed on port {port}") 
    except Exception as e:
        print(f"Could not start metrics server (might be already running): {e}")
