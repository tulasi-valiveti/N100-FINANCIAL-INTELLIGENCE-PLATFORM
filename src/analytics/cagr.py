import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parents[2]
profit_df=pd.read_excel(
    BASE_DIR / "data" / "processed" /"profitandloss.xlsx"
)


def calculate_cagr(start,end,years):
    if start==0:
        return None,"ZERO BASE"
    if start >0 and end <0:
        return None,"DECLINE_TO_LOSS"
    if start <0 and end>0:
        return None,"TURNAROUND"
    if start<0 and end <0:
        return None,'BOTH_NEGATIVE'
    cagr=((end/start)**(1/years)-1)*100
    return round(cagr,3) ,'COMPUTED_NORMALLY'

#revenue_cagr-uses sales column as revenue
"""def revenue_cagr(company_df,years):
    company_df['year']=pd.to_datetime(company_df['year'])
    company_df=company_df.sort_values('year')
    if len(company_df) < years+1 :
        return None
    start=company_df.iloc[-(years+1)]['sales']
    end=company_df.iloc[-1]['sales']
    return calculate_cagr(start,end,years)"""

#pat_cagr-uses net_profit column as pat values
"""def pat_cagr(company_df,years):
    company_df=company_df.sort_values('year')
    if len(company_df) < years + 1:
        return None
    start=company_df.iloc[-(years+1)]['net_profit']
    end=company_df.iloc[-1]['net_profit']
    return calculate_cagr(start,end,years)"""

#eps_cagr-uses eps column as eps values
"""def eps_cagr(company_df,years):
    company_df=company_df.sort_values('year')
    if len(company_df) < years + 1:
        return None
    start=company_df.iloc[-(years+1)]['eps']
    end=company_df.iloc[-1]['eps']
    return calculate_cagr(start,end,years)"""

"""function used to take particular column 
for that specific function"""

def metric_cagr(df,column,years):
    df["year"] = pd.to_datetime(df["year"], format="%Y-%m")
    df=df.sort_values('year')

    latest=df.iloc[-1]
    latest_year=latest['year'].year

    start_year=latest_year-years
    start_row=df[df['year'].dt.year==start_year]

    if start_row.empty:
        return None,'INSUFFICIENT_DATA'
    
    start=start_row.iloc[0][column]
    end=latest[column]
    return calculate_cagr(start,end,years)

"""wrapper function - 
used for calling  above functions for 
3 different years of each function"""

def calculate_all_cagrs(df):

    
        revenue_cagr_3yr,rev3_flag=metric_cagr(df,'sales',3)
        revenue_cagr_5yr,rev5_flag=metric_cagr(df,'sales',5)
        revenue_cagr_10yr,rev10_flag=metric_cagr(df,'sales',10)

        pat_cagr_3yr,pat3_flag=metric_cagr(df,'net_profit',3)
        pat_cagr_5yr,pat5_flag=metric_cagr(df,'net_profit',5)
        pat_cagr_10yr,pat10_flag=metric_cagr(df,'net_profit',10)

        eps_cagr_3yr,eps3_flag=metric_cagr(df,'eps',3)
        eps_cagr_5yr,eps5_flag=metric_cagr(df,'eps',5)
        eps_cagr_10yr,eps10_flag=metric_cagr(df,'eps',10)


        return{
        'revenue_cagr_3yr':revenue_cagr_3yr,
        'rev3yr_flag':rev3_flag,

        'revenue_cagr_5yr':revenue_cagr_5yr,
        'rev5yr_flag':rev5_flag,

        'revenue_cagr_10yr':revenue_cagr_10yr,
        'rev10yr_flag':rev10_flag,

        'pat_cagr_3yr':pat_cagr_3yr,
        'pat3yr_flag':pat3_flag,

        'pat_cagr_5yr':pat_cagr_5yr,
        'pat5yr_flag':pat5_flag,

        'pat_cagr_10yr':pat_cagr_10yr,
        'pat10yr_flag':pat10_flag,

        'eps_cagr_3yr':eps_cagr_3yr,
        'eps3yr_flag':eps3_flag,

        'eps_cagr_5yr':eps_cagr_5yr,
        'eps5yr_flag':eps5_flag,

        'eps_cagr_10yr':eps_cagr_10yr,
        'eps10yr_flag':eps10_flag
    }
    

results=[]
for company_id,company_df in profit_df.groupby('company_id'):
    metrics={'company_id':company_id}
    metrics.update(calculate_all_cagrs(company_df))
    results.append(metrics)

cagr_df=pd.DataFrame(results)
cagr_df.to_csv('reports/cagr_values.csv',index=False)
print(cagr_df.head())






    

    



