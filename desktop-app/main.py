import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from api_client import APIClient
from login_window import LoginWindow
from dashboard_window import DashboardWindow

def main():
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    
    client = APIClient()
    
    # Show Login
    login = LoginWindow(client)
    if login.exec_() == LoginWindow.Accepted:
        # Show Dashboard if login success
        dashboard = DashboardWindow(client)
        dashboard.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
