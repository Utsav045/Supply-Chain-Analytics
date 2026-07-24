import pandas as pd


def resample_dataset(df, date_column):

    # Convert to datetime
    df[date_column] = pd.to_datetime(
        df[date_column],
        dayfirst=True,
        errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(subset=[date_column])

    # Sort values
    df = df.sort_values(date_column)

    # Set index
    df.set_index(date_column, inplace=True)

    # Select numeric columns
    numeric_df = df.select_dtypes(include=["number"])

    # Weekly resampling
    resampled_df = numeric_df.resample("W").mean()

    # Fill missing values
    resampled_df = resampled_df.interpolate(method="linear")
    resampled_df = resampled_df.ffill()
    resampled_df = resampled_df.bfill()

    # Convert index back to column
    resampled_df.reset_index(inplace=True)

    return resampled_df


def main():

    print("=" * 50)
    print("Loading processed datasets...")
    print("=" * 50)

    sales_df = pd.read_csv("data/processed/clean_sales_data.csv")
    inventory_df = pd.read_csv("data/processed/clean_inventory_data.csv")
    supplier_df = pd.read_csv("data/processed/clean_supplier_data.csv")

    print("Resampling Sales Dataset...")
    sales_resampled = resample_dataset(sales_df, "date")

    print("Resampling Inventory Dataset...")
    inventory_resampled = resample_dataset(inventory_df, "date")

    print("Resampling Supplier Dataset...")
    supplier_resampled = resample_dataset(supplier_df, "delivery_date")

    print("Saving datasets...")

    sales_resampled.to_csv(
        "data/processed/resampled_sales_data.csv",
        index=False
    )

    inventory_resampled.to_csv(
        "data/processed/resampled_inventory_data.csv",
        index=False
    )

    supplier_resampled.to_csv(
        "data/processed/resampled_supplier_data.csv",
        index=False
    )

    print("=" * 50)
    print("Resampling completed successfully.")
    print("=" * 50)


if __name__ == "__main__":
    main()