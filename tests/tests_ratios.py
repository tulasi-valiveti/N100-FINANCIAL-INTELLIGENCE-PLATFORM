import pytest
from src.analytics.ratios import *
from src.validators.validation_logger import ValidationLogger

def test_net_profit_margin():
    assert net_profit_margin(145,1653)==pytest.approx(8.772,rel=1e-3)


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(234,0)==None

def test_operating_profit_ratio():
    logger=ValidationLogger()
    assert operating_profit_ratio(202,1653,12,logger,'ABB','2012-12')

def test_operating_profit_ratio_opm_mismatch():
    logger=ValidationLogger()
    operating_profit_ratio(202,1653,17,logger,'ABB','2012-12')
    assert len(logger.records)==1


def test_return_on_equity():
    assert return_on_equity(145,21,626)==pytest.approx(22.411,rel=1e-3)

def test_return_on_equity_negative_sales():
    assert return_on_equity(145,-21,21)==None

def test_return_on_capital_employed():
    assert return_on_capital_employed(202,21,626,0)==pytest.approx(31.221,rel=1e-3)

def test_return_on_capital_employed_negative_sales():
    assert return_on_capital_employed(202,-21,-34,0)==None

def test_return_on_assets():
    assert return_on_assets(145,907)==pytest.approx(15.987,rel=1e-3)

def test_return_on_assets_zero_sales():
    assert return_on_assets(145,0)==None


#day-10
def test_debt_to_equity():
    assert debt_to_equity(100,34,78)==pytest.approx(0.892,rel=1e-3)

def test_debt_to_equity_zero_borrowings():
     assert debt_to_equity(0,34,78)==0

def test_debt_to_equity_negative_reserves():
    assert debt_to_equity(678,0,0)==None

def test_check_high_leverage():
    assert check_high_leverage(8,'Financials')==False

def test_check_high_leverage_diff_sector():
    assert check_high_leverage(8,'Energy')==True

def test_interest_coverage_ratio():
    assert interest_coverage_ratio(896,88,76)==pytest.approx(12.947,rel=1e-3)

def test_interest_coverage_ratio_zero_interest():
    assert interest_coverage_ratio(896,88,0)==None

def test_get_icr_label_none():
    assert get_icr_label(None)=='Debt Free'

def test_get_icr_label():
    assert get_icr_label(56)==None

def test_check_icr_warning_none():
    assert check_icr_warning(None)==False

def test_check_icr_warning_lower():
    assert check_icr_warning(0.7)==True

def test_check_icr_warning_higher():
    assert check_icr_warning(8.9)==False

def test_net_debt():
    assert net_debt(1248,892)==356

#The company could theoretically repay all its debt and still have cash left over.
def test_net_debt_negative_result():
    assert net_debt(567,892)==-325

def test_assert_turn_over():
    assert asset_turn_over(3456,9812)==pytest.approx(0.352,rel=1e-3)

def test_assert_turn_over_zero_assets():
    assert asset_turn_over(3456,0)==None
