from pathlib import Path
import pandas as pd

# Path to your raw data folder
DATA_DIR = Path("data/supporting_datasets")

# Read all Excel files
for file in DATA_DIR.glob("*.xlsx"):
    print("=" * 70)
    print(f"File: {file.name}")

    try:
        df = pd.read_excel(file)

        print(f"Rows: {len(df)}")
        print(f"Columns ({len(df.columns)}):")

        for col in df.columns:
            print(f"  - {col}")

    except Exception as e:
        print(f"Error reading {file.name}: {e}")

    print()