import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import statistics
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

ENDPOINTS = [
    ("/api/v1/listings", "List Active Listings"),
    ("/api/v1/prices/daily", "Daily Market Prices"),
    ("/api/v1/meta/crops", "Crop Taxonomy"),
    ("/api/v1/meta/regions", "Regions & Districts"),
]

REQUESTS_PER_ENDPOINT = 100


def run_benchmark():
    print("=" * 65)
    print("🚀 HosilBozor API Yuklama va Tezlik Sinovi (Load & Latency Benchmark)")
    print(f"📊 Har bir endpoint uchun so'rovlar soni: {REQUESTS_PER_ENDPOINT}")
    print("=" * 65)

    all_passed = True

    for path, name in ENDPOINTS:
        latencies = []
        for _ in range(REQUESTS_PER_ENDPOINT):
            start = time.perf_counter()
            resp = client.get(path)
            duration_ms = (time.perf_counter() - start) * 1000.0
            if resp.status_code == 200:
                latencies.append(duration_ms)

        if not latencies:
            print(f"❌ {name} ({path}): Barcha so'rovlar xatolik bilan tugadi!")
            all_passed = False
            continue

        latencies.sort()
        p50 = statistics.median(latencies)
        p95 = latencies[int(len(latencies) * 0.95)]
        p99 = latencies[int(len(latencies) * 0.99)]
        avg = statistics.mean(latencies)

        target_met = p95 < 300.0
        status_mark = "✅" if target_met else "⚠️"
        if not target_met:
            all_passed = False

        print(f"\n{status_mark} {name}: {path}")
        print(f"   O'rtacha (avg):  {avg:.2f} ms")
        print(f"   Mediana (p50):   {p50:.2f} ms")
        print(f"   95-persentil (p95): {p95:.2f} ms  (Talab: < 300 ms)")
        print(f"   99-persentil (p99): {p99:.2f} ms")

    print("\n" + "=" * 65)
    if all_passed:
        print("🎉 BARChA ENDPOINTLAR p95 < 300 ms TALABINI TO'LIQ BAJARDi!")
    else:
        print("⚠️ Ayrim endpointlar 300 ms me'yoridan oshdi.")
    print("=" * 65)


if __name__ == "__main__":
    run_benchmark()
