#
import pandas as pd


def add_calendar_features(df, date_column):

    # Convert date column to datetime
    df[date_column] = pd.to_datetime(
        df[date_column],
        dayfirst=True,
        errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(subset=[date_column])

    # Calendar Features
    df["year"] = df[date_column].dt.year
    df["month"] = df[date_column].dt.month
    df["day"] = df[date_column].dt.day
    df["weekday"] = df[date_column].dt.day_name()
    df["week"] = df[date_column].dt.isocalendar().week.astype(int)
    df["quarter"] = df[date_column].dt.quarter
    df["is_weekend"] = df[date_column].dt.weekday >= 5

    return df


def main():

    print("=" * 50)
    print("Loading Resampled Datasets...")
    print("=" * 50)

    sales_df = pd.read_csv(
        "data/processed/resampled_sales_data.csv"
    )

    inventory_df = pd.read_csv(
        "data/processed/resampled_inventory_data.csv"
    )

    supplier_df = pd.read_csv(
        "data/processed/resampled_supplier_data.csv"
    )

    print("Generating Calendar Features for Sales...")
    sales_df = add_calendar_features(
        sales_df,
        "date"
    )

    print("Generating Calendar Features for Inventory...")
    inventory_df = add_calendar_features(
        inventory_df,
        "date"
    )

    print("Generating Calendar Features for Supplier...")
    supplier_df = add_calendar_features(
        supplier_df,
        "delivery_date"
    )

    print("Saving Feature Engineered Datasets...")

    sales_df.to_csv(
        "data/processed/calendar_sales_data.csv",
        index=False
    )

    inventory_df.to_csv(
        "data/processed/calendar_inventory_data.csv",
        index=False
    )

    supplier_df.to_csv(
        "data/processed/calendar_supplier_data.csv",
        index=False
    )

    print("=" * 50)
    print("Calendar Feature Engineering Completed")
    print("Files saved in data/processed/")
    print("=" * 50)


if __name__ == "__main__":
    main()