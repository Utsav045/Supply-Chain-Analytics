# 📘 Project Blueprint

---

## 1. Cover Page
# Project Information

- **Project Name:** Supply Chain Analytics – Demand Forecasting & Anomaly Detection Platform

- **Team Members:**
  - Utsav J. Charkhawala
  - Isaac Precious
  - Rajarshi Ghosh
  - Palak Thakur

- **Roles:**
  | Team Member | Role |
  |-------------|------|
  | **Utsav J. Charkhawala** | Team Lead, Solution Architect & Full Stack Integration |
  | **Isaac Precious** | Time-Series Forecasting & Machine Learning Lead |
  | **Rajarshi Ghosh** | Data Engineering & Analytics Lead |
  | **Palak Thakur** | Quality Assurance, Documentation & Anomaly Detection Lead |

- **Project Duration:** 4 Weeks (Month 2 Internship Project)

- **Technology Stack:**
  - **Frontend:** React.js + TypeScript *(Angular can be adopted if required)*
  - **Backend:** FastAPI (Python)
  - **Machine Learning:** Scikit-learn, Statsmodels, Prophet
  - **Data Processing:** Pandas, NumPy
  - **Visualization:** Plotly, Recharts
  - **Database:** PostgreSQL
  - **Testing:** Pytest
  - **Code Quality:** Ruff, Black, MyPy
  - **Version Control:** Git & GitHub
  - **CI/CD:** GitHub Actions
  - **Deployment:** Docker + Nginx

---

# Version History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| v0.1.0 | DD-MM-YYYY | Utsav J. Charkhawala | Initial project planning, architecture, team role allocation, and repository setup. |
| v0.2.0 | DD-MM-YYYY | Team | Week 1 implementation – Data ingestion, preprocessing, and exploratory data analysis. |
| v0.3.0 | DD-MM-YYYY | Team | Week 2 implementation – Time-series decomposition, feature engineering, and anomaly detection. |
| v0.4.0 | DD-MM-YYYY | Team | Week 3 implementation – Demand forecasting models, evaluation, and optimization. |
| v1.0.0 | DD-MM-YYYY | Team | Week 4 implementation – Frontend integration, API development, testing, deployment, and final documentation. |

---

## 2. Executive Summary

## Business Problem

Efficient supply chain management is one of the most critical factors affecting the profitability and operational success of retail, e-commerce, manufacturing, and distribution businesses. Organizations must accurately predict future product demand to maintain optimal inventory levels while minimizing operational costs.

Traditional inventory planning methods often rely on historical averages or manual estimations, which fail to account for changing market conditions, seasonal trends, promotional campaigns, holidays, or unexpected events. As a result, businesses frequently encounter two major challenges:

- **Overestimating demand**, leading to excess inventory, increased warehouse costs, capital being tied up in unsold stock, product spoilage, and reduced cash flow.
- **Underestimating demand**, resulting in stock shortages, delayed deliveries, lost revenue, dissatisfied customers, and damage to brand reputation.

Additionally, abnormal events such as supplier delays, unexpected demand spikes, stock leakage, system failures, logistics disruptions, or viral product trends often remain unnoticed until they significantly impact business performance.

Most organizations possess large volumes of historical sales and inventory data, but lack intelligent systems capable of transforming this data into actionable insights. Decision-makers require automated forecasting and anomaly detection solutions that provide early warnings and accurate demand predictions to support proactive inventory planning.

---

## Solution

The proposed solution is a production-grade **Supply Chain Analytics Platform** that leverages Time Series Analysis, Machine Learning, and Statistical Analytics to optimize inventory planning and improve supply chain visibility.

The system will process historical sales and inventory data, automatically clean and preprocess the dataset, engineer relevant time-series features, detect operational anomalies, and forecast future product demand.

The platform will consist of two primary analytical components:

### Demand Forecasting Engine
Predict future product demand for configurable forecasting horizons using multiple forecasting algorithms such as:

- Moving Average (Baseline)
- ARIMA
- Facebook Prophet

The forecasting engine will assist procurement and inventory teams in making accurate purchasing decisions based on expected future demand.

### Anomaly Detection Engine
Automatically identify unusual inventory or sales behavior using statistical and machine learning techniques including:

- Z-Score Analysis
- Interquartile Range (IQR)
- Isolation Forest

Detected anomalies will be categorized based on severity and presented with contextual information to assist operational teams in identifying supply chain disruptions before they escalate.

The platform will expose these insights through a modern web application built using **React + TypeScript** for the frontend and **FastAPI** for the backend, providing interactive dashboards, forecasting visualizations, anomaly alerts, KPI monitoring, and downloadable analytical reports.

---

## Objectives

The primary objective of this project is to develop a scalable, maintainable, and production-ready Supply Chain Analytics Platform capable of improving inventory planning and operational decision-making through intelligent forecasting and automated anomaly detection.

### Business Objectives

- Improve inventory planning accuracy.
- Reduce stockouts and excess inventory.
- Enable proactive supply chain decision-making.
- Identify abnormal operational events early.
- Improve customer satisfaction through better product availability.
- Reduce operational and warehousing costs.
- Increase forecasting reliability using data-driven models.

