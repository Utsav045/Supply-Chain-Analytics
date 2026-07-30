import pandas as pd


def add_rolling_features(df, date_column):

    # Convert date column to datetime
    df[date_column] = pd.to_datetime(df[date_column], dayfirst=True, errors="coerce")

    # Remove invalid dates
    df = df.dropna(subset=[date_column])

    # Sort by date
    df = df.sort_values(date_column)

    # Select numeric columns
    numeric_columns = df.select_dtypes(include=["number"]).columns

    # Create rolling features
    for column in numeric_columns:

        # 3-period rolling average
        df[column + "_rolling_mean_3"] = (
            df[column].rolling(window=3, min_periods=1).mean()
        )

        # 7-period rolling average
        df[column + "_rolling_mean_7"] = (
            df[column].rolling(window=7, min_periods=1).mean()
        )

        # 3-period rolling standard deviation
        df[column + "_rolling_std_3"] = (
            df[column].rolling(window=3, min_periods=1).std()
        )

        # 7-period rolling standard deviation
        df[column + "_rolling_std_7"] = (
            df[column].rolling(window=7, min_periods=1).std()
        )

    # Fill missing values created by standard deviation
    df = df.bfill()
    df = df.ffill()

    return df


def main():

    print("=" * 50)
    print("Loading Calendar Feature Datasets...")
    print("=" * 50)

    sales_df = pd.read_csv("data/processed/calendar_sales_data.csv")

    inventory_df = pd.read_csv("data/processed/calendar_inventory_data.csv")

    supplier_df = pd.read_csv("data/processed/calendar_supplier_data.csv")

    print("Generating Rolling Features for Sales...")
    sales_df = add_rolling_features(sales_df, "date")

    print("Generating Rolling Features for Inventory...")
    inventory_df = add_rolling_features(inventory_df, "date")

    print("Generating Rolling Features for Supplier...")
    supplier_df = add_rolling_features(supplier_df, "delivery_date")

    print("Saving Feature Engineered Datasets...")

    sales_df.to_csv("data/processed/rolling_sales_data.csv", index=False)

    inventory_df.to_csv("data/processed/rolling_inventory_data.csv", index=False)

    supplier_df.to_csv("data/processed/rolling_supplier_data.csv", index=False)

    print("=" * 50)
    print("Rolling Feature Engineering Completed Successfully")
    print("Files saved in data/processed/")
    print("=" * 50)


if __name__ == "__main__":
    main()
