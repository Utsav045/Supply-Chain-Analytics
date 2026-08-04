import os

import pandas as pd


def create_directory(path):
    """
    Create directory if it does not exist.
    """
    os.makedirs(path, exist_ok=True)


def load_csv(file_path):
    """
    Load a CSV file.
    """
    return pd.read_csv(file_path)


def save_csv(df, file_path):
    """
    Save DataFrame to CSV.
    """
    directory = os.path.dirname(file_path)

    if directory:
        create_directory(directory)

    df.to_csv(file_path, index=False)


def convert_to_datetime(df, column):
    """
    Convert a column to datetime format.
    """
    df[column] = pd.to_datetime(df[column], dayfirst=True, errors="coerce")

    return df


def remove_duplicates(df):
    """
    Remove duplicate rows.
    """
    return df.drop_duplicates()


def fill_missing_values(df):
    """
    Fill missing values.
    Numeric columns -> Median
    Object columns -> Mode
    """

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(df[column]):

            df[column] = df[column].fillna(df[column].median())

        else:

            mode = df[column].mode()

            if not mode.empty:

                df[column] = df[column].fillna(mode.iloc[0])

    return df


def interpolate_numeric(df):
    """
    Interpolate numeric columns.
    """

    numeric_columns = df.select_dtypes(include=["number"]).columns

    df[numeric_columns] = (
        df[numeric_columns].interpolate(method="linear").bfill().ffill()
    )

    return df


def get_numeric_columns(df):
    """
    Return numeric column names.
    """
    return df.select_dtypes(include=["number"]).columns.tolist()


def print_shape(df, name):
    """
    Print DataFrame shape.
    """
    print(f"{name} Shape : {df.shape}")


def print_missing_values(df, name):
    """
    Print missing values.
    """
    print("\n" + "=" * 60)
    print(f"Missing Values in {name}")
    print("=" * 60)
    print(df.isnull().sum())


def print_separator():
    """
    Print separator line.
    """
    print("=" * 60)


def dataset_summary(df, name):
    """
    Print complete dataset summary.
    """

    print_separator()
    print(f"Dataset : {name}")
    print_separator()

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print_separator()


def save_processed_dataset(df, filename):
    """
    Save processed dataset.
    """

    output_path = os.path.join("data", "processed", filename)

    create_directory("data/processed")

    df.to_csv(output_path, index=False)

    print(f"Saved : {output_path}")


def load_processed_dataset(filename):
    """
    Load processed dataset.
    """

    file_path = os.path.join("data", "processed", filename)

    return pd.read_csv(file_path)
