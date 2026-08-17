import pandas as pd
import pytest
from app.services.ingestion.loader import DataLoader
from app.services.utils.exceptions import DataLoadError


def test_load_non_existent_file():
    """Test that loading a non-existent file raises DataLoadError."""
    with pytest.raises(DataLoadError, match="File not found"):
        DataLoader.load_file("non_existent_file_xyz.csv")


def test_load_unsupported_format(tmp_path):
    """Test that loading an unsupported file extension raises DataLoadError."""
    temp_file = tmp_path / "data.txt"
    temp_file.write_text("some data")
    with pytest.raises(DataLoadError, match="Unsupported file extension"):
        DataLoader.load_file(temp_file)


def test_load_valid_csv(tmp_path):
    """Test loading a valid CSV file."""
    csv_file = tmp_path / "valid_data.csv"
    df_expected = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    df_expected.to_csv(csv_file, index=False)

    df_loaded = DataLoader.load_file(csv_file)
    assert list(df_loaded.columns) == ["col1", "col2"]
    assert len(df_loaded) == 2


def test_load_valid_excel(tmp_path):
    """Test loading a valid Excel file."""
    excel_file = tmp_path / "valid_data.xlsx"
    df_expected = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    df_expected.to_excel(excel_file, index=False)

    df_loaded = DataLoader.load_file(excel_file)
    assert list(df_loaded.columns) == ["col1", "col2"]
    assert len(df_loaded) == 2
