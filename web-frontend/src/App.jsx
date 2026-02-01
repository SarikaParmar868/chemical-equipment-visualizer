import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import History from './pages/History';
import Upload from './pages/Upload';

function PrivateRoute({ children }) {
    const token = localStorage.getItem('access_token');
    return token ? children : <Navigate to="/login" />;
}

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route
                    path="/*"
                    element={
                        <PrivateRoute>
                            <Navbar />
                            <div className="container">
                                <Routes>
                                    <Route path="/" element={<Upload />} />
                                    <Route path="/dashboard" element={<Dashboard />} />
                                    <Route path="/history" element={<History />} />
                                </Routes>
                            </div>
                        </PrivateRoute>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
