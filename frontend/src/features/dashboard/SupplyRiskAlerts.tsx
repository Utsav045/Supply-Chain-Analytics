interface SupplyRiskAlertsProps {
  count?: number;
}

const SupplyRiskAlerts = ({
  count = 3,
}: SupplyRiskAlertsProps) => {
  return (
    <article className="dashboard-panel supply-risk-panel">
      <div className="panel-header">
        <div>
          <h2>Supply Risk Alerts</h2>
          <span>Items requiring attention</span>
        </div>
      </div>

      <div className="supply-risk-content">
        <div className="risk-count">
          <strong>{count}</strong>
          <span>High Risk Items</span>
        </div>

        <div className="risk-indicator">
          <svg
            viewBox="0 0 50 20"
            width="70"
            height="32"
            aria-label="Supply risk trend"
          >
            <polyline
              points="0,15 10,10 20,18 30,5 40,12 50,2"
              fill="none"
              stroke="#f43f5e"
              strokeWidth="2"
            />
          </svg>
        </div>
      </div>
    </article>
  );
};

export default SupplyRiskAlerts;