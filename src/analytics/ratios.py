
from src.validators.validation_logger import ValidationLogger

#net profit margin
def net_profit_margin(net_profit,sales):
    if sales ==0:
        return None
    npm=(net_profit/sales)*100
    return npm

#operating_profit_ratio

def operating_profit_ratio(operating_profit,sales,opm_percentage,logger,company_id,year):
    if sales==0:
        return None
    calculated_opm=(operating_profit/sales)*100

    diff=abs(calculated_opm-opm_percentage)
    if diff>1:
        logger.log( "DQ-05",
            "profitandloss",
            company_id,
            year,
           "operating_profit_margin_pct",
            opm_percentage,
            "warning",
        f"Calculated OPM ({calculated_opm:.2f}%) differs by {diff:.2f}%"
        )
    return calculated_opm

#return_on_equity

def return_on_equity(net_profit,equity_capital,reserves):
    if equity_capital+reserves <= 0:
        return None
    roe=net_profit/(equity_capital+reserves)*100
    return roe

# return on capital employed

def return_on_capital_employed(operating_profit,equity_capital,reserves,borrowings):
    if (equity_capital+reserves+borrowings)<=0:
        return None
    cal_roce=operating_profit/(equity_capital+reserves+borrowings)*100
    return cal_roce

def check_roce_benchmark(
    roce,
    broad_sector,
    benchmark_roce,
    absolute_threshold=15,):
    """
    Compare ROCE against the appropriate benchmark.

    Returns
    -------
    bool
        True -> Passed benchmark
        False -> Failed benchmark
    """

    if roce is None:
        return None

    # Financial companies
    if broad_sector == "Financial":
        if benchmark_roce is None:
           return None
        return roce >= benchmark_roce

    # Other sectors
    return roce >= absolute_threshold

def get_benchmark_roce(
    company_id,
    sectors,
    peer_groups,
    ratio_df,
):
    # Find the company's peer group
    company_peer = peer_groups[
        peer_groups["company_id"] == company_id
    ]

    if company_peer.empty:
        return None

    peer_group_name = company_peer.iloc[0]["peer_group_name"]

    # Find the benchmark company in that peer group
    benchmark_row = peer_groups[
        (peer_groups["peer_group_name"] == peer_group_name)
        & (peer_groups["is_benchmark"] == True)
    ]

    if benchmark_row.empty:
        return None

    benchmark_company = benchmark_row.iloc[0]["company_id"]

    # Get benchmark company's ROCE
    benchmark_roce_row = ratio_df[
        ratio_df["company_id"] == benchmark_company
    ]

    if benchmark_roce_row.empty:
        return None

    return benchmark_roce_row.iloc[0]["returns_on_capital_employment"]

#return on assets
def return_on_assets(net_profit,total_assets):
    if total_assets==0:
        return None
    roa=net_profit/(total_assets)*100
    return roa

# day-10

def debt_to_equity(borrowings,equity_capital,reserves):
    if borrowings==0:
        return 0
    if equity_capital + reserves <= 0:
        return None
    de=borrowings/(equity_capital+reserves)
    return de

def check_high_leverage(de,broad_sector):
    if de is None:
        return False
    if de>5 and broad_sector!='Financials':
        return True
    return False

def interest_coverage_ratio(operating_profit,other_income,interest):
    if interest==0:
        return None
    icr=(operating_profit+other_income)/interest
    return icr

def get_icr_label(icr):
    if icr==None:
        return 'Debt Free'
    return None

def check_icr_warning(icr):
    if icr is None:
        return False
    if icr<1.5:
        return True
    return False

def net_debt(borrowings,investments):
    return borrowings-investments

def asset_turn_over(sales,total_assets):
    if total_assets==0:
        return None
    return sales/total_assets
