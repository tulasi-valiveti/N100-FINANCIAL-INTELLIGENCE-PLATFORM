import re
from pathlib import Path

import pandas as pd
from config.loader_config import DATASETS


def normalize_year(value):
    """
    Normalize year/month values to YYYY-MM.

    Examples:
        Mar-23        -> 2023-03
        Mar 23        -> 2023-03
        March-2023    -> 2023-03
        MAR 2023      -> 2023-03
        2023          -> 2023-03
        2,023         -> 2023-03
        2023.0        -> 2023-03
        FY23          -> 2023-03
        FY2023        -> 2023-03
        Dec-22        -> 2022-12
        Jun-23        -> 2023-06
        2023-03       -> 2023-03

    Raises:
        ValueError if the value cannot be parsed.
    """

    if pd.isna(value):
        raise ValueError("Missing year")

    value = str(value).strip()

    # Remove commas (2,023 -> 2023)
    value = value.replace(",", "")

    # Collapse multiple spaces
    value = re.sub(r"\s+", " ", value)

    # Already normalized
    if re.fullmatch(r"\d{4}-\d{2}", value):
        return value

    # Plain year (2023 or 2023.0)
    try:
        year = int(float(value))
        if 1900 <= year <= 2100:
            return f"{year}-03"
    except:
        pass

    # FY23 / FY2023
    match = re.fullmatch(r"FY\s*(\d{2,4})", value.upper())
    if match:
        year = match.group(1)
        if len(year) == 2:
            year = "20" + year
        return f"{year}-03"

    # Month-Year formats
    formats = [
        "%b-%y",     # Mar-23
        "%b %y",     # Mar 23
        "%b-%Y",     # Mar-2023
        "%b %Y",     # Mar 2023
        "%B-%Y",     # March-2023
        "%B %Y",     # March 2023
        "%Y/%m",     # 2023/03
        "%m/%Y",     # 03/2023
    ]

    for fmt in formats:
        try:
            dt = pd.to_datetime(value, format=fmt)
            return dt.strftime("%Y-%m")
        except:
            pass

    # Final automatic parsing
    try:
        dt = pd.to_datetime(value)
        return dt.strftime("%Y-%m")
    except:
        return None
    

def normalize_ticker(value):
    """
    Normalize stock ticker symbols.

    Examples
    --------
    tcs -> TCS
    TCS.NS -> TCS
    reliance.ns -> RELIANCE
    hdfc bank -> HDFCBANK
    icici-bank -> ICICIBANK
    """

    # Handle missing values
    if pd.isna(value):
        return None

    ticker = str(value).strip().upper()

    # Remove NSE/BSE suffixes
    ticker = re.sub(r"\.(NS|BO)$", "", ticker)

    # Remove spaces, hyphens and underscores
    ticker = re.sub(r"[\s\-_]", "", ticker)
    ticker = ticker.replace("-EQ", "")
    ticker = ticker.replace(" EQ", "")

    return ticker


#code to apply above functions for any dataset

def preprocess_dataset(df):
    """
    Automatically normalizes common columns.
    """

    for col in df.columns:

        name = str(col).lower()

        if "year" in name:
            df[col] = df[col].apply(normalize_year)

        if "company_id" in name :
            df[col] = df[col].apply(normalize_ticker)

    return df

#load dataset
def load_dataset(name: str) -> pd.DataFrame:
    """
    Loads one Excel dataset.

    Parameters
    ----------
    name : str
        Dataset name from DATASETS dictionary.

    Returns
    -------
    pandas.DataFrame
    """

    if name not in DATASETS:
        raise ValueError(f"{name} not found.")

    config = DATASETS[name]
    path=config["path"]
    header=config.get("header",0)

    if not Path(path).exists():
        raise FileNotFoundError(path)

    df = pd.read_excel(path,header=header)     # <-- important
    df=preprocess_dataset(df)
    return df

#load all datasets 
def load_all_datasets():
    datasets = {}

    for name in DATASETS:
        datasets[name] = load_dataset(name)

    return datasets
