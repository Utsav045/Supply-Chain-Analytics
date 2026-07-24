# Deployment Guide

## Overview

This document explains how to deploy the Supply Chain Analytics application in a local development environment.

---

## Prerequisites

Before deployment, ensure the following software is installed:

- Python 3.12 or later
- Node.js and npm
- Git
- Visual Studio Code (recommended)

---

## Clone the Repository

```bash
git clone https://github.com/Utsav045/Supply-Chain-Analytics.git
cd Supply-Chain-Analytics
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

---

## Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

---

## Project Structure

```
backend/
frontend/
data/
models/
docs/
tests/
```

---

## Run the Backend

```bash
python backend/app/main.py
```

If your project uses another entry point (for example `uvicorn`), update this command accordingly.

---

## Run the Frontend

```bash
cd frontend
npm start
```

or

```bash
npm run dev
```

depending on the project configuration.

---

## Data Files

The project datasets are stored in:

```
data/sample/
data/processed/
data/generated/
```

Processed datasets are recommended for analysis.

---

## Machine Learning Models

Saved models are located in:

```
models/anomaly/
models/forecasting/
```

---

## Running Tests

```bash
pytest
```

---

## Code Formatting

Format the project using:

```bash
python -m black .
python -m isort .
ruff check .
```

---

## Git Workflow

Check repository status:

```bash
git status
```

Commit changes:

```bash
git add .
git commit -m "Commit message"
```

Push changes:

```bash
git push origin <branch-name>
```

---

## Troubleshooting

### ModuleNotFoundError

Activate the virtual environment and install the required dependencies.

### Git Merge Conflict

Pull the latest changes before pushing.

### Missing Dataset

Verify that the required CSV files are available in the `data/processed` directory.

### Model File Not Found

Ensure trained model files are present inside the `models` directory.

---

## Deployment Checklist

- Repository cloned
- Virtual environment activated
- Dependencies installed
- Backend running
- Frontend running
- Dataset available
- Models available
- Tests passed
- Ready for deployment