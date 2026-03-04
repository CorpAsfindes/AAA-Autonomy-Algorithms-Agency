import pytest
from src.metrics import AAAMetrics


# ─── lowest_dimension ───────────────────────────────────────

def test_lowest_dimension_agency():
    m = AAAMetrics("Test Org", autonomy=11.0, algorithm=9.0, agency=7.0)
    assert m.lowest_dimension == "Agency"

def test_lowest_dimension_autonomy():
    m = AAAMetrics("Test Org", autonomy=5.0, algorithm=9.0, agency=8.0)
    assert m.lowest_dimension == "Autonomy"

def test_lowest_dimension_algorithm():
    m = AAAMetrics("Test Org", autonomy=10.0, algorithm=4.0, agency=8.0)
    assert m.lowest_dimension == "Algorithm"


# ─── risk_level ─────────────────────────────────────────────

def test_risk_level_low():
    m = AAAMetrics("Test Org", autonomy=15.0, algorithm=14.0, agency=13.0)
    assert m.risk_level == "low"

def test_risk_level_medium():
    m = AAAMetrics("Test Org", autonomy=5.0, algorithm=12.0, agency=12.0,
                   risk_flags=["low_autonomy"])
    assert m.risk_level == "medium"

def test_risk_level_high():
    m = AAAMetrics("Test Org", autonomy=5.0, algorithm=5.0, agency=5.0,
                   risk_flags=["low_autonomy", "low_algorithm", "low_agency"])
    assert m.risk_level == "high"


# ─── to_dict() ──────────────────────────────────────────────

def test_to_dict_keys():
    m = AAAMetrics("Test Org", autonomy=10.0, algorithm=11.0, agency=9.0)
    d = m.to_dict()
    assert set(d.keys()) == {"organization", "scores", "lowest_dimension", "risk_level", "risk_flags"}

def test_to_dict_scores_rounded():
    m = AAAMetrics("Test Org", autonomy=10.666, algorithm=11.333, agency=9.111)
    d = m.to_dict()
    assert d["scores"]["autonomy"] == 10.67
    assert d["scores"]["algorithm"] == 11.33
    assert d["scores"]["agency"] == 9.11

def test_to_dict_organization_name():
    m = AAAMetrics("JAC Barrio Cristobal", autonomy=11.67, algorithm=9.0, agency=8.33)
    d = m.to_dict()
    assert d["organization"] == "JAC Barrio Cristobal"

def test_to_dict_lowest_matches_scores():
    m = AAAMetrics("Test Org", autonomy=11.0, algorithm=9.0, agency=7.0)
    d = m.to_dict()
    assert d["lowest_dimension"] == "Agency"
    assert d["scores"]["agency"] == 7.0
