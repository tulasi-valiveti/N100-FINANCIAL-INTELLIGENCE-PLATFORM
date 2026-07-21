import pandas as pd
from pathlib import Path
def free_cash_flow(operating_activity,investing_activity):
    if operating_activity is None or investing_activity  is None:
        return None
    return operating_activity+investing_activity

def cfo_quality_score(operating_activity,net_profit):
    if net_profit==0:
        return None
    return operating_activity/net_profit

def cfo_average(company_df):
    
    
        company_df=company_df.sort_values('year', ascending=False,).head(5)
        ratios=[]

        for _,row in company_df.iterrows():
            ratio=cfo_quality_score(row['operating_activity'],row['net_profit'])
            if ratio is not None:
                ratios.append(ratio) 
            if len(ratios)==0:
                return None,None
            
            avg=sum(ratios)/len(ratios)

            if avg >1.0:
                quality="HIGH QUALITY"
            elif avg>=0.5:
                quality="MODERATE"
            else:
                quality="ACCRUAL RISK"
        return avg,quality
            

def capex_intensity(investing_activity, sales):
    if sales == 0:
        return None, None

    intensity = abs(investing_activity) / sales * 100

    if intensity < 3:
        category = "Asset Light"

    elif intensity <= 8:
        category = "Moderate"

    else:
        category = "Capital Intensive"

    return intensity, category
    
def fcf_conversion_rate(operating_activity,investing_activity,operating_Profit):
    if operating_Profit==0:
        return None
    fcf = free_cash_flow(operating_activity, investing_activity)
    return (fcf / operating_Profit) * 100

def capital_allocation_pattern(
    operating_activity,
    investing_activity,
    financing_activity,
    cfo_quality=None
):

    cfo = "+" if operating_activity >= 0 else "-"
    cfi = "+" if investing_activity >= 0 else "-"
    cff = "+" if financing_activity >= 0 else "-"

    pattern = (cfo, cfi, cff)

    if pattern == ("+", "-", "-"):
        if cfo_quality is not None and cfo_quality > 1:
            return "Shareholder Returns"
        return "Reinvestor"

    elif pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    elif pattern == ("-", "+", "+"):
        return "Distress Signal"

    elif pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    elif pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    elif pattern == ("+", "-", "+"):
        return "Mixed"

    return "Other"



#accessing files
import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")
query = """
SELECT
    c.company_id,
    c.year,
    c.operating_activity,
    c.investing_activity,
    c.financing_activity,
    p.sales,
    p.net_profit,
    p.operating_profit

FROM cashflow c
INNER JOIN profitandloss p
ON c.company_id = p.company_id
AND c.year = p.year
"""
merged_df = pd.read_sql_query(query, conn)

conn.close()

###calling functions

def calculate_cashflow_metrics(df):

    df = df.copy()

    # Row-wise calculations
    df["free_cash_flow"] = df.apply(
        lambda row: free_cash_flow(
            row["operating_activity"],
            row["investing_activity"]
        ),
        axis=1
    )

    capex = df.apply(
        lambda row: capex_intensity(
            row["investing_activity"],
            row["sales"]
        ),
        axis=1
    )

    df["capex_intensity"] = capex.apply(lambda x: x[0])
    df["capex_category"] = capex.apply(lambda x: x[1])

    df["fcf_conversion_rate"] = df.apply(
        lambda row: fcf_conversion_rate(
            row["operating_activity"],
            row['investing_activity'],
            row["operating_profit"]
        ),
        axis=1
    )

    # ---------- CFO Average (latest 5 years of each company) ----------

    cfo_results = {}

    for company_id, company_df in df.groupby("company_id"):

        avg, quality = cfo_average(company_df)

        cfo_results[company_id] = (avg, quality)

    df["cfo_quality_score"] = df["company_id"].map(
        lambda x: cfo_results[x][0]
    )

    df["cfo_quality"] = df["company_id"].map(
        lambda x: cfo_results[x][1]
    )


    df["cfo_pat_ratio"] = df.apply(
    lambda row: cfo_quality_score(
        row["operating_activity"],
        row["net_profit"]
    ),
    axis=1
)

    # ---------- Capital Allocation ----------

    df["capital_allocation"] = df.apply(
        lambda row: capital_allocation_pattern(
            row["operating_activity"],
            row["investing_activity"],
            row["financing_activity"],
            row["cfo_pat_ratio"]
        ),
        axis=1
    )

    return df


capital= calculate_cashflow_metrics(merged_df)
capital_output = capital[
    [
        "company_id",
        "year",
        "free_cash_flow",
        "cfo_pat_ratio",
        "cfo_quality_score",
        "cfo_quality",
        "capex_intensity",
        "capex_category",
        "fcf_conversion_rate",
        "capital_allocation",
    ]
]
capital_output = capital_output.round(2)
capital_output.to_csv(
    "reports/capital_allocation.csv",
    index=False
)

print(capital_output.head())