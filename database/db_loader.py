import sqlite3
import pandas as pd
from pathlib import Path
from config.loader_config import DATASETS

def create_database(db_path, schema_path):

    db_path = Path(db_path)

    # Delete old database if it exists
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")

    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()

    return conn

def load_table(conn, table_name, dataframe):

    dataframe.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )
def load_all_tables(conn, datasets):

    load_order = [
        "companies",
        "analysis",
        "sectors",
        "prosandcons",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
        "stock_prices",
        "documents",
        "peer_groups"
    ]

    for table in load_order:

        print(f"Loading {table}")

        load_table(conn, table, datasets[table])

    conn.commit()
    

def main():
    from src.ETL.loader import load_all_datasets
    from src.validators.validation_logger import ValidationLogger
    from src.validators.dq_rules import (
        dq01_company_pk,
        dq02_annual_pk,
        dq03_fk_integrity,
        dq07_year,
        dq08_company_id,
        dq09_net_cash_check,
        dq10_fixed_assets,
    )

    print("Loading and preprocessing datasets...")
    datasets = load_all_datasets()
    
    # Rename columns in documents to match the SQLite schema
    if "documents" in datasets:
        datasets["documents"] = datasets["documents"].rename(
            columns={"Year": "year", "Annual_Report": "annual_report"}
        )

    logger = ValidationLogger()

    print("Applying cleaning, deduplication, and validation rules (orphan filtering)...")
    
    # DQ-01: Company PK uniqueness
    datasets["companies"] = dq01_company_pk(datasets["companies"], logger)

    # DQ-02: Annual PK uniqueness
    datasets["profitandloss"] = dq02_annual_pk(datasets["profitandloss"], "profitandloss", logger)
    datasets["balancesheet"] = dq02_annual_pk(datasets["balancesheet"], "balancesheet", logger)
    datasets["cashflow"] = dq02_annual_pk(datasets["cashflow"], "cashflow", logger)

    # DQ-03: Foreign Key Integrity (removes orphan rows)
    child_tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
        "stock_prices",
        "analysis",
        "documents",
        "prosandcons",
        "sectors",
        "peer_groups"
    ]
    for table in child_tables:
        datasets[table] = dq03_fk_integrity(
            datasets[table],
            datasets["companies"],
            table,
            logger
        )

    # DQ-07: Year format validation and filtering
    child_year_tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap",
        "documents",
    ]
    for table in child_year_tables:
        datasets[table] = dq07_year(datasets[table], table, logger)

    # DQ-08: Company ID length and case standardization
    for table in datasets:
        datasets[table] = dq08_company_id(datasets[table], table, logger)

    # DQ-09: Cashflow validation and net cash flow correction
    datasets["cashflow"] = dq09_net_cash_check(datasets["cashflow"], logger)

    # DQ-10: Fixed assets negative correction
    datasets["balancesheet"] = dq10_fixed_assets(datasets["balancesheet"], logger)
    
    # Deduplicate all tables according to their primary key constraints
    print("Deduplicating datasets to satisfy database primary keys...")
    datasets["companies"] = datasets["companies"].drop_duplicates(subset=["id"], keep="last")
    datasets["profitandloss"] = datasets["profitandloss"].drop_duplicates(subset=["company_id", "year"], keep="last")
    datasets["balancesheet"] = datasets["balancesheet"].drop_duplicates(subset=["company_id", "year"], keep="last")
    datasets["cashflow"] = datasets["cashflow"].drop_duplicates(subset=["company_id", "year"], keep="last")
    datasets["financial_ratios"] = datasets["financial_ratios"].drop_duplicates(subset=["company_id", "year"], keep="last")
    datasets["market_cap"] = datasets["market_cap"].drop_duplicates(subset=["company_id", "year"], keep="last")
    datasets["documents"] = datasets["documents"].drop_duplicates(subset=["company_id", "year", "annual_report"], keep="last")
    datasets["peer_groups"] = datasets["peer_groups"].drop_duplicates(subset=["company_id", "peer_group_name"], keep="last")
    datasets["stock_prices"] = datasets["stock_prices"].drop_duplicates(subset=["company_id", "date"], keep="last")
    datasets["sectors"] = datasets["sectors"].drop_duplicates(subset=["company_id"], keep="last")
    datasets["prosandcons"] = datasets["prosandcons"].drop_duplicates(subset=["id"], keep="last")
    
    for table, df in datasets.items():
       df.to_excel(f"data/processed/{table}.xlsx", index=False)
    
    audit = []

    for table in DATASETS.keys():

        source = pd.read_excel(
        DATASETS[table]["path"],
        header=DATASETS[table]["header"])

        source_rows = len(source)
        loaded_rows = len(datasets[table])

        audit.append({
        "table_name": table,
        "source_rows": source_rows,
        "loaded_rows": loaded_rows,
        "rejected_rows": source_rows - loaded_rows,
        "status": "SUCCESS"
        })

    audit_df = pd.DataFrame(audit)

    audit_df.to_csv(
    "database/load_audit.csv",
    index=False)

    conn = create_database(
        "database/nifty100.db",
        "database/schema.sql"
    )
    
    load_all_tables(conn, datasets)

    conn.close()

    print("Database loaded successfully.")

if __name__ == "__main__":
    main()