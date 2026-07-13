header=1
import pandas as pd
from config.loader_config import DATASETS

for dataset_name, file_path in DATASETS.items():

    print("=" * 80)
    print(f"Dataset : {dataset_name}")
    print(f"File     : {file_path}")

    try:
        df = pd.read_excel(file_path,header=1)

        print(f"Rows     : {len(df)}")
        print(f"Columns  : {len(df.columns)}")

        for i, col in enumerate(df.columns, start=1):
            print(f"{i}. {col}")

    except Exception as e:
        print(f"Error: {e}")

    print()

    