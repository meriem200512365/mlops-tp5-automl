"""Call a local MLflow model endpoint and report request latency."""
import statistics
import sys
import time

import requests

PORT = sys.argv[1] if len(sys.argv) > 1 else "8100"
URL = f"http://127.0.0.1:{PORT}/invocations"
BODY = {"dataframe_records": [{"montant": 8500.0, "anciennete": 3,
                               "freq_24h": 9, "nuit": 1}]}

response = requests.post(URL, json=BODY, timeout=10)
response.raise_for_status()
print("reponse :", response.status_code, response.json())
for _ in range(10):
    requests.post(URL, json=BODY, timeout=10).raise_for_status()
latencies = []
for _ in range(200):
    start = time.perf_counter()
    requests.post(URL, json=BODY, timeout=10).raise_for_status()
    latencies.append((time.perf_counter() - start) * 1000)
p95 = sorted(latencies)[int(0.95 * len(latencies)) - 1]
print(f"port {PORT} | mediane : {statistics.median(latencies):.1f} ms | p95 : {p95:.1f} ms")
