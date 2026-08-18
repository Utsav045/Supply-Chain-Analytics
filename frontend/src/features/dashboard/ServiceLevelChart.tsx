import {
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

interface ServiceLevelChartProps {
  value?: number;
}

const ServiceLevelChart = ({
  value = 96,
}: ServiceLevelChartProps) => {
  const remaining = 100 - value;

  const chartData = [
    {
      name: "Service Level",
      value,
    },
    {
      name: "Remaining",
      value: remaining,
    },
  ];

  return (
    <article className="dashboard-panel service-level-panel">
      <div className="panel-header">
        <div>
          <h2>Service Level</h2>
          <span>Overall fulfillment performance</span>
        </div>
      </div>

      <div className="service-level-chart">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              startAngle={90}
              endAngle={-270}
              innerRadius="68%"
              outerRadius="88%"
              paddingAngle={2}
              dataKey="value"
              stroke="none"
            >
              <Cell fill="#2563eb" />
              <Cell fill="#e5e7eb" />
            </Pie>

            <Tooltip
              formatter={(value) => [`${value}%`, "Service Level"]}
            />
          </PieChart>
        </ResponsiveContainer>

        <div className="service-level-center">
          <strong>{value}%</strong>
          <span>Service Level</span>
        </div>
      </div>
    </article>
  );
};

export default ServiceLevelChart;