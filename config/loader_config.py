from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA = BASE_DIR / "data" / "raw"
SUPPORTING_DATA=BASE_DIR / "data" / "supporting_datasets"

DATASETS = {
    "analysis": RAW_DATA / "analysis.xlsx",
    "balancesheet": RAW_DATA / "balancesheet.xlsx",
    "cashflow": RAW_DATA / "cashflow.xlsx",
    "companies": RAW_DATA / "companies.xlsx",
    "documents": RAW_DATA / "documents.xlsx",
    "profitandloss": RAW_DATA / "profitandloss.xlsx",
    "prosandcons": RAW_DATA / "prosandcons.xlsx",
   
}