import pandas as pd

REQUIRED_COLUMNS = ["Nombre de la organización", "Autonomía_AAA", "Algoritmo_AAA", "Agencia_AAA"]

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
    df.columns = df.columns.str.strip().str.replace("\xa0", " ")
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}\n"
            f"Available columns: {list(df.columns)}"
        )
    return df
