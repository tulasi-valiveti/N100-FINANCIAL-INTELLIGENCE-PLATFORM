import re
import requests
import pandas as pd
import numpy as np
from src.validators.validation_logger import ValidationLogger

def dq01_company_pk(companies, logger):

    duplicates = companies[
        companies.duplicated(
            subset=["id"],
            keep=False
        )
    ]

    if duplicates.empty:
        return companies   # ✅ Return the original DataFrame

    for _, row in duplicates.iterrows():

        logger.log(
            "DQ-01",
            "companies",
            row["id"],
            "",
            "id",
            row["id"],
            "CRITICAL",
            "Duplicate Company ID"
        )

    return companies.drop_duplicates(
        subset=["id"],
        keep="last"
    )

def dq02_annual_pk(
    df,
    table_name,
    logger
):

    duplicates = df[
        df.duplicated(
            subset=["company_id", "year"],
            keep=False
        )
    ]

    for _, row in duplicates.iterrows():

        logger.log(
            "DQ-02",
            table_name,
            row["company_id"],
            "",
            "company_id,year",
            f"{row['company_id']} - {row['year']}",
            "CRITICAL",
            "Duplicate company/year"
        )

    return df.drop_duplicates(
        subset=["company_id", "year"],
        keep="last").reset_index(drop=True)

def dq03_fk_integrity(
    df,
    companies,
    table_name,
    logger
):

    valid_ids = set(companies["id"])

    invalid = df[
        ~df["company_id"].isin(valid_ids)
    ]

    for _, row in invalid.iterrows():

        logger.log(
            "DQ-03",
            table_name,
            row["company_id"],
            "",
            "company_id",
            row["company_id"],
            "CRITICAL",
            "Foreign key not found"
        )

    return df[df["company_id"].isin(valid_ids)].reset_index(drop=True)

def dq04_balance_sheet(
    balancesheet,
    logger
):

    diff = (
        (
            balancesheet["total_assets"]
            -
            balancesheet["total_liabilities"]
        ).abs()
        /
        balancesheet["total_assets"]
    )

    invalid = balancesheet[
        diff >= 0.01
    ]

    for _, row in invalid.iterrows():

        logger.log(
            "DQ-04",
            "balancesheet",
            row["id"],
            "",
            "total_assets",
            row["total_assets"],
            "WARNING",
            "Assets and liabilities mismatch"
        )

    return balancesheet

def dq05_opm(
    profitandloss,
    logger
):

    calculated = (
        profitandloss["operating_profit"]
        /
        profitandloss["sales"]
    ) * 100

    diff = (
        profitandloss["opm_percentage"]
        -
        calculated
    ).abs()

    invalid = profitandloss[
        diff >= 1
    ]

    for _, row in invalid.iterrows():

        logger.log(
            "DQ-05",
            "profitandloss",
            row["id"],
            "",
            "opm_percentage",
            row["opm_percentage"],
            "WARNING",
            "OPM mismatch"
        )

    return profitandloss

def dq06_sales(profitandloss, logger):

    invalid = profitandloss[
        profitandloss["sales"] <= 0
    ]

    for _, row in invalid.iterrows():

        logger.log(
            "DQ-06",
            "profitandloss",
            row["id"],
            "",
            "sales",
            row["sales"],
            "WARNING",
            "Sales must be positive"
        )

    return profitandloss


def dq07_year(
    df,
    table_name,
    logger
):

    pattern = r"^\d{4}-\d{2}$"

    invalid = df[
        ~df["year"]
        .astype(str)
        .str.match(pattern)
    ]

    for _, row in invalid.iterrows():

        logger.log(
            "DQ-07",
            table_name,
            row["id"],
            "",
            "year",
            row["year"],
            "CRITICAL",
            "Invalid year format"
        )

    return df[
        df["year"]
        .astype(str)
        .str.match(pattern)
    ]
def dq08_company_id(df, table_name, logger):

    if "company_id" in df.columns:
        col = "company_id"
    else:
        col = "id"

    df[col] = df[col].astype(str).str.strip().str.upper()

    invalid = df[
        (df[col].str.len() < 2) |
        (df[col].str.len() > 12)
    ]

    for _, row in invalid.iterrows():
        logger.log(
            "DQ-08",
            table_name,
            row[col],
            "",
            col,
            row[col],
            "WARNING",
            "Invalid Company ID format"
        )

    return df

