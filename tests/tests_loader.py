import pytest
from src.ETL.loader import normalize_year, normalize_ticker

#testing normalize_year() with unit testing
def test_year_1():
    assert normalize_year("Mar-23") == "2023-03"

def test_year_2():
    assert normalize_year("Mar 23") == "2023-03"

def test_year_3():
    assert normalize_year("March-2023") == "2023-03"

def test_year_4():
    assert normalize_year("March 2023") == "2023-03"

def test_year_5():
    assert normalize_year("MAR 2023") == "2023-03"

def test_year_6():
    assert normalize_year("2023") == "2023-03"

def test_year_7():
    assert normalize_year("2,023") == "2023-03"

def test_year_8():
    assert normalize_year(2023) == "2023-03"

def test_year_9():
    assert normalize_year(2023.0) == "2023-03"

def test_year_10():
    assert normalize_year("FY23") == "2023-03"

def test_year_11():
    assert normalize_year("FY2023") == "2023-03"

def test_year_12():
    assert normalize_year("Dec-22") == "2022-12"

def test_year_13():
    assert normalize_year("Jun-24") == "2024-06"

def test_year_14():
    assert normalize_year("2023-03") == "2023-03"

def test_year_15():
    assert normalize_year("2023/03") == "2023-03"

def test_year_16():
    assert normalize_year("03/2023") == "2023-03"

def test_year_17():
    assert normalize_year("Jan-21") == "2021-01"

def test_year_18():
    assert normalize_year("Aug-20") == "2020-08"

def test_year_19():
    assert normalize_year("TTM") == None

def test_year_20():
    assert normalize_year("ABCXYZ") is None


#testing normalize_ticker() with unit testing
def test_ticker_1():
    assert normalize_ticker("tcs") == "TCS"

def test_ticker_2():
    assert normalize_ticker("TCS.NS") == "TCS"

def test_ticker_3():
    assert normalize_ticker("reliance.ns") == "RELIANCE"

def test_ticker_4():
    assert normalize_ticker("INFY.BO") == "INFY"

def test_ticker_5():
    assert normalize_ticker("hdfc bank") == "HDFCBANK"

def test_ticker_6():
    assert normalize_ticker("icici-bank") == "ICICIBANK"

def test_ticker_7():
    assert normalize_ticker("axis_bank") == "AXISBANK"

def test_ticker_8():
    assert normalize_ticker("SBIN") == "SBIN"

def test_ticker_9():
    assert normalize_ticker("ltim") == "LTIM"

def test_ticker_10():
    assert normalize_ticker("TATA MOTORS") == "TATAMOTORS"

def test_ticker_11():
    assert normalize_ticker("BAJAJ-FINANCE") == "BAJAJFINANCE"

def test_ticker_12():
    assert normalize_ticker("asian_paints") == "ASIANPAINTS"

def test_ticker_13():
    assert normalize_ticker(None) is None

def test_ticker_14():
    assert normalize_ticker(" ") == ""

def test_ticker_15():
    assert normalize_ticker("HCLTECH.NS") == "HCLTECH"