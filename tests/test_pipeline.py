import pytest
from src.data_loader import load_data
from src.metrics import calculate_aaa_metrics, AAAMetrics


def test_load_data_success():
    df = load_data("data/sample_input.csv")
    assert len(df) == 3
    assert "Organizacion" in df.columns


def test_load_data_missing_file():
    with pytest.raises(FileNotFoundError):
        load_data("nonexistent.csv")


def test_load_data_missing_columns(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("col1,col2\n1,2\n")
    with pytest.raises(ValueError):
        load_data(str(bad_csv))


def test_calculate_metrics():
    df = load_data("data/sample_input.csv")
    metrics = calculate_aaa_metrics(df)
    assert len(metrics) == 3
    assert all(isinstance(m, AAAMetrics) for m in metrics)


def test_lowest_dimension():
    m = AAAMetrics("Test Org", autonomy=11.0, algorithm=9.0, agency=7.0)
    assert m.lowest_dimension == "Agency"


def test_risk_level_high():
    m = AAAMetrics(
        "Test Org",
        autonomy=5.0,
        algorithm=5.0,
        agency=5.0,
        risk_flags=["low_agency", "low_autonomy", "low_algorithm"],
    )
    assert m.risk_level == "high"


def test_risk_level_low():
    m = AAAMetrics("Test Org", autonomy=15.0, algorithm=14.0, agency=13.0)
    assert m.risk_level == "low"


def test_to_dict_structure():
    m = AAAMetrics("Test Org", autonomy=10.0, algorithm=11.0, agency=9.0)
    d = m.to_dict()
    assert "organization" in d
    assert "scores" in d
    assert "lowest_dimension" in d
    assert "risk_level" in d
