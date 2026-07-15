from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA = BASE_DIR / "data" / "raw"
PROCESSED_DATA=BASE_DIR / "data" / "processed"
SUPPORTING_DATA = BASE_DIR / "data" / "supporting_datasets"

DATASETS = {
    "analysis": {
        "path": RAW_DATA / "analysis.xlsx",
        "header": 1,
    },
    "balancesheet": {
        "path": RAW_DATA / "balancesheet.xlsx",
        "header": 1,
    },
    "cashflow": {
        "path": RAW_DATA / "cashflow.xlsx",
        "header": 1,
    },
    "companies": {
        "path": RAW_DATA / "companies.xlsx",
        "header": 1,
    },
    "documents": {
        "path": RAW_DATA / "documents.xlsx",
        "header": 1,
    },
    "profitandloss": {
        "path": RAW_DATA / "profitandloss.xlsx",
        "header": 1,
    },
    "prosandcons": {
        "path": RAW_DATA / "prosandcons.xlsx",
        "header": 1,
    },
    "financial_ratios": {
        "path": SUPPORTING_DATA / "financial_ratios.xlsx",
        "header": 0,
    },
     "peer_groups": {
        "path": SUPPORTING_DATA / "peer_groups.xlsx",
        "header": 0,
    },
     "market_cap": {
        "path": SUPPORTING_DATA / "market_cap.xlsx",
        "header": 0,
    },
     "sectors": {
        "path": SUPPORTING_DATA / "sectors.xlsx",
        "header": 0,
    },
     "stock_prices": {
        "path": SUPPORTING_DATA / "stock_prices.xlsx",
        "header": 0,
    }
}
