import sqlite3
import pandas as pd
from src.analytics.ratios import *

from src.validators.validation_logger import ValidationLogger


conn=sqlite3.connect("database/nifty100.db")

sectors = pd.read_sql("SELECT * FROM sectors", conn)

peer_groups = pd.read_sql("SELECT * FROM peer_groups", conn)

ratio_df = pd.read_sql("SELECT * FROM f_ratios", conn)
logger=ValidationLogger()

query="""SELECT
    p.company_id,
    p.year,
    p.sales,
    p.net_profit,
    p.operating_profit,
    p.opm_percentage,
    p.other_income,
    p.interest,
    b.equity_capital,
    b.total_assets,
    b.reserves,
    b.borrowings,
    b.investments,
    s.broad_sector
FROM profitandloss p
JOIN balancesheet b
    ON p.company_id=b.company_id
    AND p.year=b.year
LEFT JOIN sectors s
    ON p.company_id=s.company_id;"""
      
df=pd.read_sql(query,conn)
results=[]

for _, row in df.iterrows():
    npm=net_profit_margin(
        row['net_profit'],row['sales']
    )

    opm=operating_profit_ratio(
        row['operating_profit'],row['sales'],row['opm_percentage'],logger,row['company_id'],row['year']
    )
    

    roe=return_on_equity(
        row['net_profit'],row['equity_capital'],row['reserves'])

    roce=return_on_capital_employed(
        row['operating_profit'],row['equity_capital'],row['reserves'],row['borrowings'])
    

    benchmark_roce = get_benchmark_roce(row['company_id'],
    sectors,
    peer_groups,
    ratio_df)


    passed = check_roce_benchmark(
    roce,
    row['broad_sector'],
    benchmark_roce,
)

    roa=return_on_assets(
        row['net_profit'],row['total_assets'])
    
    #day-10

    deb_equity=debt_to_equity(
        row['borrowings'],row['equity_capital'],row['reserves']
    )
     

    high_leverage_flag=check_high_leverage(deb_equity,row['broad_sector'])
    
    icr=interest_coverage_ratio(
        row['operating_profit'],row['other_income'],row['interest']
    )

    icr_label=get_icr_label(icr)

    icr_warning_flag=check_icr_warning(icr)

    net_dbt=net_debt(
        row['borrowings'],row['investments']
    )

    asset_turnover=asset_turn_over(row['sales'],row['total_assets'])
    
    results.append({
        "company_id":row['company_id'],
        "year":row['year'],
        "net_profit_margin":f"{npm:.3f}"if npm is not None else None,
        "operational_profit_margin":f"{opm:.3f}"if opm is not None else None,
        "returns_on_equity":f"{roe:.3f}"if roe is not None else None,
        "returns_on_capital_employment":f"{roce:.3f}"if roce is not None else None,
        "returns_on_assets":f"{roa:.3f}"if roa is not None else None,
        "debt_to_equity":f"{deb_equity:.3f}"if deb_equity is not None else None,
        "high_leverage_flag":high_leverage_flag,
        "interest_coverage_ratio":f"{icr:.3f}"if icr is not None else None,
        "icr_label":icr_label,
        "icr_warning_flag":icr_warning_flag,
        "net_debt":f"{net_dbt:.3f}"if net_dbt is not None else None,
        "asset_turn_over":f"{asset_turnover:.3f}"if asset_turnover is not None else None
    })

ratios_df=pd.DataFrame(results)

ratios_df.to_csv("reports/f_ratios.csv",index=False)
    
df_log=pd.DataFrame(logger.records)

df_log.to_csv("src/analytics/opm_mismatch.csv",index=False)

ratios_df.to_sql("f_ratios",
                 conn,
                 if_exists='replace',
                 index=False)

print("successfully calculated ratios")
conn.close()