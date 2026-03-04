data_loader.py que descargaste — o copia esto:
import pandas as pd

REQUIRED_COLUMNS = ["Organizacion", "Autonomia_AAA", "Algoritmo_AAA", "Agencia_AAA"]


def load_data(path: str) -> pd.DataFrame:
    """
    Loads and validates organizational data from a CSV file.

    Args:
        path: Path to the CSV input file.

    Returns:
        A cleaned DataFrame ready for processing.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        ValueError: If required columns are missing from the file.
    """
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {path}")

    # Strip whitespace and invisible characters from column names and values
    df.columns = df.columns.str.strip().str.replace("\xa0", " ")
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # Validate required columns are present
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )

    return df
