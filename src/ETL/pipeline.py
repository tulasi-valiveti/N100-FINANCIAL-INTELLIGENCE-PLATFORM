from pathlib import Path
from .loader import load_all_datasets
def main():
    datasets = load_all_datasets()

    for name, df in datasets.items():
        print(f"\n{name}")
        print(df.shape)
        print(df.head())


# Save processed datasets

    datasets = load_all_datasets()

    OUTPUT_DIR = Path("data/processed")
    

    for name, df in datasets.items():
        output_file = OUTPUT_DIR / f"{name}_processed.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Saved: {output_file}")

    print("All processed datasets saved successfully.")

if __name__ == "__main__":
    main()