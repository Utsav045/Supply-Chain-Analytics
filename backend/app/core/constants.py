"""
Application Constants

Centralized constants used throughout the Supply Chain Analytics project.

Author: Utsav J. Charkhawala
"""

# ==========================================================
# DATASET COLUMN NAMES
# ==========================================================

DATE_COLUMN = "date"
PRODUCT_ID_COLUMN = "product_id"
PRODUCT_NAME_COLUMN = "product_name"
CATEGORY_COLUMN = "category"

SALES_COLUMN = "sales"
DEMAND_COLUMN = "demand"
INVENTORY_COLUMN = "inventory"

PRICE_COLUMN = "price"

# ==========================================================
# RESAMPLING FREQUENCIES
# ==========================================================

DAILY = "D"
WEEKLY = "W"
MONTHLY = "M"

SUPPORTED_FREQUENCIES = [
    DAILY,
    WEEKLY,
    MONTHLY,
]

# ==========================================================
# FORECAST MODELS
# ==========================================================

MOVING_AVERAGE = "moving_average"
ARIMA = "arima"
PROPHET = "prophet"

SUPPORTED_FORECAST_MODELS = [
    MOVING_AVERAGE,
    ARIMA,
    PROPHET,
]

# ==========================================================
# ANOMALY DETECTION METHODS
# ==========================================================

Z_SCORE = "z_score"
IQR = "iqr"
ISOLATION_FOREST = "isolation_forest"

SUPPORTED_ANOMALY_METHODS = [
    Z_SCORE,
    IQR,
    ISOLATION_FOREST,
]

# ==========================================================
# METRIC NAMES
# ==========================================================

MAPE = "MAPE"
RMSE = "RMSE"
MAE = "MAE"

# ==========================================================
# API STATUS
# ==========================================================

STATUS_SUCCESS = "success"
STATUS_FAILED = "failed"

# ==========================================================
# FILE EXTENSIONS
# ==========================================================

CSV_EXTENSION = ".csv"
XLSX_EXTENSION = ".xlsx"
JSON_EXTENSION = ".json"

# ==========================================================
# DEFAULT VALUES
# ==========================================================

DEFAULT_FORECAST_DAYS = 90
DEFAULT_CONFIDENCE_LEVEL = 0.95

# ==========================================================
# RANDOM SEED
# ==========================================================

RANDOM_STATE = 42
