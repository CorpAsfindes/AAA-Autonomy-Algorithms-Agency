import pytest
import pandas as pd
from src.data_loader import load_data

VALID_CSV = (
    "Nombre de la organización,Autonomía_AAA,Algoritmo_AAA,Agencia_AAA\n"
    "JAC Barrio Cristobal,11.67,9.0,8.33\n"
    "JAC La Pradera,12.33,10.67,10.0\n"
)


def test_load_data_returns_dataframe(tmp_path):
    """load_data returns a DataFrame when given a valid CSV."""
    f = tmp_path / "valid.csv"
    f.write_text(VALID_CSV, encoding="utf-8")
    df = load_data(str(f))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


def test_load_data_missing_file():
    """load_data raises FileNotFoundError for a non-existent path."""
    with pytest.raises(FileNotFoundError):
        load_data("nonexistent_file.csv")


def test_load_data_missing_required_columns(tmp_path):
    """load_data raises ValueError listing which columns are absent."""
    bad_csv = "WrongColumn,Autonomía_AAA,Algoritmo_AAA,Agencia_AAA\nJAC Test,10,10,10\n"
    f = tmp_path / "bad.csv"
    f.write_text(bad_csv, encoding="utf-8")
    with pytest.raises(ValueError, match="Missing required columns"):
        load_data(str(f))


def test_load_data_strips_cell_whitespace(tmp_path):
    """load_data strips leading/trailing whitespace from string cells."""
    padded = (
        "Nombre de la organización,Autonomía_AAA,Algoritmo_AAA,Agencia_AAA\n"
        " JAC Test ,10.0,10.0,10.0\n"
    )
    f = tmp_path / "padded.csv"
    f.write_text(padded, encoding="utf-8")
    df = load_data(str(f))
    assert df["Nombre de la organización"].iloc[0] == "JAC Test"


def test_load_data_all_required_columns_present(tmp_path):
    """load_data accepts a file that has all required columns."""
    f = tmp_path / "valid.csv"
    f.write_text(VALID_CSV, encoding="utf-8")
    df = load_data(str(f))
    for col in ["Nombre de la organización", "Autonomía_AAA", "Algoritmo_AAA", "Agencia_AAA"]:
        assert col in df.columns
