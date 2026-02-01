import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigate('/login');
    };

    return (
        <nav>
            <div style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>Chemical Visualizer</div>
            <div>
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/">Upload</Link>
                <Link to="/history">History</Link>
                <button onClick={handleLogout} className="btn" style={{ background: '#ef4444' }}>Logout</button>
            </div>
        </nav>
    );
}

export default Navbar;
