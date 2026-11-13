import json
import time
import urllib.request
from pathlib import Path


def query_endpoint(url: str, prompt: str, timeout: float = 30.0) -> str:
    payload = json.dumps({"prompt": prompt}).encode("utf-8")
    request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def run_suite(suite_path: str, endpoint: str) -> dict:
    suite = json.loads(Path(suite_path).read_text(encoding="utf-8"))
    results = {}
    for item in suite["tasks"]:
        started = time.time()
        answer = query_endpoint(endpoint, item["prompt"])
        results[item["id"]] = {"answer": answer, "latency": round(time.time() - started, 3)}
    return results


if __name__ == "__main__":
    print(run_suite("tasks.json", "http://localhost:8000/generate"))
