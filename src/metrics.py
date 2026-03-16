from dataclasses import dataclass, field
from typing import List
import pandas as pd

THRESHOLDS = {"Autonomía_AAA": 8.0, "Algoritmo_AAA": 8.0, "Agencia_AAA": 8.0}

@dataclass
class AAAMetrics:
    organization: str
    autonomy: float
    algorithm: float
    agency: float
    risk_flags: List[str] = field(default_factory=list)

    @property
    def lowest_dimension(self):
        scores = {"Autonomy": self.autonomy, "Algorithm": self.algorithm, "Agency": self.agency}
        return min(scores, key=scores.get)

    @property
    def risk_level(self):
        n = len(self.risk_flags)
        if n == 0: return "low"
        if n == 1: return "medium"
        return "high"

    def to_dict(self):
        return {
            "organization": self.organization,
            "scores": {
                "autonomy": round(self.autonomy, 2),
                "algorithm": round(self.algorithm, 2),
                "agency": round(self.agency, 2)
            },
            "lowest_dimension": self.lowest_dimension,
            "risk_level": self.risk_level,
            "risk_flags": self.risk_flags,
        }

def calculate_aaa_metrics(df: pd.DataFrame):
    grouped = df.groupby("Nombre de la organización").mean(numeric_only=True)
    result = []
    for org, row in grouped.iterrows():
        flags = []
        if row["Agencia_AAA"] < THRESHOLDS["Agencia_AAA"]: flags.append("low_agency")
        if row["Autonomía_AAA"] < THRESHOLDS["Autonomía_AAA"]: flags.append("low_autonomy")
        if row["Algoritmo_AAA"] < THRESHOLDS["Algoritmo_AAA"]: flags.append("low_algorithm")
        result.append(AAAMetrics(
            organization=org,
            autonomy=round(float(row["Autonomía_AAA"]), 2),
            algorithm=round(float(row["Algoritmo_AAA"]), 2),
            agency=round(float(row["Agencia_AAA"]), 2),
            risk_flags=flags,
        ))
    return result
