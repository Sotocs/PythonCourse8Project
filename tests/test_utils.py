from unittest.mock import patch, mock_open
import json
import pandas as pd

from scr.utils import load_transactions


# =========================
# JSON ТЕСТЫ
# =========================


def test_json_valid_list():
    data = [{"id": 1}, {"id": 2}]

    with patch("builtins.open", mock_open(read_data=json.dumps(data))):
        result = load_transactions("file.json")

    assert result == data


def test_json_not_list():
    data = {"id": 1}

    with patch("builtins.open", mock_open(read_data=json.dumps(data))):
        result = load_transactions("file.json")

    assert result == []


def test_json_empty():
    with patch("builtins.open", mock_open(read_data="")):
        result = load_transactions("file.json")

    assert result == []


def test_json_invalid():
    with patch("builtins.open", mock_open(read_data="{bad json}")):
        result = load_transactions("file.json")

    assert result == []


# =========================
# CSV ТЕСТЫ
# =========================


def test_csv_valid():
    csv_data = "id,amount\n1,100\n2,200\n"

    with patch("builtins.open", mock_open(read_data=csv_data)):
        result = load_transactions("file.csv")

    expected = [
        {"id": "1", "amount": "100"},
        {"id": "2", "amount": "200"},
    ]

    assert result == expected


def test_csv_empty():
    with patch("builtins.open", mock_open(read_data="")):
        result = load_transactions("file.csv")

    assert result == []


# =========================
# XLSX ТЕСТЫ
# =========================


def test_xlsx_valid():
    df = pd.DataFrame(
        [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 200},
        ]
    )

    with patch("pandas.read_excel", return_value=df):
        result = load_transactions("file.xlsx")

    expected = df.to_dict("records")
    assert result == expected


def test_xlsx_empty():
    df = pd.DataFrame()

    with patch("pandas.read_excel", return_value=df):
        result = load_transactions("file.xlsx")

    assert result == []


# =========================
# ОБЩИЕ ТЕСТЫ
# =========================


def test_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_transactions("file.json")

    assert result == []


def test_unknown_format():
    result = load_transactions("file.txt")
    assert result == []
