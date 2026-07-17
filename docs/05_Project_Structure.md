# Project Structure

## Overview

The Supply Chain Analytics project follows a modular architecture to separate backend services, frontend components, datasets, documentation, and deployment resources. This structure improves maintainability, scalability, and collaborative development.

---

# Root Directory

```
Supply-Chain-Analytics/
│
├── backend/
├── frontend/
├── docs/
├── models/
├── docker/
├── scripts/
├── logs/
├── artifacts/
├── exports/
├── .github/
├── .githooks/
├── docker-compose.yml
├── README.md
└── setup.bat
```

---

# Backend Structure

```
backend/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── anomaly.py
│   │   │   ├── forecast.py
│   │   │   ├── dashboard.py
│   │   │   └── health.py
│   │   └── router.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── constants.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   ├── anomaly.py
│   │   ├── forecast.py
│   │   └── common.py
│   │
│   └── services/
│       ├── anomaly/
│       ├── forecasting/
│       ├── ingestion/
│       ├── preprocessing/
│       ├── visualization/
│       ├── feature_engineering/
│       ├── decomposition/
│       └── utils/
│
├── data/
└── tests/
```

---

# Frontend Structure

```
frontend/
│
├── public/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── hooks/
│   ├── assets/
│   └── styles/
│
├── package.json
└── tsconfig.json
```

---

# Models Directory

```
models/
│
├── anomaly/
│   ├── isolation_forest.pkl
│   ├── iqr_model.pkl
│   ├── zscore_model.pkl
│   └── README.md
│
└── forecasting/
```

---

# Documentation

```
docs/
│
├── 01_PRD.md
├── 02_SRS.md
├── 03_HLD.md
├── 04_LLD.md
├── 05_PROJECT_STRUCTURE.md
├── 06_API.md
├── 07_SECURITY.md
├── 08_TESTING.md
├── 09_DEPLOYMENT.md
├── 10_TEAM_GUIDE.md
└── 11_Team_Roles.md
```

---

# Supporting Directories

```
docker/
scripts/
.github/
.githooks/
logs/
artifacts/
exports/
```

---

# Purpose of Each Directory

| Directory | Purpose |
|-----------|---------|
| backend | Backend application and business logic |
| frontend | React-based user interface |
| docs | Project documentation |
| models | Machine learning models |
| data | Dataset storage |
| tests | Unit, API and integration tests |
| docker | Container configuration |
| scripts | Automation scripts |
| logs | Runtime logs |
| artifacts | Generated artifacts |
| exports | Exported reports and files |

---

# Design Principles

- Modular architecture
- Separation of concerns
- Scalable project organization
- Easy testing and maintenance
- Independent backend and frontend development
- Organized documentation and deployment resources

---

# Conclusion

The project structure has been designed to support collaborative development, simplify maintenance, and ensure scalability. Each module is organized according to its responsibility, enabling efficient implementation, testing, deployment, and future enhancements.