def dq09_net_cash_check(
    cashflow,
    logger
):

    calculated = (
        cashflow["operating_activity"] +
        cashflow["investing_activity"] +
        cashflow["financing_activity"]
    )

    diff = (cashflow["net_cash_flow"] - calculated).abs()

    invalid = cashflow[
        diff > 10
    ]

    for _, row in invalid.iterrows():

        logger.log(
            "DQ-09",
            "cashflow",
            row["id"],
            "",
            "net_cash_flow",
            row["net_cash_flow"],
            "WARNING",
            "Net cash flow does not match CFO + CFI + CFF"
        )
        cashflow.loc[diff > 10,"net_cash_flow"] = calculated[diff > 10]

    return cashflow

def dq10_fixed_assets(
    balancesheet,
    logger
):

    invalid = balancesheet[
        balancesheet["fixed_assets"] < 0
    ]

    for _, row in invalid.iterrows():

        logger.log(
            "DQ-10",
            "balancesheet",
            row["id"],
            "",
            "fixed_assets",
            row["fixed_assets"],
            "WARNING",
            "Negative fixed assets"
        )

    balancesheet.loc[
        balancesheet["fixed_assets"] < 0,
        "fixed_assets"
    ] = 0

    return balancesheet

def dq11_tax_percentage(
    profitandloss,
    logger
):

    invalid = profitandloss[
        (profitandloss["tax_percentage"] < 0)
        |
        (profitandloss["tax_percentage"] > 60)
    ]

    for _, row in invalid.iterrows():

        logger.log(
            "DQ-11",
            "profitandloss",
            row["id"],
            "",
            "tax_percentage",
            row["tax_percentage"],
            "WARNING",
            "Tax percentage outside valid range"
        )

    return profitandloss

def dq12_dividend_payout(
    profitandloss,
    logger
):

    invalid = profitandloss[
        profitandloss["dividend_payout"] > 200
    ]

    for _, row in invalid.iterrows():

        logger.log(
            "DQ-12",
            "profitandloss",
            row["id"],
            "",
            "dividend_payout",
            row["dividend_payout"],
            "WARNING",
            "Dividend payout exceeds 200%"
        )

    return profitandloss


def dq13_document_urls(
    documents,
    logger
):

    for _, row in documents.iterrows():

        try:

            response = requests.head(
                row["Annual_Report"],
                allow_redirects=True,
                timeout=5
            )

            if response.status_code != 200:

                logger.log(
                    "DQ-13",
                    "documents",
                    row["id"],
                    "",
                    "Annual_Report",
                    row["Annual_Report"],
                    "WARNING",
                    f"URL returned {response.status_code}"
                )

        except Exception:

            logger.log(
                "DQ-13",
                "documents",
                row["id"],
                "",
                "Annual_Report",
                row["Annual_Report"],
                "WARNING",
                "URL not reachable"
            )

    return documents

def dq14_eps_sign(
    profitandloss,
    logger
):

    invalid = profitandloss[
        (profitandloss["net_profit"] > 0)
        &
        (profitandloss["eps"] <= 0)
    ]

    for _, row in invalid.iterrows():

        logger.log(
            "DQ-14",
            "profitandloss",
            row["id"],
            "",
            "eps",
            row["eps"],
            "WARNING",
            "Positive net profit with non-positive EPS"
        )

    return profitandloss

def dq15_balance_sheet(
    balancesheet,
    logger
):

    invalid = balancesheet[
        balancesheet["total_liabilities"] !=
        balancesheet["total_assets"]
    ]

    for _, row in invalid.iterrows():

        logger.log(
            "DQ-15",
            "balancesheet",
            row["id"],
            "",
            "total_assets",
            row["total_assets"],
            "INFO",
            "Assets and liabilities do not balance"
        )

    return balancesheet

def dq16_company_history(
    df,
    table_name,
    logger
):

    coverage = (
        df.groupby("company_id")["year"]
          .nunique()
    )

    invalid = coverage[coverage < 5]

    for company_id, years in invalid.items():

        logger.log(
            "DQ-16",
            table_name,
            company_id,
            "",
            "year",
            years,
            "WARNING",
            "Less than 5 years of financial history"
        )

    return df