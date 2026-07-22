import pandas as pd


def interpolate_data(df):
    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        df[column] = df[column].interpolate(method="linear")
        df[column] = df[column].bfill()
        df[column] = df[column].ffill()

    return df


def main():

    print("Loading datasets...")

    sales_df = pd.read_excel("data/processed/clean_sales_data.xlsx")
    inventory_df = pd.read_excel("data/processed/clean_inventory_data.xlsx")
    supplier_df = pd.read_excel("data/processed/clean_supplier_data.xlsx")

    sales_df = interpolate_data(sales_df)
    inventory_df = interpolate_data(inventory_df)
    supplier_df = interpolate_data(supplier_df)

    sales_df.to_excel("data/processed/clean_sales_data.xlsx", index=False)
    inventory_df.to_excel("data/processed/clean_inventory_data.xlsx", index=False)
    supplier_df.to_excel("data/processed/clean_supplier_data.xlsx", index=False)

    print("Interpolation completed successfully.")


if __name__ == "__main__":
    main()
