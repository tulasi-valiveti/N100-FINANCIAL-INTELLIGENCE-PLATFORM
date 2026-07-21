'''import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT company_id, year, COUNT(*)
FROM profitandloss
GROUP BY company_id, year
HAVING COUNT(*) ==1;
"""

print(pd.read_sql(query, conn))

conn.close()



import pandas as pd
df=pd.read_excel('data/raw/profitandloss.xlsx')
print(df[""].nunique())
print(df["company_id"].unique())

df1=pd.read_excel('data/processed/companies.xlsx')
print(df1["id"].nunique())
print(df1["id"].unique()) '''

from config.loader_config import DATASETS
from src.ETL.loader import load_dataset
def load_all_datasets():
    datasets = {}

    for name in DATASETS:
        datasets[name] = load_dataset(name)
        
    return datasets
