import numpy as np
from sklearn.metrics import (mean_absolute_error,
                             mean_absolute_percentage_error,
                             mean_squared_error, r2_score)


def calculate_metrics(y_true, y_pred):

    mae = mean_absolute_error(y_true, y_pred)

    mse = mean_squared_error(y_true, y_pred)

    rmse = np.sqrt(mse)

    mape = mean_absolute_percentage_error(y_true, y_pred) * 100

    r2 = r2_score(y_true, y_pred)

    metrics = {
        "MAE": round(mae, 4),
        "MSE": round(mse, 4),
        "RMSE": round(rmse, 4),
        "MAPE (%)": round(mape, 4),
        "R2 Score": round(r2, 4),
    }

    return metrics


def print_metrics(metrics):
    """
    Display evaluation metrics.
    """

    print("=" * 50)
    print("Model Evaluation Metrics")
    print("=" * 50)

    for metric, value in metrics.items():
        print(f"{metric:<15}: {value}")

    print("=" * 50)


def main():

    # Example values
    y_true = [120, 150, 180, 210, 250]
    y_pred = [118, 155, 175, 220, 245]

    metrics = calculate_metrics(y_true, y_pred)

    print_metrics(metrics)


if __name__ == "__main__":
    main()
