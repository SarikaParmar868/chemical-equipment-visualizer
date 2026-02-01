import React, { useEffect, useState } from 'react';
import api from '../api';

function History() {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        api.get('history/')
            .then(res => setHistory(res.data))
            .catch(err => console.error(err));
    }, []);

    return (
        <div>
            <h2>Upload History (Last 5)</h2>
            <div className="card">
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr style={{ textAlign: 'left', borderBottom: '1px solid #eee' }}>
                            <th style={{ padding: '0.5rem' }}>Date</th>
                            <th style={{ padding: '0.5rem' }}>File Name</th>
                            <th style={{ padding: '0.5rem' }}>Total Count</th>
                            <th style={{ padding: '0.5rem' }}>Avg Flowrate</th>
                        </tr>
                    </thead>
                    <tbody>
                        {history.map(item => (
                            <tr key={item.id} style={{ borderBottom: '1px solid #eee' }}>
                                <td style={{ padding: '0.5rem' }}>{new Date(item.uploaded_at).toLocaleString()}</td>
                                <td style={{ padding: '0.5rem' }}>{item.file_name}</td>
                                <td style={{ padding: '0.5rem' }}>{item.total_count}</td>
                                <td style={{ padding: '0.5rem' }}>{item.avg_flowrate.toFixed(2)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default History;
