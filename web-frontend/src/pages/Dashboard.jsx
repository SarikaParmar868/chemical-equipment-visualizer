import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

function Dashboard() {
    const [data, setData] = useState(null);

    const fetchSummary = async () => {
        try {
            const res = await api.get('summary/');
            setData(res.data);
        } catch (err) {
            console.error("No data", err);
        }
    };

    useEffect(() => {
        fetchSummary();
    }, []);

    const downloadReport = async () => {
        try {
            const res = await api.get('report/', { responseType: 'blob' });
            const url = window.URL.createObjectURL(new Blob([res.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `report_${data.id}.pdf`);
            document.body.appendChild(link);
            link.click();
        } catch (err) {
            alert("Failed to download report");
        }
    };

    if (!data) return (
        <div>
            <h2>Dashboard</h2>
            <div className="card">
                <h3>No Data Available</h3>
                <p>Please upload a dataset to view analytics.</p>
                <Link to="/upload" className="btn">Go to Upload</Link>
            </div>
        </div>
    );

    const barData = data ? {
        labels: ['Flowrate', 'Pressure', 'Temperature'],
        datasets: [{
            label: 'Average Values',
            data: [data.avg_flowrate, data.avg_pressure, data.avg_temperature],
            backgroundColor: ['rgba(53, 162, 235, 0.5)', 'rgba(255, 99, 132, 0.5)', 'rgba(75, 192, 192, 0.5)'],
        }]
    } : null;

    const getDistribution = () => {
        if (!data || !data.type_distribution) return {};
        try {
            return typeof data.type_distribution === 'string'
                ? JSON.parse(data.type_distribution)
                : data.type_distribution;
        } catch (e) {
            return {};
        }
    };

    const distribution = getDistribution();

    const pieData = (data && Object.keys(distribution).length > 0) ? {
        labels: Object.keys(distribution),
        datasets: [{
            data: Object.values(distribution),
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
            ],
            borderWidth: 1,
        }]
    } : null;

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h2>Dashboard</h2>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <Link to="/upload" className="btn">New Upload</Link>
                    <button onClick={downloadReport} className="btn">Download PDF</button>
                </div>
            </div>

            <div className="stats-grid">
                <div className="stat-card">
                    <h3>Total Equipment</h3>
                    <div className="stat-value">{data.total_count || 0}</div>
                </div>
                <div className="stat-card">
                    <h3>Avg Flowrate</h3>
                    <div className="stat-value">{data.avg_flowrate ? data.avg_flowrate.toFixed(2) : '-'}</div>
                </div>
                <div className="stat-card">
                    <h3>Avg Pressure</h3>
                    <div className="stat-value">{data.avg_pressure ? data.avg_pressure.toFixed(2) : '-'}</div>
                </div>
                <div className="stat-card">
                    <h3>Avg Temp</h3>
                    <div className="stat-value">{data.avg_temperature ? data.avg_temperature.toFixed(2) : '-'}</div>
                </div>
            </div>

            <div className="grid">
                <div className="card">
                    <h3>Parameter Averages</h3>
                    {barData && <Bar data={barData} />}
                </div>
                <div className="card">
                    <h3>Equipment Type Distribution</h3>
                    <div style={{ height: '300px', display: 'flex', justifyContent: 'center' }}>
                        {pieData && <Pie data={pieData} />}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
