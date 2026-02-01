import sys
import json
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QTabWidget, QTableWidget, 
                             QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DashboardWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Apply modern theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background: white;
            }
            QTabBar::tab {
                background: #e1e4e8;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #007bff;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f9f9f9;
                selection-background-color: #007bff;
            }
        """)

        # Maximize the window
        self.showMaximized()
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Tab 1: Dashboard
        self.dashboard_tab = QWidget()
        self.setup_dashboard_ui()
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        
        # Tab 2: History
        self.history_tab = QWidget()
        self.setup_history_ui()
        self.tabs.addTab(self.history_tab, "History")
        
        self.tabs.currentChanged.connect(self.on_tab_change)

        # Initial Load
        self.refresh_dashboard()

    def setup_dashboard_ui(self):
        layout = QVBoxLayout()
        
        # Controls
        controls_layout = QHBoxLayout()
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.handle_upload)
        controls_layout.addWidget(self.upload_btn)
        
        self.download_btn = QPushButton("Download Report PDF")
        self.download_btn.clicked.connect(self.handle_download)
        controls_layout.addWidget(self.download_btn)
        
        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.clicked.connect(self.refresh_dashboard)
        controls_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(controls_layout)
        
        # Stats
        stats_layout = QHBoxLayout()
        self.lbl_total = QLabel("Total: -")
        self.lbl_flow = QLabel("Avg Flow: -")
        self.lbl_pressure = QLabel("Avg Press: -")
        self.lbl_temp = QLabel("Avg Temp: -")
        for lbl in [self.lbl_total, self.lbl_flow, self.lbl_pressure, self.lbl_temp]:
            lbl.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; border: 1px solid #ccc;")
            stats_layout.addWidget(lbl)
        layout.addLayout(stats_layout)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        # Bar Chart Canvas
        self.bar_figure = Figure(figsize=(5, 4), dpi=100)
        self.bar_canvas = FigureCanvas(self.bar_figure)
        charts_layout.addWidget(self.bar_canvas)
        
        # Pie Chart Canvas
        self.pie_figure = Figure(figsize=(5, 4), dpi=100)
        self.pie_canvas = FigureCanvas(self.pie_figure)
        charts_layout.addWidget(self.pie_canvas)
        
        layout.addLayout(charts_layout)
        
        self.dashboard_tab.setLayout(layout)

    def setup_history_ui(self):
        layout = QVBoxLayout()
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Date", "File Name", "Total Count", "Avg Flowrate"])
        layout.addWidget(self.history_table)
        
        btn_refresh = QPushButton("Refresh History")
        btn_refresh.clicked.connect(self.refresh_history)
        layout.addWidget(btn_refresh)
        
        self.history_tab.setLayout(layout)

    def handle_upload(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "CSV files (*.csv)")
        if fname:
            success, result = self.api_client.upload_file(fname)
            if success:
                QMessageBox.information(self, "Success", "File uploaded successfully!")
                self.refresh_dashboard()
            else:
                QMessageBox.critical(self, "Error", f"Upload failed: {result}")

    def handle_download(self):
        fname, _ = QFileDialog.getSaveFileName(self, 'Save Report', 'c:\\report.pdf', "PDF files (*.pdf)")
        if fname:
            success, msg = self.api_client.download_report(fname)
            if success:
                QMessageBox.information(self, "Success", msg)
            else:
                QMessageBox.warning(self, "Error", msg)

    def refresh_dashboard(self):
        success, data = self.api_client.get_summary()
        if success and data:
            self.lbl_total.setText(f"Total: {data.get('total_count', 0)}")
            
            avg_flow = data.get('avg_flowrate')
            self.lbl_flow.setText(f"Avg Flow: {avg_flow:.2f}" if avg_flow is not None else "Avg Flow: -")

            avg_press = data.get('avg_pressure')
            self.lbl_pressure.setText(f"Avg Press: {avg_press:.2f}" if avg_press is not None else "Avg Press: -")
            
            avg_temp = data.get('avg_temperature')
            self.lbl_temp.setText(f"Avg Temp: {avg_temp:.2f}" if avg_temp is not None else "Avg Temp: -")
            
            # Update Bar Chart
            self.bar_figure.clear()
            ax = self.bar_figure.add_subplot(111)
            params = ['Flowrate', 'Pressure', 'Temp']
            # Use 0.0 for chart if value is None
            values = [
                avg_flow if avg_flow is not None else 0.0, 
                avg_press if avg_press is not None else 0.0, 
                avg_temp if avg_temp is not None else 0.0
            ]
            ax.bar(params, values, color=['blue', 'red', 'green'])
            ax.set_title("Average Parameters")
            self.bar_canvas.draw()
            
            # Update Pie Chart
            self.pie_figure.clear()
            ax_pie = self.pie_figure.add_subplot(111)
            
            dist = data.get('type_distribution', {})
            if isinstance(dist, str):
                try:
                    dist = json.loads(dist)
                except json.JSONDecodeError:
                    dist = {}
            
            if dist:
                labels = list(dist.keys())
                sizes = list(dist.values())
                
                ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax_pie.axis('equal')
                ax_pie.set_title("Equipment Types")
            else:
                 ax_pie.text(0.5, 0.5, "No Data", horizontalalignment='center', verticalalignment='center')

            self.pie_canvas.draw()
        else:
            # Clear or show empty state if api fails or no data
            pass

    def refresh_history(self):
        success, data = self.api_client.get_history()
        if success:
            self.history_table.setRowCount(len(data))
            for i, row in enumerate(data):
                self.history_table.setItem(i, 0, QTableWidgetItem(str(row['uploaded_at'])))
                self.history_table.setItem(i, 1, QTableWidgetItem(row['file_name']))
                self.history_table.setItem(i, 2, QTableWidgetItem(str(row['total_count'])))
                self.history_table.setItem(i, 3, QTableWidgetItem(str(row['avg_flowrate'])))

    def on_tab_change(self, index):
        if index == 1: # History tab
            self.refresh_history()
