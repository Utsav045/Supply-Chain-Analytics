# Demand Forecasting Module

## Overview

The demand forecasting module generates future product-demand
predictions from historical supply-chain observations.

The current forecasting engine supports:

- Moving Average baselines
- ARIMA forecasting
- Chronological train-test splitting
- Expanding-window backtesting
- Automatic model comparison and selection
- Forecast confidence intervals
- Model artifact persistence
- FastAPI integration

## Data Contract

Required historical fields:

| Field | Type | Description |
|---|---|---|
| date | datetime | Observation date |
| sku_id | string | Product identifier |
| demand | numeric | Historical product demand |

Optional fields:

| Field | Type | Description |
|---|---|---|
| inventory_level | numeric | Available inventory |
| price | numeric | Product price |
| promotion | boolean | Promotion indicator |
| holiday | boolean | Holiday indicator |
| category | string | Product category |
| location_id | string | Store or warehouse |

The unique time-series key is normally:

```text
date + sku_id + location_id
