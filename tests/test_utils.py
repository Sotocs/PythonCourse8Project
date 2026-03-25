import pytest
import json
from pathlib import Path
from scr.utils import load_transactions

# --- Создаём временные файлы для теста ---
@pytest.fixture
def tmp_json_file(tmp_path):
    file_path = tmp_path / "transactions.json"
    return file_path

def test_valid_list(tmp_json_file):
    data = [{"id": 1, "amount": 1000}, {"id": 2, "amount": 2000}]
    tmp_json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_transactions(str(tmp_json_file))
    assert result == data

def test_empty_file(tmp_json_file):
    tmp_json_file.write_text("", encoding="utf-8")
    result = load_transactions(str(tmp_json_file))
    assert result == []

def test_not_a_list(tmp_json_file):
    data = {"id": 1, "amount": 1000}  # словарь вместо списка
    tmp_json_file.write_text(json.dumps(data), encoding="utf-8")
    result = load_transactions(str(tmp_json_file))
    assert result == []

def test_file_not_found():
    result = load_transactions("non_existent_file.json")
    assert result == []

def test_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{invalid: json}", encoding="utf-8")  # некорректный JSON
    result = load_transactions(str(file_path))
    assert result == []