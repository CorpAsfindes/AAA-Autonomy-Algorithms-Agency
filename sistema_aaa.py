# AAA — Autonomy, Algorithms & Agency
# Technical Framework for Digital Sovereignty
# Developed by: Corporación ASFINDES / Vita'e Plena
# Medellin, Colombia - 2026

import json

def get_recommendations(flags):
    """Generates actionable steps based on detected risks."""
    rec_map = {
        "LOW_INFRASTRUCTURE_CONTROL": "Implement local NAS storage and migrate to Nextcloud for data ownership.",
        "ALGORITHMIC_OPACITY": "Deploy algorithmic literacy workshops and use privacy-focused tools like Signal.",
        "POLITICAL_DISENFRANCHISEMENT": "Establish digital governance protocols to restore community decision-making power."
    }
    return [rec_map[flag] for flag in flags]

def run_aaa_diagnostic(community_data):
    results = []
    critical_threshold = 9.0
    
    for org in community_data:
        flags = []
        if org['autonomy'] < critical_threshold: flags.append("LOW_INFRASTRUCTURE_CONTROL")
        if org['algorithms'] < critical_threshold: flags.append("ALGORITHMIC_OPACITY")
        if org['agency'] < critical_threshold: flags.append("POLITICAL_DISENFRANCHISEMENT")
        
        composite_score = round((org['autonomy'] + org['algorithms'] + org['agency']) / 3, 2)
        
        entry = {
            "org_id": org['name'].lower().replace(" ", "_"),
            "name": org['name'],
            "metrics": {
                "autonomy": org['autonomy'],
                "algorithms": org['algorithms'],
                "agency": org['agency']
            },
            "analysis": {
                "composite_score": composite_score,
                "risk_level": "HIGH" if len(flags) > 1 else "MEDIUM" if flags else "LOW",
                "active_alerts": flags,
                "recommendations": get_recommendations(flags)
            }
        }
        results.append(entry)
    return results

# PILOT DATA: This preserves your original analysis of the Medellin JACs
pilot_data = [
    {"name": "Barrio Cristobal", "autonomy": 11.67, "algorithms": 9.0, "agency": 8.33},
    {"name": "La Pradera", "autonomy": 12.33, "algorithms": 9.0, "agency": 10.0},
    {"name": "Mirador de Calasanz", "autonomy": 9.67, "algorithms": 8.33, "agency": 7.67}
]

if __name__ == "__main__":
    diagnostics = run_aaa_diagnostic(pilot_data)
    print(json.dumps(diagnostics, indent=4))
