import pandas as pd


def load_datasets():

    print("Loading datasets...\n")

    sales_df = pd.read_excel("data/sample/sales_raw_data.xlsx")
    inventory_df = pd.read_excel("data/sample/inventory_raw_data.xlsx")
    supplier_df = pd.read_excel("data/sample/supplier_raw_data.xlsx")

    print("Datasets loaded successfully.\n")

    return sales_df, inventory_df, supplier_df


def display_info(df, name):

    print("=" * 50)
    print(name)
    print("=" * 50)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nData Types:")
    print(df.dtypes)

    print("\n")


def main():

    sales_df, inventory_df, supplier_df = load_datasets()

    display_info(sales_df, "Sales Dataset")
    display_info(inventory_df, "Inventory Dataset")
    display_info(supplier_df, "Supplier Dataset")


if __name__ == "__main__":
    main()
