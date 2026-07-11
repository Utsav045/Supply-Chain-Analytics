# PowerShell script to create the remaining frontend files

$files = @(
    "frontend/src/components/charts/KPIChart.tsx",
    "frontend/src/components/charts/InventoryChart.tsx",
    "frontend/src/components/dashboard/KPISection.tsx",
    "frontend/src/components/dashboard/SummaryCards.tsx",
    "frontend/src/components/dashboard/RecentAlerts.tsx",
    "frontend/src/components/dashboard/TopProducts.tsx",
    "frontend/src/components/layout/Navbar.tsx",
    "frontend/src/components/layout/Sidebar.tsx",
    "frontend/src/components/layout/Header.tsx",
    "frontend/src/components/layout/Footer.tsx",
    "frontend/src/components/layout/Layout.tsx",
    "frontend/src/features/dashboard/DashboardPage.tsx",
    "frontend/src/features/dashboard/dashboardSlice.ts",
    "frontend/src/features/dashboard/dashboardService.ts",
    "frontend/src/features/dashboard/types.ts",
    "frontend/src/features/forecasting/ForecastPage.tsx",
    "frontend/src/features/forecasting/ForecastForm.tsx",
    "frontend/src/features/forecasting/ForecastTable.tsx",
    "frontend/src/features/forecasting/forecastSlice.ts",
    "frontend/src/features/forecasting/types.ts",
    "frontend/src/features/anomaly/AnomalyPage.tsx",
    "frontend/src/features/anomaly/AnomalyTable.tsx",
    "frontend/src/features/anomaly/anomalySlice.ts",
    "frontend/src/features/anomaly/types.ts",
    "frontend/src/features/inventory/InventoryPage.tsx",
    "frontend/src/features/inventory/InventoryTable.tsx",
    "frontend/src/features/inventory/inventorySlice.ts",
    "frontend/src/features/inventory/types.ts",
    "frontend/src/hooks/useForecast.ts",
    "frontend/src/hooks/useAnomaly.ts",
    "frontend/src/hooks/useDashboard.ts",
    "frontend/src/hooks/useInventory.ts",
    "frontend/src/hooks/useDebounce.ts",
    "frontend/src/layouts/MainLayout.tsx",
    "frontend/src/layouts/AuthLayout.tsx",
    "frontend/src/pages/Home.tsx",
    "frontend/src/pages/Dashboard.tsx",
    "frontend/src/pages/Forecast.tsx",
    "frontend/src/pages/Anomaly.tsx",
    "frontend/src/pages/Inventory.tsx",
    "frontend/src/pages/Reports.tsx",
    "frontend/src/pages/Settings.tsx",
    "frontend/src/pages/NotFound.tsx",
    "frontend/src/router/AppRouter.tsx",
    "frontend/src/router/PrivateRoute.tsx",
    "frontend/src/router/routes.ts",
    "frontend/src/store/index.ts",
    "frontend/src/store/store.ts",
    "frontend/src/App.tsx",
    "frontend/src/main.tsx",
    "frontend/src/vite-env.d.ts",
    "frontend/.env.example",
    "frontend/eslint.config.js",
    "frontend/prettier.config.js",
    "frontend/vite.config.ts",
    "frontend/tsconfig.json",
    "frontend/README.md"
)

foreach ($file in $files) {
    $fullPath = Join-Path -Path $PSScriptRoot -ChildPath $file
    $directory = Split-Path -Path $fullPath -Parent
    if (-not (Test-Path -Path $directory)) {
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
    }
    if (-not (Test-Path -Path $fullPath)) {
        New-Item -ItemType File -Force -Path $fullPath | Out-Null
        Write-Host "Created file: $file"
    } else {
        Write-Host "File already exists: $file"
    }
}
