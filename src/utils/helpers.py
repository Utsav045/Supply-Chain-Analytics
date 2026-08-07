import os
import pandas as pd


class Helper:

    def __init__(self):

        self.raw_path = "data/raw"
        self.processed_path = "data/processed"

        os.makedirs(self.processed_path, exist_ok=True)

    def load_datasets(self):

        print("=" * 60)
        print("Loading Datasets...")
        print("=" * 60)

        self.sales_df = pd.read_csv(
            f"{self.raw_path}/sales_data.csv"
        )

        self.inventory_df = pd.read_csv(
            f"{self.raw_path}/inventory_data.csv"
        )

        self.supplier_df = pd.read_csv(
            f"{self.raw_path}/supplier_data.csv"
        )

        print("Datasets Loaded Successfully\n")

        return (
            self.sales_df,
            self.inventory_df,
            self.supplier_df
        )

    def dataset_summary(self, df, name):

        print("=" * 60)
        print(name)
        print("=" * 60)

        print("\nShape")
        print(df.shape)

        print("\nColumns")
        print(df.columns.tolist())

        print("\nData Types")
        print(df.dtypes)

        print("\nMissing Values")
        print(df.isnull().sum())

        print("\nFirst Five Rows")
        print(df.head())

        print("\n")

    def remove_duplicates(self, df):

        return df.drop_duplicates()

    def fill_missing_values(self, df):

        for column in df.columns:

            if pd.api.types.is_numeric_dtype(df[column]):

                df[column] = df[column].fillna(
                    df[column].median()
                )

            else:

                mode = df[column].mode()

                if not mode.empty:
                    df[column] = df[column].fillna(
                        mode.iloc[0]
                    )

        return df

    def convert_datetime(self, df, column):

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
                dayfirst=True
            )

        return df

    def interpolate_numeric(self, df):

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns

        df[numeric_columns] = (
            df[numeric_columns]
            .interpolate(method="linear")
            .bfill()
            .ffill()
        )

        return df

    def save_dataset(self, df, filename):

        output = f"{self.processed_path}/{filename}"

        df.to_csv(output, index=False)

        print(f"Saved -> {output}")


def main():

    helper = Helper()

    sales_df, inventory_df, supplier_df = helper.load_datasets()

    helper.dataset_summary(
        sales_df,
        "Sales Dataset"
    )

    helper.dataset_summary(
        inventory_df,
        "Inventory Dataset"
    )

    helper.dataset_summary(
        supplier_df,
        "Supplier Dataset"
    )

    sales_df = helper.remove_duplicates(sales_df)
    inventory_df = helper.remove_duplicates(inventory_df)
    supplier_df = helper.remove_duplicates(supplier_df)

    sales_df = helper.fill_missing_values(sales_df)
    inventory_df = helper.fill_missing_values(inventory_df)
    supplier_df = helper.fill_missing_values(supplier_df)

    sales_df = helper.convert_datetime(
        sales_df,
        "date"
    )

    inventory_df = helper.convert_datetime(
        inventory_df,
        "date"
    )

    supplier_df = helper.convert_datetime(
        supplier_df,
        "delivery_date"
    )

    sales_df = helper.interpolate_numeric(sales_df)
    inventory_df = helper.interpolate_numeric(inventory_df)
    supplier_df = helper.interpolate_numeric(supplier_df)

    helper.save_dataset(
        sales_df,
        "helper_sales_data.csv"
    )

    helper.save_dataset(
        inventory_df,
        "helper_inventory_data.csv"
    )

    helper.save_dataset(
        supplier_df,
        "helper_supplier_data.csv"
    )

    print("\n" + "=" * 60)
    print("Helper Module Executed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()