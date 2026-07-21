#
import pandas as pd


def process_datetime(df):

    print("Processing datetime columns...")

    for column in df.columns:

        if "date" in column.lower():

            df[column] = pd.to_datetime(df[column], errors="coerce")

            df[column + "_year"] = df[column].dt.year
            df[column + "_month"] = df[column].dt.month
            df[column + "_day"] = df[column].dt.day
            df[column + "_weekday"] = df[column].dt.day_name()
            df[column + "_quarter"] = df[column].dt.quarter

    print("Datetime processing completed.\n")

    return df


def main():

    print("Loading cleaned datasets...\n")

    sales_df = pd.read_excel("data/processed/clean_sales_data.xlsx")
    inventory_df = pd.read_excel("data/processed/clean_inventory_data.xlsx")
    supplier_df = pd.read_excel("data/processed/clean_supplier_data.xlsx")

    sales_df = process_datetime(sales_df)
    inventory_df = process_datetime(inventory_df)
    supplier_df = process_datetime(supplier_df)

    sales_df.to_excel("data/processed/clean_sales_data.xlsx", index=False)
    inventory_df.to_excel("data/processed/clean_inventory_data.xlsx", index=False)
    supplier_df.to_excel("data/processed/clean_supplier_data.xlsx", index=False)

    print("===================================")
    print("Datetime preprocessing completed.")
    print("Datasets updated successfully.")
    print("===================================")


if __name__ == "__main__":
    main()