### Technical Objectives

- Build an automated end-to-end data processing pipeline.
- Develop robust time-series preprocessing workflows.
- Implement statistical and machine learning based anomaly detection.
- Develop multiple forecasting models and compare their performance.
- Design a modular backend using FastAPI.
- Develop a responsive frontend using React and TypeScript.
- Implement REST APIs for seamless frontend-backend communication.
- Ensure high code quality through automated testing and continuous integration.
- Maintain comprehensive project documentation and GitHub workflow.

---

## Success Metrics

The success of the project will be evaluated using both business and technical performance indicators.

### Business Metrics

- Reduction in forecasting error.
- Improved inventory utilization.
- Faster identification of supply chain anomalies.
- Reduction in stockout incidents.
- Reduction in excess inventory.
- Improved operational visibility.
- Faster decision-making for procurement teams.

### Forecasting Performance Metrics

- Mean Absolute Error (MAE)
- Mean Absolute Percentage Error (MAPE)
- Root Mean Square Error (RMSE)
- Mean Squared Error (MSE)
- R² Score (where applicable)

### Anomaly Detection Metrics

- Precision
- Recall
- F1-Score
- False Positive Rate
- False Negative Rate
- Number of anomalies detected
- Alert accuracy

### Application Performance Metrics

- API response time < 500 ms
- Dashboard load time < 3 seconds
- Forecast generation time < 10 seconds
- Support for large historical datasets
- High application availability

### Code Quality Metrics

- Minimum 90% automated test coverage.
- Zero critical security vulnerabilities.
- Successful CI/CD pipeline execution.
- Ruff, Black, and MyPy compliance.
- Modular and maintainable architecture.

### Project Delivery Metrics

- Completion of all planned features within the four-week timeline.
- Daily GitHub commits following semantic commit conventions.
- Complete technical documentation.
- Successful deployment of the application.
- Review-ready project with reproducible setup instructions.

---

## 3. Product Requirements Document (PRD)

Complete PRD including:
- Vision
- Problem Statement
- Goals
- KPIs
- Stakeholders
- User Personas
- User Journey
- User Stories
- Functional Requirements
- Non-Functional Requirements
- Acceptance Criteria
- Risks
- Future Scope

---

## 4. Software Requirement Specification (SRS)

Including:
- Overall Description
- Product Perspective
- System Context
- Constraints
- Assumptions
- Technology Stack
- APIs
- Libraries
- Folder Responsibilities

### 4.1 Technology Stack (Consolidated)

> Derived from the tools, frameworks, and libraries referenced throughout this blueprint (folder structure, dev standards, CI/CD, testing, models, deployment).

| Layer | Technology / Tool | Purpose |
|---|---|---|
| Language | Python | Core development language |
| Dependency Management | `uv`, `pyproject.toml`, `uv.lock` | Package & environment management |
| App / UI | TypeScript + React (or Angular) | Interactive dashboard frontend |
| Forecasting Models | ARIMA, Prophet, Moving Average | Time-series forecasting |
| Anomaly Detection | Isolation Forest, Z-Score, IQR | Anomaly detection module |
| Code Quality | Ruff, Black, MyPy | Linting, formatting, type checking |
| Notebook Hygiene | nbstripout | Strips notebook output before commit |
| Testing | Pytest | Unit / Integration / Regression / Performance / Security / E2E testing |
| Test Coverage | Coverage tooling (target 90%+) | Code coverage enforcement |
| Git Hooks | Husky, pre-commit (`.pre-commit-config.yaml`) | Pre-commit & pre-push checks |
| Secret Scanning | Secret Scanner (pre-commit hook) | Prevents credential leaks |
| CI/CD | GitHub Actions (`ci.yml`, `security.yml`, `lint.yml`, `release.yml`) | Lint → Test → Coverage → Security → Build → Deploy |
| Containerization | Docker (`docker/`) | Packaging & deployment |
| Deployment Targets | Render, Local, Docker, Vercel/Netlify (frontend) | Hosting options |
| Version Control Workflow | GitHub Flow, Semantic Commits | Branching & commit strategy |
| Project Management | GitHub Issues, Labels, Milestones, Kanban | Task tracking |
| Documentation | Markdown (`docs/`), architecture & API docs | Project documentation |

---

## 5. Complete Enterprise Folder Structure

```
project-root/
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── security.yml
│   │   ├── lint.yml
│   │   └── release.yml
│   │
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS
│
├── .husky/
├── .pre-commit-config.yaml
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── assets/
│   │   ├── services/
│   │   ├── routes/
│   │   └── App.tsx        (or app.module.ts for Angular)
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
│
├── configs/
│
├── data/
│   ├── sample/
│   ├── processed/
│   └── generated/
│
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── deployment/
│   ├── testing/
│   ├── diagrams/
│   └── weekly_reports/
│
├── models/
│   ├── forecasting/
│   └── anomaly/
│
├── notebooks/
│
├── reports/
│
├── scripts/
│
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── decomposition/
│   ├── feature_engineering/
│   ├── forecasting/
│   ├── anomaly_detection/
│   ├── evaluation/
│   ├── visualization/
│   ├── services/
│   ├── config/
│   ├── utils/
│   └── exceptions/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── regression/
│   ├── security/
│   ├── performance/
│   └── conftest.py
│
├── logs/
├── artifacts/
├── exports/
└── docker/
```

