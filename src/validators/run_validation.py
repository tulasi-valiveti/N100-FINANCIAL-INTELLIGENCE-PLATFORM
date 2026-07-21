"""
run_validation.py

Runs all Data Quality (DQ) rules.

If any CRITICAL rule fails:
    -> Stop ETL

Otherwise:
    -> Continue to database loading
"""

import sys


from src.ETL.loader import load_dataset
from config.loader_config import DATASETS

from src.validators.validation_logger import ValidationLogger

from src.validators.dq_rules import (

    dq01_company_pk,
    dq02_annual_pk,
    dq03_fk_integrity,
    dq04_balance_sheet,
    dq05_opm,
    dq06_sales,
    dq07_year,
    dq08_company_id,
    dq09_net_cash_check,
    dq10_fixed_assets,
    dq11_tax_percentage,
    dq12_dividend_payout,
    dq13_document_urls,
    dq14_eps_sign,
    dq15_balance_sheet,
    dq16_company_history

)


def main():

    print("\nLoading datasets...\n")

    datasets = {}

    for name in DATASETS:

        datasets[name] = load_dataset(name)

        print(f"{name} loaded")
    # Standardize the documents year column
    datasets["documents"] = datasets["documents"].rename(columns={"Year": "year"})
    

    logger = ValidationLogger()

    print("\nRunning Data Quality Rules...\n")

    # -------------------------------------------------
    # DQ-01 to DQ-08
    # -------------------------------------------------

    datasets["companies"] = dq01_company_pk(
        datasets["companies"],
        logger
    )
    

    datasets["profitandloss"]=dq02_annual_pk(
        datasets["profitandloss"],"profitandloss",
        logger
    )
    datasets["balancesheet"]=dq02_annual_pk(
        datasets["balancesheet"],"balance_sheet",
        logger
    )
    datasets["cashflow"]=dq02_annual_pk(
        datasets["cashflow"],"cashflow",
        logger
    )

    for table in datasets:
     datasets[table] = dq08_company_id(
        datasets[table],
        table,
        logger
    )
 
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

    datasets["balancesheet"]=dq04_balance_sheet(
        datasets["balancesheet"],
        logger
    )

    datasets["profitandloss"] = dq05_opm(
        datasets["profitandloss"],
        logger
    )
    
    
    datasets["profitandloss"] = dq06_sales(
        datasets["profitandloss"],
        logger
    )
    child_table = [
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "market_cap",
    "documents",
    ]
    for table in child_table:
     datasets[table] = dq07_year(
        datasets[table],
        table,
        logger
    )
    
    
    

    # -------------------------------------------------
    # DQ-09 to DQ-16
    # -------------------------------------------------

    datasets["cashflow"] = dq09_net_cash_check(
        datasets["cashflow"],
        logger
    )

    datasets["balancesheet"] = dq10_fixed_assets(
        datasets["balancesheet"],
        logger
    )

    datasets["profitandloss"] = dq11_tax_percentage(
        datasets["profitandloss"],
        logger
    )

    datasets["profitandloss"] = dq12_dividend_payout(
        datasets["profitandloss"],
        logger
    )

    datasets["documents"] = dq13_document_urls(
        datasets["documents"],
        logger
    )

    datasets["profitandloss"] = dq14_eps_sign(
        datasets["profitandloss"],
        logger
    )

    datasets["balancesheet"] = dq15_balance_sheet(
        datasets["balancesheet"],
        logger
    )

    datasets["profitandloss"] = dq16_company_history(
        datasets["profitandloss"],"profitandloss",
        logger
    )
    datasets["balancesheet"] = dq16_company_history(
        datasets["balancesheet"],"balancesheet",
        logger
    )
    datasets["cashflow"] = dq16_company_history(
        datasets["cashflow"],"cashflow",
        logger
    )
    # -------------------------------------------------
    # Save Validation Report
    # -------------------------------------------------

    logger.save(
        "reports/validation_failures.csv"
    )

    print("\nValidation report generated.")

    # -------------------------------------------------
    # Check Critical Errors
    # -------------------------------------------------
    

    critical_errors = logger.get_critical_errors()
    if critical_errors:

        print("\nCRITICAL ERRORS FOUND")

        print( f"Total Critical Errors : {len(critical_errors)}")

        print("ETL Process Halted.")
        
        sys.exit(1)

    print("\nNo Critical Errors Found")

    print("Validation Successful")

    print("ETL Can Continue")
    


if __name__ == "__main__":

    main()