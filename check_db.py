import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

query = """
SELECT company_id, year, COUNT(*)
FROM f_ratios
GROUP BY company_id, year
HAVING COUNT(*) > 1;
"""

print(pd.read_sql(query, conn))

conn.close()