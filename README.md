# Chemical Equipment Parameter Visualizer

A production-ready hybrid application for visualizing and analyzing chemical equipment data. This project demonstrates a robust full-stack architecture with Python (Django), React.js, and PyQt5.

## 🚀 Key Features
- **Hybrid Frontend**: Identical data access via Web (React) and Desktop (PyQt5) interfaces.
- **Advanced Analytics**: Automated analysis of Flowrate, Pressure, and Temperature using Pandas.
- **Secure Authentication**: Full JWT (JSON Web Token) implementation with expiration and refresh updates.
- **Reporting**: Automated PDF generation using ReportLab.
- **Data Retention**: Smart history management keeping only the last 5 datasets.

---

## 🏗 Architecture
- **Backend**: Django REST Framework + SimpleJWT + Pandas (Data Processing).
- **Web**: React (Vite) + Axios + Chart.js.
- **Desktop**: PyQt5 + Requests + Matplotlib (Native UI, not Electron).
- **Database**: SQLite (Configurable to PostgreSQL).

---

## 🔧 Configuration & Environment
The backend is configured to use environment variables for security.

### 1. Environment Setup
Create a `.env` file in the `backend/` directory based on `.env.example`:
```ini
SECRET_KEY=your-production-secret-key-super-secure
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

### 2. Authentication Flow
This project uses **JWT Authentication**.
1.  **Login**: User posts credentials to `/api/login/`.
2.  **Token Issue**: Server returns `access` (short-lived) and `refresh` (long-lived) tokens.
3.  **Storage**:
    *   **Web**: Tokens stored in `localStorage`.
    *   **Desktop**: Tokens stored in runtime memory (`APIClient` instance).
4.  **Usage**: All protected endpoints require header `Authorization: Bearer <access_token>`.
5.  **Expiry**: Frontends automatically detect 401 errors and prompt re-login.

### 3. Data Retention Policy
To maintain database performance and relevance:
*   The system strictly stores **only the last 5 uploaded datasets**.
*   When a 6th file is uploaded, the oldest record is automatically deleted from the SQLite database.
*   This logic is handled atomically in the `UploadView` transaction.

---

## 🛠 Setup & Run Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+

### Backend (Django)
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
# Ensure .env is created or system env vars are set
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Web Application (React)
```bash
cd web-frontend
npm install
npm run dev
```
*Access at http://localhost:5173*

### Desktop Application (PyQt5)
```bash
cd desktop-app
# Use same venv as backend covers all requirements
../backend/venv/Scripts/activate
python main.py
```

---

## 📸 Screenshots
*(Placeholders - Add actual screenshots here)*
| Dashboard | Charts |
|-----------|--------|
| ![Dashboard View](docs/dashboard_placeholder.png) | ![Charts View](docs/charts_placeholder.png) |

## 🎥 Demo
[Link to Demo Video](https://example.com/demo)

---

## 📚 API Documentation

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/upload/` | Upload CSV. Validates columns: `Equipment Name`, `Type`, `Flowrate`, `Pressure`, `Temperature`. | Bearer |
| GET | `/api/summary/` | Get latest batch stats. | Bearer |
| GET | `/api/history/` | Get last 5 batches. | Bearer |
| GET | `/api/report/` | Download analysis PDF. | Bearer |

## 🤝 Contributing
1. Fork the repository.
2. Create `feature/YourFeature` branch.
3. Commit and Push.
4. Open a Pull Request.

**Repository**: [Placeholder for GitHub Repo Link]
