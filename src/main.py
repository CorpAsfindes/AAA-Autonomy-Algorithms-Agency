import os
import json
import time
from src.data_loader import load_data
from src.metrics import calculate_aaa_metrics
from src.ai_module import generate_diagnostic

OUTPUT_SEPARATOR = "=" * 60

def run_pipeline(input_path: str, delay: float = 2.0):
    print("AAA Diagnostic Engine")
    print(OUTPUT_SEPARATOR)
    df = load_data(input_path)
    metrics_list = calculate_aaa_metrics(df)
    print(f"Loaded {len(metrics_list)} organizations.")
    print(OUTPUT_SEPARATOR)
    results = []
    for i, metrics in enumerate(metrics_list):
        print(f"\n[{i+1}/{len(metrics_list)}] {metrics.organization}")
        print(f"  Autonomy={metrics.autonomy} | Algorithm={metrics.algorithm} | Agency={metrics.agency}")
        print(f"  Risk: {metrics.risk_level} | Flags: {metrics.risk_flags}")
        print(f"  Weakest: {metrics.lowest_dimension}")
        print("  Generating AI diagnostic...")
        diagnostic = generate_diagnostic(metrics)
        entry = metrics.to_dict()
        entry["diagnostic"] = diagnostic
        results.append(entry)
        print(diagnostic)
        print(OUTPUT_SEPARATOR)
        if i < len(metrics_list) - 1:
            time.sleep(delay)
    os.makedirs("salida", exist_ok=True)
    output_path = "salida/results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved to {output_path}")

if __name__ == "__main__":
    run_pipeline("data/AAA_datos_piloto_Medellin_2026.csv")
