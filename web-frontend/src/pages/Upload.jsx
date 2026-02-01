import React, { useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

function Upload() {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;
        const formData = new FormData();
        formData.append('file', file);

        setLoading(true);
        try {
            await api.post('upload/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            alert('Success: Dataset uploaded and analyzed successfully!');
            navigate('/dashboard'); // Redirect to dashboard after success
        } catch (err) {
            console.error(err);
            const msg = err.response?.data?.error || "An unexpected error occurred.";
            alert(`Upload Failed: ${msg}`);
        }
        setLoading(false);
    };

    return (
        <div className="card" style={{ maxWidth: '600px', margin: '2rem auto' }}>
            <h2>Upload Dataset</h2>
            <p>Select a CSV file containing chemical equipment data to upload and analyze.</p>
            <form onSubmit={handleUpload} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
                <input
                    type="file"
                    accept=".csv"
                    onChange={(e) => setFile(e.target.files[0])}
                    style={{ padding: '0.5rem', border: '1px solid #ddd', borderRadius: '4px' }}
                />
                <button
                    type="submit"
                    className="btn"
                    disabled={loading || !file}
                    style={{ alignSelf: 'flex-start' }}
                >
                    {loading ? 'Uploading...' : 'Upload File'}
                </button>
            </form>
        </div>
    );
}

export default Upload;
