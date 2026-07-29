import pandas as pd


def add_lag_features(df, date_column):

    # Convert date column to datetime
    df[date_column] = pd.to_datetime(
        df[date_column],
        dayfirst=True,
        errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(subset=[date_column])

    # Sort by date
    df = df.sort_values(date_column)

    # Select numeric columns
    numeric_columns = df.select_dtypes(include=["number"]).columns

    # Create lag features
    for column in numeric_columns:
        df[column + "_lag1"] = df[column].shift(1)
        df[column + "_lag7"] = df[column].shift(7)

    # Fill missing values created by lagging
    df = df.bfill()

    return df


def main():

    print("=" * 50)
    print("Loading Calendar Feature Datasets...")
    print("=" * 50)

    sales_df = pd.read_csv(
        "data/processed/calendar_sales_data.csv"
    )

    inventory_df = pd.read_csv(
        "data/processed/calendar_inventory_data.csv"
    )

    supplier_df = pd.read_csv(
        "data/processed/calendar_supplier_data.csv"
    )

    print("Generating Lag Features for Sales...")
    sales_df = add_lag_features(
        sales_df,
        "date"
    )

    print("Generating Lag Features for Inventory...")
    inventory_df = add_lag_features(
        inventory_df,
        "date"
    )

    print("Generating Lag Features for Supplier...")
    supplier_df = add_lag_features(
        supplier_df,
        "delivery_date"
    )

    print("Saving Datasets...")

    sales_df.to_csv(
        "data/processed/lag_sales_data.csv",
        index=False
    )

    inventory_df.to_csv(
        "data/processed/lag_inventory_data.csv",
        index=False
    )

    supplier_df.to_csv(
        "data/processed/lag_supplier_data.csv",
        index=False
    )

    print("=" * 50)
    print("Lag Feature Engineering Completed Successfully")
    print("Files saved in data/processed/")
    print("=" * 50)


if __name__ == "__main__":
    main()