---

## 6. Complete Project Flow

```
Raw Dataset
      │
      ▼
Data Validation
      │
      ▼
Data Cleaning
      │
      ▼
Time Series Processing
      │
      ▼
Feature Engineering
      │
      ├─────────────┐
      ▼             ▼
Forecasting     Anomaly Detection
      │             │
      └──────┬──────┘
             ▼
Model Evaluation
             ▼
Business KPIs
             ▼
Visualization
             ▼
React / Angular Dashboard (TypeScript)
             ▼
Export Reports
```

---

## 7. High-Level Architecture (HLD)
- Component Diagram
- Module Diagram
- Data Flow Diagram
- Deployment Diagram
- Sequence Diagram

---

## 8. Low-Level Design (LLD)

Every module will include:
- Purpose
- Responsibilities
- Classes
- Functions
- Inputs
- Outputs
- Error Handling
- Logging
- Validation

---

## 9. Development Standards
- Folder Naming
- File Naming
- Python Style Guide
- Ruff
- Black
- MyPy
- Logging
- Docstrings
- Type Hinting
- Exception Handling

---

## 10. Security Standards
- Environment Variables
- Secrets Management
- Input Validation
- CSV Validation
- Path Traversal Protection
- Safe File Upload
- Static Analysis
- Dependency Scanning
- Secure Logging
- Data Privacy

---

## 11. Testing Strategy

Every source file will have its own corresponding test file.

**Example:**
```
src/
  forecasting/
    arima.py

tests/
  forecasting/
    test_arima.py
```

**Testing Levels:**
- Unit Testing
- Integration Testing
- Regression Testing
- Performance Testing
- Security Testing
- End-to-End Testing

**Target Coverage:** 90%+

---

## 12. Git Strategy
- Branching
- GitHub Flow
- Pull Requests
- Code Review
- Semantic Commits
- Labels
- Issues
- Milestones
- Kanban

---

## 13. Git Hooks

**Pre-Commit**
- Ruff
- Black
- MyPy
- nbstripout
- pytest
- Secret Scanner

**Pre-Push**
- Coverage
- Security
- Build

---

## 14. CI/CD Pipeline (GitHub Actions)

```
Push
  ↓
Lint
  ↓
Tests
  ↓
Coverage
  ↓
Security
  ↓
Build
  ↓
Deploy
```

---

## 15. Week-wise Plan

**Week 1** — Daily tasks for Utsav, Isaac, Rajarshi, Palak (Monday–Sunday)
**Week 2** — Daily tasks
**Week 3** — Daily tasks
**Week 4** — Daily tasks

Each day will include:
- Owner
- Task
- Expected Deliverable
- GitHub Issues
- Suggested Commit Messages
- Review Checklist

---

## 16. Team Responsibilities

Detailed responsibilities for all four members.

---

## 17. GitHub Issue Breakdown

40–60 issues mapped to the four-week roadmap, with priorities, owners, and dependencies.

---

## 18. Documentation Checklist

Every document to create.

---

## 19. React / Angular UI Design (TypeScript)
- Every page/route
- Components (widgets, filters, charts)
- Navigation / Routing
- Theme
- State Management
- API Integration Layer

---

## 20. API Specifications

If APIs are introduced later.

---

## 21. Model Documentation
- Moving Average
- ARIMA
- Prophet
- Isolation Forest
- Z-Score
- IQR

With formulas and implementation notes.

---

## 22. Deployment Guide
- Docker
- Vercel / Netlify (frontend)
- Render (backend)
- Local

---

## 23. Review Preparation

Expected viva questions:
- Architecture questions
- Business questions
- Technical questions
- Role-wise answers

---

## 24. Appendix

**Commands:**
- Git
- UV
- Pytest
- Ruff
- Black

**Useful Links**
**Troubleshooting**
**Coding Standards**

---

## 📂 Recommended Documentation Structure (Upgrade)

Instead of a single Markdown file, organize the docs as a professional engineering wiki — this keeps each section maintainable and easy to navigate during development, matching documentation practices used in professional software teams:

```
docs/
├── 00_Project_Overview.md
├── 01_PRD.md
├── 02_SRS.md
├── 03_HLD.md
├── 04_LLD.md
├── 05_Project_Structure.md
├── 06_Development_Guide.md
├── 07_Testing_Strategy.md
├── 08_Security_Guide.md
├── 09_Git_Workflow.md
├── 10_Weekwise_Execution_Plan.md
├── 11_Team_Roles.md
├── 12_Deployment_Guide.md
├── 13_Review_Preparation.md
└── diagrams/
```
