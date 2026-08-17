import { useState } from "react";
import "./settings.css";

const Settings = () => {
  const [organizationName, setOrganizationName] =
    useState("Supply Analytics");
  const [currency, setCurrency] = useState("INR");
  const [dateFormat, setDateFormat] = useState("DD/MM/YYYY");

  const [autoRefresh, setAutoRefresh] = useState(true);
  const [showKpiCards, setShowKpiCards] = useState(true);
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [anomalyAlerts, setAnomalyAlerts] = useState(true);
  const [forecastAlerts, setForecastAlerts] = useState(false);

  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);

    window.setTimeout(() => {
      setSaved(false);
    }, 2500);
  };

  return (
    <section className="settings-page">
      {/* Page Header */}
      <div className="settings-header">
        <h1>Settings</h1>
        <p>Manage application preferences and dashboard settings.</p>
      </div>

      {/* General Settings */}
      <div className="settings-card">
        <div className="settings-card-header">
          <h2>General Settings</h2>
          <p>Configure basic application information.</p>
        </div>

        <div className="settings-form-grid">
          {/* Organization Name */}
          <div className="settings-field settings-field-full">
            <label htmlFor="organizationName">
              Organization Name
            </label>

            <p className="settings-field-description">
              The name displayed throughout the application.
            </p>

            <input
              id="organizationName"
              type="text"
              value={organizationName}
              onChange={(event) =>
                setOrganizationName(event.target.value)
              }
              className="settings-input"
              placeholder="Enter organization name"
            />
          </div>

          {/* Currency */}
          <div className="settings-field">
            <label htmlFor="currency">
              Default Currency
            </label>

            <p className="settings-field-description">
              Currency used for financial values.
            </p>

            <select
              id="currency"
              value={currency}
              onChange={(event) =>
                setCurrency(event.target.value)
              }
              className="settings-select"
            >
              <option value="INR">
                INR - Indian Rupee
              </option>
              <option value="USD">
                USD - US Dollar
              </option>
              <option value="EUR">
                EUR - Euro
              </option>
              <option value="GBP">
                GBP - British Pound
              </option>
            </select>
          </div>

          {/* Date Format */}
          <div className="settings-field">
            <label htmlFor="dateFormat">
              Date Format
            </label>

            <p className="settings-field-description">
              Format used for displaying dates.
            </p>

            <select
              id="dateFormat"
              value={dateFormat}
              onChange={(event) =>
                setDateFormat(event.target.value)
              }
              className="settings-select"
            >
              <option value="DD/MM/YYYY">
                DD/MM/YYYY
              </option>
              <option value="MM/DD/YYYY">
                MM/DD/YYYY
              </option>
              <option value="YYYY-MM-DD">
                YYYY-MM-DD
              </option>
            </select>
          </div>
        </div>
      </div>

      {/* Dashboard Preferences */}
      <div className="settings-card">
        <div className="settings-card-header">
          <h2>Dashboard Preferences</h2>
          <p>
            Control how dashboard information is displayed.
          </p>
        </div>

        <div className="settings-options">
          {/* Auto Refresh */}
          <div className="settings-option">
            <div className="settings-option-content">
              <h3>Auto Refresh</h3>
              <p>
                Automatically refresh dashboard data.
              </p>
            </div>

            <button
              type="button"
              className={`settings-toggle ${
                autoRefresh
                  ? "settings-toggle--active"
                  : ""
              }`}
              onClick={() =>
                setAutoRefresh((value) => !value)
              }
              aria-pressed={autoRefresh}
              aria-label="Toggle Auto Refresh"
            >
              <span />
            </button>
          </div>

          {/* Show KPI Cards */}
          <div className="settings-option settings-option-last">
            <div className="settings-option-content">
              <h3>Show KPI Cards</h3>
              <p>
                Display key performance indicators on the
                dashboard.
              </p>
            </div>

            <button
              type="button"
              className={`settings-toggle ${
                showKpiCards
                  ? "settings-toggle--active"
                  : ""
              }`}
              onClick={() =>
                setShowKpiCards((value) => !value)
              }
              aria-pressed={showKpiCards}
              aria-label="Toggle Show KPI Cards"
            >
              <span />
            </button>
          </div>
        </div>
      </div>

      {/* Notifications */}
      <div className="settings-card">
        <div className="settings-card-header">
          <h2>Notifications</h2>
          <p>Manage important supply chain alerts.</p>
        </div>

        <div className="settings-options">
          {/* Email Notifications */}
          <div className="settings-option">
            <div className="settings-option-content">
              <h3>Email Notifications</h3>
              <p>
                Receive important system notifications by
                email.
              </p>
            </div>

            <button
              type="button"
              className={`settings-toggle ${
                emailNotifications
                  ? "settings-toggle--active"
                  : ""
              }`}
              onClick={() =>
                setEmailNotifications((value) => !value)
              }
              aria-pressed={emailNotifications}
              aria-label="Toggle Email Notifications"
            >
              <span />
            </button>
          </div>

          {/* Anomaly Alerts */}
          <div className="settings-option">
            <div className="settings-option-content">
              <h3>Anomaly Alerts</h3>
              <p>
                Get notified when unusual supply chain
                activity is detected.
              </p>
            </div>

            <button
              type="button"
              className={`settings-toggle ${
                anomalyAlerts
                  ? "settings-toggle--active"
                  : ""
              }`}
              onClick={() =>
                setAnomalyAlerts((value) => !value)
              }
              aria-pressed={anomalyAlerts}
              aria-label="Toggle Anomaly Alerts"
            >
              <span />
            </button>
          </div>

          {/* Forecast Alerts */}
          <div className="settings-option settings-option-last">
            <div className="settings-option-content">
              <h3>Forecast Alerts</h3>
              <p>
                Receive notifications about forecast changes.
              </p>
            </div>

            <button
              type="button"
              className={`settings-toggle ${
                forecastAlerts
                  ? "settings-toggle--active"
                  : ""
              }`}
              onClick={() =>
                setForecastAlerts((value) => !value)
              }
              aria-pressed={forecastAlerts}
              aria-label="Toggle Forecast Alerts"
            >
              <span />
            </button>
          </div>
        </div>

        {/* Save Area */}
        <div className="settings-save-area">
          {saved && (
            <span className="settings-save-message">
              Changes saved successfully.
            </span>
          )}

          <button
            type="button"
            className="settings-save-button"
            onClick={handleSave}
          >
            Save Changes
          </button>
        </div>
      </div>
    </section>
  );
};

export default Settings;