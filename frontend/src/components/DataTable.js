const DataTable = ({ data }) => {
    if (!data || data.length === 0) {
        return <div>No data available</div>;
    }
    console.log ("data:",data, "data.exchange_rates:", data.exchange_rates)

    return (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Rate</th>
                </tr>
            </thead>
            <tbody>
                {data.exchange_rates.map((item, index) => (
                    <tr key={index}>
                        <td>{item.date}</td>
                        <td>{parseFloat(item.rate)}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default DataTable;