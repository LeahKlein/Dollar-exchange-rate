import React from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    Legend,
    ResponsiveContainer
} from 'recharts';

const DataGraph = ({ data }) => {
  if (!data) {
      return <div>Loading...</div>;
  }

  const chartData = data.exchange_rates.map(item => ({
      name: item.date,
      value: parseFloat(item.rate)
  }));

  return (
    <div style={{ height: '400px', width: '100%' }}> {/* הוסף גובה לקומפוננטה DataGraph */}
      <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#8884d8" />
          </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DataGraph;