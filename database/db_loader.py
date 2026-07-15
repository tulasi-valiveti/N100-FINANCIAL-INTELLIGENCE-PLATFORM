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
    
    datasets = {}
    for table, config in DATASETS.items():
        datasets[table] = pd.read_excel(
            config["path"],
            header=config["header"]
        )
    
    conn = create_database(
        "database/nifty100.db",
        "database/schema.sql"
    )
    

    load_all_tables(conn, datasets)
    
    conn.close()

    print("Database loaded successfully.")


if __name__ == "__main__":
    main()