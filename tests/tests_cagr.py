import pandas as pd
from src.analytics.cagr import calculate_cagr, metric_cagr


# ---------- calculate_cagr() tests ----------

def test_normal_cagr():
    value, flag = calculate_cagr(100, 200, 3)

    expected = round((((200 / 100) ** (1 / 3)) - 1) * 100, 3)

    assert value == expected
    assert flag == "COMPUTED_NORMALLY"


def test_turnaround_flag():
    value, flag = calculate_cagr(-100, 100, 3)

    assert value is None
    assert flag == "TURNAROUND"


def test_decline_to_loss():
    value, flag = calculate_cagr(100, -50, 3)

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_both_negative():
    value, flag = calculate_cagr(-100, -50, 3)

    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():
    value, flag = calculate_cagr(0, 100, 3)

    assert value is None
    assert flag == "ZERO BASE"


# ---------- metric_cagr() tests ----------

def test_metric_cagr_normal():
    df = pd.DataFrame({
        "year": ["2021-03", "2024-03"],
        "sales": [100, 200]
    })

    value, flag = metric_cagr(df, "sales", 3)

    expected = round((((200 / 100) ** (1 / 3)) - 1) * 100, 3)

    assert value == expected
    assert flag == "COMPUTED_NORMALLY"


def test_metric_cagr_insufficient_data():
    df = pd.DataFrame({
        "year": ["2022-03", "2024-03"],
        "sales": [100, 200]
    })

    value, flag = metric_cagr(df, "sales", 3)

    assert value is None
    assert flag == "INSUFFICIENT_DATA"


def test_metric_cagr_turnaround():
    df = pd.DataFrame({
        "year": ["2021-03", "2024-03"],
        "sales": [-100, 200]
    })

    value, flag = metric_cagr(df, "sales", 3)

    assert value is None
    assert flag == "TURNAROUND"


def test_metric_cagr_decline_to_loss():
    df = pd.DataFrame({
        "year": ["2021-03", "2024-03"],
        "sales": [100, -200]
    })

    value, flag = metric_cagr(df, "sales", 3)

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_metric_cagr_zero_base():
    df = pd.DataFrame({
        "year": ["2021-03", "2024-03"],
        "sales": [0, 200]
    })

    value, flag = metric_cagr(df, "sales", 3)

    assert value is None
    assert flag == "ZERO BASE"