import os

import pandas as pd


def clean_data(df):
    print("Cleaning dataset...")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Handle missing values
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = pd.to_numeric(df[column], errors="coerce")
            df[column] = df[column].fillna(df[column].median())
        else:
            df[column] = df[column].fillna(df[column].mode()[0])

    # Handle negative values in numeric columns
    numeric_columns = df.select_dtypes(include=["number"]).columns

    for column in numeric_columns:
        median_value = df[column].median()

        if pd.api.types.is_integer_dtype(df[column]):
            median_value = int(round(median_value))

        df.loc[df[column] < 0, column] = median_value

    print("Dataset cleaned successfully.\n")

    return df


def main():

    print("Loading datasets...\n")

    sales_df = pd.read_excel("data/sample/sales_raw_data.xlsx")
    inventory_df = pd.read_excel("data/sample/inventory_raw_data.xlsx")
    supplier_df = pd.read_excel("data/sample/supplier_raw_data.xlsx")

    sales_df = clean_data(sales_df)
    inventory_df = clean_data(inventory_df)
    supplier_df = clean_data(supplier_df)

    os.makedirs("data/processed", exist_ok=True)

    sales_df.to_csv("data/processed/clean_sales_data.csv", index=False)
    inventory_df.to_csv("data/processed/clean_inventory_data.csv", index=False)
    supplier_df.to_csv("data/processed/clean_supplier_data.csv", index=False)

    print("=======================================")
    print("All datasets cleaned successfully.")
    print("Saved in data/processed/")
    print("=======================================")


if __name__ == "__main__":
    main()
