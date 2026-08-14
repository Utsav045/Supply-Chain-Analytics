const DashboardPage = () => {
  const kpiCards = [
    {
      title: "OTIF Rate",
      value: "94.2%",
      change: "+2.1%",
      period: "vs last 30 days",
      status: "Positive",
    },
    {
      title: "Total Logistics Cost",
      value: "$1.24M",
      change: "+4.8%",
      period: "vs last 30 days",
      status: "Positive",
    },
    {
      title: "Inventory Turnover",
      value: "4.8x",
      change: "Optimal",
      period: "Inventory efficiency",
      status: "Positive",
    },
    {
      title: "Backorder Rate",
      value: "12",
      change: "+8.3%",
      period: "vs last 30 days",
      status: "Negative",
    },
  ];

  return (
    <section className="dashboard-page">
      <div className="dashboard-heading">
        <div>
          <h1>Executive Overview</h1>
          <p>Monitor your supply chain performance</p>
        </div>
      </div>

      <div className="kpi-grid">
        {kpiCards.map((card) => (
          <article className="kpi-card" key={card.title}>
            <div className="kpi-card-header">
              <span className="kpi-card-title">{card.title}</span>
            </div>

            <div className="kpi-value">{card.value}</div>

            <div
              className={`kpi-change ${
                card.status === "Negative" ? "negative" : "positive"
              }`}
            >
              {card.change}
              <span>{card.period}</span>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
};

export default DashboardPage;