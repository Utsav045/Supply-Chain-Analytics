# Team Ownership & Development Responsibilities

## Team Members

| Team Member | Role |
|-------------|------|
| Utsav J. Charkhawala | Team Lead, Solution Architect & Full Stack Integration |
| Isaac Precious | Time-Series Forecasting & Machine Learning Lead |
| Rajarshi Ghosh | Data Engineering & Visualization Lead |
| Palak Thakur | Anomaly Detection, QA & Documentation Lead |

---

# Folder & File Ownership

## Utsav J. Charkhawala

| Folder | Files | Responsibility |
|---------|-------|----------------|
| backend/app/ | main.py | FastAPI Application |
| backend/app/api/ | router.py | API Router |
| backend/app/api/routes/ | forecast.py, anomaly.py, dashboard.py, health.py | REST APIs |
| backend/app/core/ | config.py, logger.py, constants.py | Configuration |
| backend/app/database/ | connection.py, models.py | Database |
| frontend/ | Entire Folder | React + TypeScript |
| .github/ | Entire Folder | GitHub Actions |
| docker/ | Entire Folder | Docker |
| scripts/ | Entire Folder | Automation Scripts |
| Root | docker-compose.yml, .pre-commit-config.yaml | Deployment |

---

## Isaac Precious

| Folder | Files | Responsibility |
|---------|-------|----------------|
| backend/app/services/preprocessing/ | datetime_processor.py, resampler.py, interpolator.py | Time Series Preprocessing |
| backend/app/services/decomposition/ | seasonal.py | Seasonal Decomposition |
| backend/app/services/feature_engineering/ | lag_features.py, rolling_features.py, calendar_features.py | Feature Engineering |
| backend/app/services/forecasting/ | moving_average.py, arima.py, prophet.py, trainer.py, evaluator.py | Forecasting Models |
| backend/app/schemas/ | forecast.py | Forecast Schemas |
| backend/tests/preprocessing/ | All Files | Unit Tests |
| backend/tests/decomposition/ | All Files | Unit Tests |
| backend/tests/feature_engineering/ | All Files | Unit Tests |
| backend/tests/forecasting/ | All Files | Unit Tests |

---

## Rajarshi Ghosh

| Folder | Files | Responsibility |
|---------|-------|----------------|
| backend/app/services/ingestion/ | loader.py, validator.py, cleaner.py | Data Ingestion |
| backend/app/services/visualization/ | dashboard_chart.py, forecast_chart.py, anomaly_chart.py | Visualizations |
| backend/app/services/utils/ | metrics.py, helpers.py | Utility Functions |
| backend/app/schemas/ | common.py | Common Schemas |
| backend/data/ | Entire Folder | Dataset Management |
| backend/tests/ingestion/ | All Files | Unit Tests |
| backend/tests/visualization/ | All Files | Unit Tests |
| backend/tests/utils/ | All Files | Unit Tests |

---

## Palak Thakur

| Folder | Files | Responsibility |
|---------|-------|----------------|
| backend/app/services/anomaly/ | detector.py, zscore.py, iqr.py, isolation_forest.py | Anomaly Detection |
| backend/app/schemas/ | anomaly.py | Anomaly Schemas |
| backend/app/services/utils/ | exceptions.py | Exception Handling |
| backend/tests/anomaly/ | All Files | Unit Tests |
| backend/tests/api/ | All Files | API Tests |
| backend/tests/integration/ | All Files | Integration Tests |
| backend/tests/ | conftest.py | Shared Fixtures |
| docs/ | PRD.md, SRS.md, HLD.md, LLD.md, API.md, SECURITY.md, TESTING.md, DEPLOYMENT.md, TEAM_GUIDE.md | Documentation |

---

# Integration Ownership

| Task | Owner |
|------|-------|
| Repository Setup | **Utsav J. Charkhawala** |
| Project Architecture | **Utsav J. Charkhawala** |
| Backend Integration | **Utsav J. Charkhawala** |
| Frontend Development | **Utsav J. Charkhawala** |
| API Integration | **Utsav J. Charkhawala** |
| Database Integration | **Utsav J. Charkhawala** |
| Code Reviews | **Utsav J. Charkhawala** |
| Merge Pull Requests | **Utsav J. Charkhawala** |
| Release Management | **Utsav J. Charkhawala** |
| Deployment | **Utsav J. Charkhawala** |
| Final Testing | **Utsav J. Charkhawala** & **Palak Thakur** |

---

# Module Ownership Summary

| Module | Primary Owner | Reviewer |
|---------|---------------|----------|
| API | **Utsav J. Charkhawala** | **Palak Thakur** |
| Core Configuration | **Utsav J. Charkhawala** | **Rajarshi Ghosh** |
| Database | **Utsav J. Charkhawala** | **Isaac Precious** |
| Frontend | **Utsav J. Charkhawala** | **Rajarshi Ghosh** |
| Data Ingestion | **Rajarshi Ghosh** | **Utsav J. Charkhawala** |
| Preprocessing | **Isaac Precious** | **Rajarshi Ghosh** |
| Time-Series Decomposition | **Isaac Precious** | **Utsav J. Charkhawala** |
| Feature Engineering | **Isaac Precious** | **Rajarshi Ghosh** |
| Forecasting Models | **Isaac Precious** | **Utsav J. Charkhawala** |
| Anomaly Detection | **Palak Thakur** | **Isaac Precious** |
| Visualization | **Rajarshi Ghosh** | **Utsav J. Charkhawala** |
| Documentation | **Palak Thakur** | **Utsav J. Charkhawala** |
| Testing | **Palak Thakur** | **Module Owner** |
| CI/CD & Deployment | **Utsav J. Charkhawala** | **Palak Thakur** |

---

# Code Review Workflow

| Pull Request Raised By | Reviewer |
|------------------------|----------|
| **Utsav J. Charkhawala** | **Palak Thakur** |
| **Isaac Precious** | **Utsav J. Charkhawala** |
| **Rajarshi Ghosh** | **Isaac Precious** |
| **Palak Thakur** | **Rajarshi Ghosh** |

---

# Merge Strategy

| Branch | Owner | Merge Responsibility |
|--------|-------|----------------------|
| `utsav` | Utsav J. Charkhawala | Self (after approvals) |
| `isaac` | Isaac Precious | Utsav J. Charkhawala |
| `rajarshi` | Rajarshi Ghosh | Utsav J. Charkhawala |
| `palak` | Palak Thakur | Utsav J. Charkhawala |

---

# Final Release Responsibility

| Activity | Responsible |
|----------|-------------|
| Backend Final Verification | **Utsav J. Charkhawala** |
| Frontend Final Verification | **Utsav J. Charkhawala** |
| Forecast Model Validation | **Isaac Precious** |
| Data Validation | **Rajarshi Ghosh** |
| Anomaly Detection Validation | **Palak Thakur** |
| Test Execution | **Palak Thakur** |
| Security Verification | **Palak Thakur** |
| Documentation Verification | **Palak Thakur** |
| Final Integration | **Utsav J. Charkhawala** |
| GitHub Release | **Utsav J. Charkhawala** |
| Production Deployment | **Utsav J. Charkhawala** |
| Final Demo & Project Presentation | **All Team Members** |