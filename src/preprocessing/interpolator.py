import pandas as pd


def interpolate_data(df):

    numeric_columns = df.select_dtypes(include=["number"]).columns

    for column in numeric_columns:
        df[column] = df[column].interpolate(method="linear")
        df[column] = df[column].bfill()
        df[column] = df[column].ffill()

    return df


def main():

    print("===================================")
    print("Loading Cleaned Datasets...")
    print("===================================")

    sales_df = pd.read_csv("data/processed/clean_sales_data.csv")
    inventory_df = pd.read_csv("data/processed/clean_inventory_data.csv")
    supplier_df = pd.read_csv("data/processed/clean_supplier_data.csv")

    print("Interpolating Sales Dataset...")
    sales_df = interpolate_data(sales_df)

    print("Interpolating Inventory Dataset...")
    inventory_df = interpolate_data(inventory_df)

    print("Interpolating Supplier Dataset...")
    supplier_df = interpolate_data(supplier_df)

    print("Saving Interpolated Datasets...")

    sales_df.to_csv("data/processed/clean_sales_data.csv", index=False)
    inventory_df.to_csv("data/processed/clean_inventory_data.csv", index=False)
    supplier_df.to_csv("data/processed/clean_supplier_data.csv", index=False)

    print("===================================")
    print("Interpolation Completed Successfully")
    print("Files Saved in data/processed/")
    print("===================================")


if __name__ == "__main__":
    main()
