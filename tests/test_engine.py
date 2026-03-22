import json
import sys
import os
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.main import run_pipeline

SAMPLE_CSV = (
    "Nombre de la organización,Autonomía_AAA,Algoritmo_AAA,Agencia_AAA\n"
    "JAC Test Org,11.0,9.0,7.0\n"
)


@pytest.fixture
def sample_csv(tmp_path):
    f = tmp_path / "test_input.csv"
    f.write_text(SAMPLE_CSV, encoding="utf-8")
    return str(f)


@pytest.fixture
def mock_gemini():
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Mock diagnostic output."}]}}]
    }
    return resp


def test_pipeline_produces_output_file(sample_csv, mock_gemini, tmp_path, monkeypatch):
    """run_pipeline writes a results.json file to the output/ directory."""
    monkeypatch.setenv("GOOGLE_API_KEY", "test_key")
    monkeypatch.chdir(tmp_path)
    with patch("src.ai_module.requests.post", return_value=mock_gemini):
        run_pipeline(sample_csv, delay=0)
    assert (tmp_path / "output" / "results.json").exists()


def test_pipeline_output_is_valid_json(sample_csv, mock_gemini, tmp_path, monkeypatch):
    """The output file is deserializable as a JSON list."""
    monkeypatch.setenv("GOOGLE_API_KEY", "test_key")
    monkeypatch.chdir(tmp_path)
    with patch("src.ai_module.requests.post", return_value=mock_gemini):
        run_pipeline(sample_csv, delay=0)
    with open(tmp_path / "output" / "results.json", encoding="utf-8") as f:
        results = json.load(f)
    assert isinstance(results, list)
    assert len(results) == 1


def test_pipeline_output_structure(sample_csv, mock_gemini, tmp_path, monkeypatch):
    """Each result contains the required fields with correct types."""
    monkeypatch.setenv("GOOGLE_API_KEY", "test_key")
    monkeypatch.chdir(tmp_path)
    with patch("src.ai_module.requests.post", return_value=mock_gemini):
        run_pipeline(sample_csv, delay=0)
    with open(tmp_path / "output" / "results.json", encoding="utf-8") as f:
        result = json.load(f)[0]
    assert set(result.keys()) == {
        "organization", "scores", "lowest_dimension", "risk_level", "risk_flags", "diagnostic"
    }
    assert result["organization"] == "JAC Test Org"
    assert result["lowest_dimension"] == "Agency"
    assert result["risk_level"] == "medium"
    assert "low_agency" in result["risk_flags"]
    assert result["diagnostic"] == "Mock diagnostic output."


def test_pipeline_scores_are_rounded(sample_csv, mock_gemini, tmp_path, monkeypatch):
    """Scores in output are rounded to 2 decimal places."""
    monkeypatch.setenv("GOOGLE_API_KEY", "test_key")
    monkeypatch.chdir(tmp_path)
    with patch("src.ai_module.requests.post", return_value=mock_gemini):
        run_pipeline(sample_csv, delay=0)
    with open(tmp_path / "output" / "results.json", encoding="utf-8") as f:
        scores = json.load(f)[0]["scores"]
    for val in scores.values():
        assert isinstance(val, float)
        assert round(val, 2) == val
