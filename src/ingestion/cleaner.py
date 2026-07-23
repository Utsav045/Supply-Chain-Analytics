import pandas as pd


def clean_data(df):

    # Remove duplicate rows
    df = df.drop_duplicates()

    for column in df.columns:

        # Convert numeric-like columns
        converted = pd.to_numeric(df[column], errors="coerce")

        # If most values are numeric, treat as numeric
        if converted.notna().sum() > 0:

            median_value = converted.median()

            converted = converted.fillna(median_value)

            converted[converted < 0] = median_value

            # Convert float to int if column contains whole numbers
            if (converted % 1 == 0).all():
                df[column] = converted.astype(int)
            else:
                df[column] = converted

        else:
            # String column
            df[column] = df[column].fillna("Unknown")
            df[column] = df[column].replace("", "Unknown")

    return df


def main():

    print("===================================")
    print("Loading Sample Datasets...")
    print("===================================")

    sales_df = pd.read_csv("data/sample/sales_raw_data.csv")
    inventory_df = pd.read_csv("data/sample/inventory_raw_data.csv")
    supplier_df = pd.read_csv("data/sample/supplier_raw_data.csv")

    print("Cleaning Sales Dataset...")
    sales_df = clean_data(sales_df)

    print("Cleaning Inventory Dataset...")
    inventory_df = clean_data(inventory_df)

    print("Cleaning Supplier Dataset...")
    supplier_df = clean_data(supplier_df)

    print("Saving Cleaned Datasets...")

    sales_df.to_csv("data/processed/clean_sales_data.csv", index=False)
    inventory_df.to_csv("data/processed/clean_inventory_data.csv", index=False)
    supplier_df.to_csv("data/processed/clean_supplier_data.csv", index=False)

    print("===================================")
    print("Cleaning Completed Successfully")
    print("Files Saved in data/processed/")
    print("===================================")


if __name__ == "__main__":
    main()
